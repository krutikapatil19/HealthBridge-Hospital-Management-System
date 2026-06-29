from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Hospital, BedBooking, Appointment


def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    if request.method == 'POST':
        email    = request.POST.get('email')
        password = request.POST.get('password')
        user     = authenticate(request, username=email, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')
    return render(request, 'admin_panel/login.html')


def admin_logout(request):
    logout(request)
    return redirect('admin_login')


@login_required(login_url='/admin-panel/login/')
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('user_dashboard')

    hospitals   = Hospital.objects.filter(is_active=True)
    total_beds  = sum(h.total_beds for h in hospitals)
    avail_beds  = sum(h.available_beds for h in hospitals)
    occupied    = total_beds - avail_beds
    pending_beds = BedBooking.objects.filter(status='Pending').count()
    pending_apts = Appointment.objects.filter(status='Pending').count()

    return render(request, 'admin_panel/dashboard.html', {
        'hospitals':           hospitals,
        'total_beds':          total_beds,
        'available_beds':      avail_beds,
        'occupied_beds':       occupied,
        'hospital_count':      hospitals.count(),
        'recent_bookings':     BedBooking.objects.select_related('hospital','user').order_by('-created_at')[:5],
        'recent_appointments': Appointment.objects.select_related('hospital','doctor','user').order_by('-created_at')[:5],
        'pending_beds':        pending_beds,
        'pending_apts':        pending_apts,
        'total_bookings':      BedBooking.objects.count(),
        'total_appointments':  Appointment.objects.count(),
    })


@login_required(login_url='/admin-panel/login/')
def manage_beds(request):
    if not request.user.is_staff:
        return redirect('user_dashboard')
    hospitals = Hospital.objects.filter(is_active=True)
    if request.method == 'POST':
        hospital = get_object_or_404(Hospital, id=request.POST.get('hospital_id'))
        hospital.total_beds         = request.POST.get('total_beds',         hospital.total_beds)
        hospital.available_beds     = request.POST.get('available_beds',     hospital.available_beds)
        hospital.icu_beds           = request.POST.get('icu_beds',           hospital.icu_beds)
        hospital.available_icu_beds = request.POST.get('available_icu_beds', hospital.available_icu_beds)
        hospital.save()
        messages.success(request, f'Bed availability updated for {hospital.name}')
        return redirect('manage_beds')
    return render(request, 'admin_panel/manage_beds.html', {'hospitals': hospitals})


@login_required(login_url='/admin-panel/login/')
def manage_bookings(request):
    if not request.user.is_staff:
        return redirect('user_dashboard')
    status_filter = request.GET.get('status', '')
    bookings = BedBooking.objects.select_related('hospital', 'user').order_by('-created_at')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    return render(request, 'admin_panel/manage_bookings.html', {
        'bookings': bookings, 'status_filter': status_filter,
    })


@login_required(login_url='/admin-panel/login/')
def update_booking_status(request, booking_id):
    if not request.user.is_staff:
        return redirect('user_dashboard')
    booking = get_object_or_404(BedBooking, id=booking_id)
    if request.method == 'POST':
        new_status   = request.POST.get('status')
        admin_notes  = request.POST.get('admin_notes', '')
        if new_status in ['Pending', 'Approved', 'Cancelled']:
            booking.status      = new_status
            booking.admin_notes = admin_notes
            booking.save()
            messages.success(request, f'Booking {booking.booking_id} updated to {new_status}')
    return redirect('manage_bookings')


@login_required(login_url='/admin-panel/login/')
def manage_appointments(request):
    if not request.user.is_staff:
        return redirect('user_dashboard')
    status_filter = request.GET.get('status', '')
    appointments = Appointment.objects.select_related('hospital', 'doctor', 'department', 'user').order_by('-created_at')
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    return render(request, 'admin_panel/manage_appointments.html', {
        'appointments': appointments, 'status_filter': status_filter,
    })


@login_required(login_url='/admin-panel/login/')
def update_appointment_status(request, appointment_id):
    if not request.user.is_staff:
        return redirect('user_dashboard')
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        new_status   = request.POST.get('status')
        admin_notes  = request.POST.get('admin_notes', '')
        if new_status in ['Pending', 'Approved', 'Cancelled', 'Completed']:
            appointment.status      = new_status
            appointment.admin_notes = admin_notes
            appointment.save()
            messages.success(request, f'Appointment {appointment.appointment_id} updated to {new_status}')
    return redirect('manage_appointments')
