from django.urls import path
from . import views, admin_views

urlpatterns = [
    # ── Public ──────────────────────────────────────────────────
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('hospital/<int:hospital_id>/', views.hospital_detail, name='hospital_detail'),
    path('ajax/doctors/', views.get_doctors, name='get_doctors'),

    # ── Auth ────────────────────────────────────────────────────
    path('register/', views.user_register, name='user_register'),
    path('login/',    views.user_login,    name='user_login'),
    path('logout/',   views.user_logout,   name='user_logout'),

    # ── User Dashboard ───────────────────────────────────────────
    path('dashboard/',                                           views.user_dashboard,    name='user_dashboard'),
    path('dashboard/bookings/',                                  views.my_bookings,       name='my_bookings'),
    path('dashboard/bookings/<int:booking_id>/',                 views.booking_detail,    name='booking_detail'),
    path('dashboard/appointments/',                              views.my_appointments,   name='my_appointments'),
    path('dashboard/appointments/<int:appointment_id>/',         views.appointment_detail,name='appointment_detail'),

    # ── Booking Flow (login required) ────────────────────────────
    path('book/bed/<int:hospital_id>/',                          views.bed_booking,  name='bed_booking'),
    path('book/appointment/<int:hospital_id>/',                  views.appointment,  name='appointment'),
    path('payment/<str:booking_type>/<int:booking_id>/',         views.payment,      name='payment'),
    path('confirmation/<str:booking_type>/<int:booking_id>/',    views.confirmation, name='confirmation'),

    # ── Admin Panel ──────────────────────────────────────────────
    path('admin-panel/login/',      admin_views.admin_login,              name='admin_login'),
    path('admin-panel/logout/',     admin_views.admin_logout,             name='admin_logout'),
    path('admin-panel/dashboard/',  admin_views.admin_dashboard,          name='admin_dashboard'),
    path('admin-panel/beds/',       admin_views.manage_beds,              name='manage_beds'),
    path('admin-panel/bookings/',   admin_views.manage_bookings,          name='manage_bookings'),
    path('admin-panel/bookings/<int:booking_id>/status/', admin_views.update_booking_status, name='update_booking_status'),
    path('admin-panel/appointments/', admin_views.manage_appointments,    name='manage_appointments'),
    path('admin-panel/appointments/<int:appointment_id>/status/', admin_views.update_appointment_status, name='update_appointment_status'),
]
