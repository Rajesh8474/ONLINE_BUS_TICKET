from django.urls import path
from . import views

urlpatterns = [
    # Pages
    path('health/', views.health),
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('bus-detail/', views.bus_detail, name='bus_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('ticket/', views.ticket_view, name='ticket'),
    path('bookings/', views.my_bookings, name='my_bookings'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),

    # API
    path('api/login/', views.api_login, name='api_login'),
    path('api/register/', views.api_register, name='api_register'),
    path('api/logout/', views.api_logout, name='api_logout'),
    path('api/admin-login/', views.api_admin_login, name='api_admin_login'),
    path('api/admin-logout/', views.api_admin_logout, name='api_admin_logout'),
    path('api/save-temp-booking/', views.api_save_temp_booking, name='api_save_temp_booking'),
    path('api/confirm-booking/', views.api_confirm_booking, name='api_confirm_booking'),
    path('api/my-bookings/', views.api_my_bookings, name='api_my_bookings'),
    path('api/cancel-booking/', views.api_cancel_booking, name='api_cancel_booking'),
    path('api/submit-review/', views.api_submit_review, name='api_submit_review'),
    path('api/update-profile/', views.api_update_profile, name='api_update_profile'),
    path('api/change-password/', views.api_change_password, name='api_change_password'),
    path('api/reset-password/', views.api_reset_password, name='api_reset_password'),
    path('api/check-email/', views.api_check_email, name='api_check_email'),

    # Admin API
    path('api/admin/stats/', views.api_admin_stats, name='api_admin_stats'),
    path('api/admin/buses/', views.api_admin_buses, name='api_admin_buses'),
    path('api/admin/save-bus/', views.api_admin_save_bus, name='api_admin_save_bus'),
    path('api/admin/delete-bus/', views.api_admin_delete_bus, name='api_admin_delete_bus'),
    path('api/admin/bookings/', views.api_admin_all_bookings, name='api_admin_all_bookings'),
    path('api/admin/users/', views.api_admin_users, name='api_admin_users'),
    path('api/admin/charts/', views.api_admin_booking_charts, name='api_admin_charts'),
]
