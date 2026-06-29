from django.contrib import admin
from .models import Hospital, Department, Doctor, BedBooking, Appointment, UserProfile


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display  = ['name', 'area', 'total_beds', 'available_beds', 'is_active']
    list_filter   = ['area', 'is_active']
    search_fields = ['name', 'area']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'hospital']
    list_filter  = ['hospital']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display  = ['name', 'department', 'hospital', 'consultation_fee']
    list_filter   = ['hospital', 'department']


@admin.register(BedBooking)
class BedBookingAdmin(admin.ModelAdmin):
    list_display  = ['booking_id', 'patient_name', 'hospital', 'admission_date', 'status', 'user']
    list_filter   = ['status', 'hospital']
    search_fields = ['booking_id', 'patient_name']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display  = ['appointment_id', 'patient_name', 'hospital', 'doctor', 'appointment_date', 'status', 'user']
    list_filter   = ['status', 'hospital']
    search_fields = ['appointment_id', 'patient_name']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display  = ['user', 'phone']
    search_fields = ['user__username', 'user__email']
