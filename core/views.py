from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Hospital, Department, Doctor, BedBooking, Appointment, UserProfile
from .forms import BedBookingForm, AppointmentForm, PaymentForm, UserRegisterForm, UserLoginForm


# ── Auth Views ──────────────────────────────────────────────────────────────

def user_register(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user            = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name  = form.cleaned_data['last_name']
            user.email      = form.cleaned_data['email']
            user.save()
            UserProfile.objects.create(user=user, phone=form.cleaned_data['phone'])
            login(request, user)
            messages.success(request, f"Welcome {user.first_name}! Your account has been created.")
            return redirect('user_dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'core/auth/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # allow login by email
            if '@' in username:
                try:
                    username = User.objects.get(email=username).username
                except User.DoesNotExist:
                    pass
            user = authenticate(request, username=username, password=password)
            if user and not user.is_staff:
                login(request, user)
                next_url = request.GET.get('next', 'user_dashboard')
                return redirect(next_url)
            elif user and user.is_staff:
                messages.error(request, "Admin accounts must use the admin panel.")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request, 'core/auth/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('index')


# ── User Dashboard ──────────────────────────────────────────────────────────

@login_required(login_url='/login/')
def user_dashboard(request):
    bed_bookings = BedBooking.objects.filter(user=request.user).order_by('-created_at')
    appointments = Appointment.objects.filter(user=request.user).order_by('-created_at')
    stats = {
        'total_bookings':        bed_bookings.count(),
        'approved_bookings':     bed_bookings.filter(status='Approved').count(),
        'pending_bookings':      bed_bookings.filter(status='Pending').count(),
        'cancelled_bookings':    bed_bookings.filter(status='Cancelled').count(),
        'total_appointments':    appointments.count(),
        'approved_appointments': appointments.filter(status='Approved').count(),
        'pending_appointments':  appointments.filter(status='Pending').count(),
        'completed_appointments':appointments.filter(status='Completed').count(),
    }
    return render(request, 'core/dashboard/dashboard.html', {
        'bed_bookings': bed_bookings,
        'appointments': appointments,
        'stats': stats,
    })


@login_required(login_url='/login/')
def my_bookings(request):
    status_filter = request.GET.get('status', '')
    bookings = BedBooking.objects.filter(user=request.user).order_by('-created_at')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    return render(request, 'core/dashboard/my_bookings.html', {
        'bookings': bookings,
        'status_filter': status_filter,
    })


@login_required(login_url='/login/')
def my_appointments(request):
    status_filter = request.GET.get('status', '')
    appointments = Appointment.objects.filter(user=request.user).order_by('-created_at')
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    return render(request, 'core/dashboard/my_appointments.html', {
        'appointments': appointments,
        'status_filter': status_filter,
    })


@login_required(login_url='/login/')
def booking_detail(request, booking_id):
    booking = get_object_or_404(BedBooking, id=booking_id, user=request.user)
    return render(request, 'core/dashboard/booking_detail.html', {'booking': booking})


@login_required(login_url='/login/')
def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
    return render(request, 'core/dashboard/appointment_detail.html', {'appointment': appointment})


# ── Public Views ────────────────────────────────────────────────────────────

def index(request):
    areas = Hospital.objects.values_list('area', flat=True).distinct().order_by('area')
    return render(request, 'core/index.html', {'areas': areas})


def search(request):
    query    = request.GET.get('q', '')
    area     = request.GET.get('area', '')
    bed_type = request.GET.get('bed_type', '')
    hospitals = Hospital.objects.filter(is_active=True)
    if query:
        hospitals = hospitals.filter(name__icontains=query) | hospitals.filter(area__icontains=query)
    if area:
        hospitals = hospitals.filter(area=area)
    if bed_type == 'icu':
        hospitals = hospitals.filter(available_icu_beds__gt=0)
    elif bed_type == 'available':
        hospitals = hospitals.filter(available_beds__gt=0)
    areas = Hospital.objects.values_list('area', flat=True).distinct().order_by('area')
    return render(request, 'core/search.html', {
        'hospitals': hospitals, 'query': query,
        'area': area, 'areas': areas, 'total': hospitals.count(),
    })


def hospital_detail(request, hospital_id):
    hospital    = get_object_or_404(Hospital, id=hospital_id, is_active=True)
    departments = hospital.departments.all()
    doctors     = hospital.doctors.all()
    return render(request, 'core/hospital_detail.html', {
        'hospital': hospital, 'departments': departments, 'doctors': doctors,
    })


def get_doctors(request):
    dept_id = request.GET.get('department_id')
    doctors = Doctor.objects.filter(department_id=dept_id).values(
        'id', 'name', 'qualification', 'consultation_fee')
    return JsonResponse({'doctors': list(doctors)})


# ── Booking Flow (login required) ───────────────────────────────────────────

@login_required(login_url='/login/')
def bed_booking(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id, is_active=True)
    if request.method == 'POST':
        form = BedBookingForm(request.POST)
        if form.is_valid():
            booking          = form.save(commit=False)
            booking.hospital = hospital
            booking.user     = request.user
            booking.save()
            return redirect('payment', booking_type='bed', booking_id=booking.id)
    else:
        # pre-fill from user account
        phone = ''
        try:
            phone = request.user.profile.phone
        except Exception:
            pass
        form = BedBookingForm(initial={
            'patient_name':  request.user.get_full_name() or request.user.username,
            'patient_email': request.user.email,
            'patient_phone': phone,
        })
    return render(request, 'core/bed_booking.html', {'hospital': hospital, 'form': form})


@login_required(login_url='/login/')
def appointment(request, hospital_id):
    hospital    = get_object_or_404(Hospital, id=hospital_id, is_active=True)
    departments = hospital.departments.all()
    if request.method == 'POST':
        form      = AppointmentForm(request.POST)
        dept_id   = request.POST.get('department')
        doctor_id = request.POST.get('doctor')
        if form.is_valid():
            appt          = form.save(commit=False)
            appt.hospital = hospital
            appt.user     = request.user
            if dept_id:
                try:    appt.department = Department.objects.get(id=dept_id)
                except: pass
            if doctor_id:
                try:
                    appt.doctor      = Doctor.objects.get(id=doctor_id)
                    appt.amount_paid = appt.doctor.consultation_fee
                except: pass
            appt.save()
            return redirect('payment', booking_type='appointment', booking_id=appt.id)
    else:
        phone = ''
        try:
            phone = request.user.profile.phone
        except Exception:
            pass
        form = AppointmentForm(initial={
            'patient_name':  request.user.get_full_name() or request.user.username,
            'patient_email': request.user.email,
            'patient_phone': phone,
        })
    all_doctors = Doctor.objects.filter(hospital=hospital).select_related('department').order_by('department__name', 'name')
    return render(request, 'core/appointment.html', {
        'hospital': hospital, 'departments': departments,
        'all_doctors': all_doctors, 'form': form,
    })


@login_required(login_url='/login/')
def payment(request, booking_type, booking_id):
    if booking_type == 'bed':
        booking      = get_object_or_404(BedBooking,  id=booking_id, user=request.user)
    else:
        booking      = get_object_or_404(Appointment, id=booking_id, user=request.user)
    if request.method == 'POST':
        booking.payment_method = request.POST.get('payment_method', 'UPI')
        booking.payment_status = 'Paid'
        booking.save()
        return redirect('confirmation', booking_type=booking_type, booking_id=booking_id)
    return render(request, 'core/payment.html', {
        'booking':      booking,
        'booking_type': booking_type,
        'amount':       booking.amount_paid,
        'patient_name': booking.patient_name,
        'form':         PaymentForm(),
    })


@login_required(login_url='/login/')
def confirmation(request, booking_type, booking_id):
    if booking_type == 'bed':
        booking = get_object_or_404(BedBooking,  id=booking_id, user=request.user)
    else:
        booking = get_object_or_404(Appointment, id=booking_id, user=request.user)
    return render(request, 'core/confirmation.html', {
        'booking': booking, 'booking_type': booking_type,
    })
