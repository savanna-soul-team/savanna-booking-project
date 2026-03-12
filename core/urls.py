from django.urls import path
from . import views

urlpatterns = [
    # --- Main Tour Views ---
    path('', views.tour_list, name='tour_list'),
    path('tour/<int:pk>/', views.tour_detail, name='tour_detail'),
    path('destinations/', views.tour_list, name='destinations_hub'),

    # --- Destination Filters (The Master Dynamic Path) ---
    path('destinations/<str:country_name>/', views.destination_filter, name='destination_filter'),

    # --- Auth & Profile ---
    path('register/', views.register_view, name='register'),
    path('login/',    views.login_view,    name='login'),
    path('logout/',   views.logout_view,   name='logout'),
    path('profile/',  views.profile_view,  name='profile'),

    # --- Bookings & Payments ---
    path('book/<int:tour_pk>/',          views.create_booking,       name='create_booking'),
    path('bookings/',                    views.my_bookings,          name='my_bookings'),
    path('bookings/<int:pk>/edit/',      views.edit_booking,         name='edit_booking'),
    path('bookings/<int:pk>/cancel/',    views.cancel_booking,       name='cancel_booking'),
    path('bookings/<int:pk>/pay/',       views.payment_view,         name='payment'),
    path('bookings/<int:pk>/status/',    views.payment_status,       name='payment_status'),
    path('bookings/<int:pk>/success/',   views.booking_success,      name='booking_success'),

    # --- M-Pesa Callback ---
    path('mpesa/callback/', views.mpesa_callback, name='mpesa_callback'),
]