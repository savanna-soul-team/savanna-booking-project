import json
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Tour, Booking, MpesaTransaction
from .forms import RegisterForm, LoginForm, BookingForm, PaymentForm
from .mpesa import MpesaClient

logger = logging.getLogger(__name__)


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
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/my_bookings.html', {'bookings': bookings})

@login_required
def edit_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user,
                                status='pending')
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
            client = MpesaClient()
            result = client.stk_push(
                phone_number=phone,
                amount=booking.total_kes,
                account_ref=f"SB-{booking.pk}",
                description=f"{booking.tour.title[:20]}",
            )
            if result.get('ResponseCode') == '0':
                MpesaTransaction.objects.update_or_create(
                    booking=booking,
                    defaults={
                        'checkout_request_id': result['CheckoutRequestID'],
                        'merchant_request_id': result['MerchantRequestID'],
                        'phone_number': phone,
                        'amount': booking.total_kes,
                        'status': 'pending',
                    }
                )
                return JsonResponse({
                    'success': True,
                    'checkout_request_id': result['CheckoutRequestID'],
                    'message': 'STK push sent. Enter PIN on your phone.'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': result.get('errorMessage', 'STK push failed.')
                })
    else:
        form = PaymentForm(initial={
            'phone_number': request.user.phone_number
        })
    return render(request, 'core/payment.html', {
        'booking': booking,
        'form': form,
    })

@login_required
def payment_status(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    try:
        txn = booking.mpesa_transaction
        return JsonResponse({
            'status': txn.status,
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
                checkout_request_id=checkout_id
            )
        except MpesaTransaction.DoesNotExist:
            return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})

        txn.result_code = result_code
        txn.result_desc = result_desc

        if result_code == 0:
            items = stk_callback.get('CallbackMetadata', {}).get('Item', [])
            meta  = {i['Name']: i.get('Value') for i in items}
            txn.mpesa_receipt    = str(meta.get('MpesaReceiptNumber', ''))
            txn.status           = 'success'
            booking              = txn.booking
            booking.status       = 'confirmed'
            booking.mpesa_ref    = txn.mpesa_receipt
            booking.save()
        else:
            txn.status = 'failed'

        txn.save()

    except (KeyError, json.JSONDecodeError) as e:
        logger.error(f"M-Pesa callback error: {e}")

    return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})