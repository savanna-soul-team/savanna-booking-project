import json
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import User, Tour, Booking, MpesaTransaction
from .forms import RegisterForm, LoginForm, BookingForm, PaymentForm
from django_daraja.mpesa.core import MpesaClient
from .forms import RegisterForm, LoginForm, BookingForm, PaymentForm, ProfileForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
logger = logging.getLogger(__name__)



def send_booking_email(user_email, tour_name, price):
    subject = f'Your Adventure Awaits: {tour_name} Confirmed!'

    # 1. Create the HTML version of the email
    html_message = render_to_string('emails/booking_confirmed.html', {
        'tour_name': tour_name,
        'price': price,
    })

    # 2. Create a plain-text version for older email clients
    plain_message = strip_tags(html_message)

    # 3. Send it using your settings.py config
    send_mail(
        subject,
        plain_message,
        'Savanna & Soul <noreply@savannabooking.com>',
        [user_email],
        html_message=html_message,
    )
# ── Tours ─────────────────────────────────────────────────────
def tour_list(request):
    country  = request.GET.get('country', '')
    category = request.GET.get('category', '')
    tours = Tour.objects.filter(is_active=True)
    if country:
        tours = tours.filter(country=country)
    if category:
        tours = tours.filter(category=category)
    return render(request, 'core/tour_list.html', {
        'tours': tours,
        'selected_country': country,
        'selected_category': category,
    })

def tour_detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk, is_active=True)
    return render(request, 'core/tour_detail.html', {'tour': tour})


# ── Auth ──────────────────────────────────────────────────────
def register_view(request):
    if request.user.is_authenticated:
        return redirect('tour_list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.first_name}! 🌍")
            return redirect('tour_list')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('tour_list')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}!")
            return redirect(request.GET.get('next', 'tour_list'))
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('tour_list')


# ── Bookings ──────────────────────────────────────────────────
@login_required
def create_booking(request, tour_pk):
    tour = get_object_or_404(Tour, pk=tour_pk, is_active=True)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.tour = tour
            booking.save()
            return redirect('payment', pk=booking.pk)
    else:
        form = BookingForm()
    return render(request, 'core/create_booking.html', {
        'tour': tour,
        'form': form,
    })

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(
        user=request.user).order_by('-created_at')
    return render(request, 'core/my_bookings.html', {'bookings': bookings})

@login_required
def edit_booking(request, pk):
    booking = get_object_or_404(
        Booking, pk=pk, user=request.user, status='pending')
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking updated!")
            return redirect('my_bookings')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'core/create_booking.html', {
        'form': form,
        'tour': booking.tour,
        'edit': True,
    })

@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, "Booking cancelled.")
    return redirect('my_bookings')


# ── Payment ───────────────────────────────────────────────────
@login_required
def payment_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if booking.status == 'confirmed':
        return redirect('booking_success', pk=booking.pk)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            phone  = form.cleaned_data['phone_number']
            cl     = MpesaClient()
            resp   = cl.stk_push(
                phone,
                booking.total_kes,
                f"SB-{booking.pk}",
                f"{booking.tour.title[:20]}",
                settings.MPESA_CALLBACK_URL,
            )
            if resp.response_code == '0':
                MpesaTransaction.objects.update_or_create(
                    booking=booking,
                    defaults={
                        'checkout_request_id': resp.checkout_request_id,
                        'merchant_request_id': resp.merchant_request_id,
                        'phone_number':        phone,
                        'amount':              booking.total_kes,
                        'status':              'pending',
                    }
                )
                return JsonResponse({
                    'success': True,
                    'message': 'STK push sent. Enter PIN on your phone.',
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': resp.response_description or 'STK push failed.',
                })
    else:
        form = PaymentForm(initial={
            'phone_number': request.user.phone_number
        })

    return render(request, 'core/payment.html', {
        'booking': booking,
        'form':    form,
    })

@login_required
def payment_status(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    try:
        txn = booking.mpesa_transaction
        return JsonResponse({
            'status':  txn.status,
            'receipt': txn.mpesa_receipt,
        })
    except MpesaTransaction.DoesNotExist:
        return JsonResponse({'status': 'pending'})

@login_required
def booking_success(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'core/success.html', {'booking': booking})


# ── M-Pesa Callback ───────────────────────────────────────────
@csrf_exempt
def mpesa_callback(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data         = json.loads(request.body)
        stk_callback = data['Body']['stkCallback']
        checkout_id  = stk_callback['CheckoutRequestID']
        result_code  = stk_callback['ResultCode']
        result_desc  = stk_callback['ResultDesc']

        try:
            txn = MpesaTransaction.objects.get(
                checkout_request_id=checkout_id)
        except MpesaTransaction.DoesNotExist:
            return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})

        txn.result_code = result_code
        txn.result_desc = result_desc

        if result_code == 0:
            items = stk_callback.get(
                'CallbackMetadata', {}).get('Item', [])
            meta             = {i['Name']: i.get('Value') for i in items}
            txn.mpesa_receipt = str(meta.get('MpesaReceiptNumber', ''))
            txn.status        = 'success'
            booking           = txn.booking
            booking.status    = 'confirmed'
            booking.mpesa_ref = txn.mpesa_receipt
            booking.save()
        else:
            txn.status = 'failed'

        txn.save()

    except (KeyError, json.JSONDecodeError) as e:
        logger.error(f"M-Pesa callback error: {e}")

    return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})

# ── Profile ───────────────────────────────────────────────────
@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'core/profile.html', {'form': form})


import os
from django.shortcuts import render
from .models import Tour


def destination_filter(request, country_name):
    tours = Tour.objects.filter(location__icontains=country_name)

    # Logic: Look for a template named 'kenya.html' or 'south-africa.html'
    # Fallback to 'tour_list.html' if the specific one doesn't exist
    template_name = f'core/{country_name.lower().replace(" ", "-")}.html'

    # We check if the file exists; if not, use the default
    return render(request, [template_name, 'core/tour_list.html'], {
        'tours': tours,
        'selected_country': country_name.title()
    })
