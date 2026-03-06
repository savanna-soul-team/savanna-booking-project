from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Booking


# ── Auth Forms ────────────────────────────────────────────────
class RegisterForm(UserCreationForm):
    first_name   = forms.CharField(max_length=50)
    last_name    = forms.CharField(max_length=50)
    email        = forms.EmailField()
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        help_text="Format: 2547XXXXXXXX"
    )

    class Meta:
        model  = User
        fields = [
            'first_name', 'last_name', 'email',
            'username', 'phone_number',
            'password1', 'password2'
        ]


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username')


# ── Booking Form ──────────────────────────────────────────────
class BookingForm(forms.ModelForm):
    class Meta:
        model  = Booking
        fields = ['travel_date', 'guests', 'special_notes']
        widgets = {
            'travel_date':   forms.DateInput(attrs={'type': 'date'}),
            'special_notes': forms.Textarea(attrs={'rows': 3}),
        }


# ── Payment Form ──────────────────────────────────────────────
class PaymentForm(forms.Form):
    phone_number = forms.CharField(
        max_length=12,
        label="M-Pesa Phone Number",
        help_text="Format: 2547XXXXXXXX"
    )

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number'].strip().replace('+', '')
        if not phone.startswith('254') or len(phone) != 12:
            raise forms.ValidationError(
                "Enter a valid Safaricom number in format 2547XXXXXXXX"
            )
        return phone

class ProfileForm(forms.ModelForm):
    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'profile_pic']
        widgets = {
            'profile_pic': forms.FileInput(),
        }