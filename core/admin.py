from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Tour, Booking, MpesaTransaction

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display  = ['username', 'email', 'first_name', 'last_name', 'phone_number']
    fieldsets     = UserAdmin.fieldsets + (
        ('Extra', {'fields': ('phone_number', 'profile_pic')}),
    )

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display  = ['title', 'location', 'country', 'category', 'price_usd', 'is_active']
    list_filter   = ['country', 'category', 'is_active']
    search_fields = ['title', 'location']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display  = ['user', 'tour', 'travel_date', 'guests', 'total_kes', 'status']
    list_filter   = ['status']
    search_fields = ['user__username', 'tour__title']

@admin.register(MpesaTransaction)
class MpesaTransactionAdmin(admin.ModelAdmin):
    list_display  = ['booking', 'phone_number', 'amount', 'status', 'mpesa_receipt', 'created_at']
    list_filter   = ['status']