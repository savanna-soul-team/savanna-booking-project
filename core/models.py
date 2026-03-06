
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


# ── Custom User ──────────────────────────────────────────────
class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    profile_pic  = models.ImageField(upload_to='profiles/', blank=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"


# ── Tour ─────────────────────────────────────────────────────
class Tour(models.Model):
    CATEGORY_CHOICES = [
        ('safari',    'Safari'),
        ('cultural',  'Cultural'),
        ('adventure', 'Adventure'),
    ]
    COUNTRY_CHOICES = [
        ('kenya',       'Kenya'),
        ('tanzania',    'Tanzania'),
        ('southafrica', 'South Africa'),
        ('morocco',     'Morocco'),
        ('uganda',      'Uganda'),
    ]

    title       = models.CharField(max_length=200)
    location    = models.CharField(max_length=100)
    country     = models.CharField(max_length=50, choices=COUNTRY_CHOICES)
    category    = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    price_usd   = models.DecimalField(max_digits=10, decimal_places=2)
    duration    = models.CharField(max_length=50)
    rating      = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    badge       = models.CharField(max_length=50, blank=True)
    image       = models.ImageField(upload_to='tours/', blank=True)
    image_url   = models.URLField(blank=True)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def get_image(self):
        return self.image.url if self.image else self.image_url

    def price_kes(self):
        return int(self.price_usd * 130)

    def __str__(self):
        return self.title


# ── Booking ───────────────────────────────────────────────────
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user          = models.ForeignKey(User, on_delete=models.CASCADE,
                                      related_name='bookings')
    tour          = models.ForeignKey(Tour, on_delete=models.CASCADE)
    travel_date   = models.DateField()
    guests        = models.PositiveIntegerField(default=1)
    special_notes = models.TextField(blank=True)
    total_usd     = models.DecimalField(max_digits=10, decimal_places=2,
                                        editable=False, default=0)
    total_kes     = models.IntegerField(editable=False, default=0)
    status        = models.CharField(max_length=20, choices=STATUS_CHOICES,
                                     default='pending')
    mpesa_ref     = models.CharField(max_length=50, blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.total_usd = self.tour.price_usd * self.guests
        self.total_kes = int(self.total_usd * 130)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} → {self.tour} on {self.travel_date}"


# ── M-Pesa Transaction ────────────────────────────────────────
class MpesaTransaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed',  'Failed'),
    ]

    booking             = models.OneToOneField(Booking, on_delete=models.CASCADE,
                                               related_name='mpesa_transaction')
    checkout_request_id = models.CharField(max_length=100, unique=True)
    merchant_request_id = models.CharField(max_length=100)
    phone_number        = models.CharField(max_length=15)
    amount              = models.IntegerField()
    mpesa_receipt       = models.CharField(max_length=50, blank=True)
    status              = models.CharField(max_length=20, choices=STATUS_CHOICES,
                                           default='pending')
    result_code         = models.IntegerField(null=True, blank=True)
    result_desc         = models.CharField(max_length=255, blank=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"M-Pesa {self.checkout_request_id} [{self.status}]"