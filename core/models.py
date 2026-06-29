from django.db import models
from django.contrib.auth.models import User
import uuid


PUNE_AREAS = [
    ('Shivajinagar', 'Shivajinagar'),
    ('Kothrud', 'Kothrud'),
    ('Hadapsar', 'Hadapsar'),
    ('Pimpri-Chinchwad', 'Pimpri-Chinchwad'),
    ('Wakad', 'Wakad'),
    ('Baner', 'Baner'),
    ('Aundh', 'Aundh'),
    ('Viman Nagar', 'Viman Nagar'),
    ('Koregaon Park', 'Koregaon Park'),
    ('Deccan', 'Deccan'),
    ('Kalyani Nagar', 'Kalyani Nagar'),
    ('Magarpatta', 'Magarpatta'),
    ('Swargate', 'Swargate'),
    ('Camp', 'Camp'),
    ('Nigdi', 'Nigdi'),
]

DEPARTMENTS = [
    ('Cardiology', 'Cardiology'),
    ('Neurology', 'Neurology'),
    ('Orthopedics', 'Orthopedics'),
    ('Pediatrics', 'Pediatrics'),
    ('Gynecology', 'Gynecology'),
    ('General Medicine', 'General Medicine'),
    ('Emergency', 'Emergency'),
    ('Oncology', 'Oncology'),
    ('Dermatology', 'Dermatology'),
    ('ENT', 'ENT'),
    ('Ophthalmology', 'Ophthalmology'),
    ('Psychiatry', 'Psychiatry'),
    ('Urology', 'Urology'),
    ('Gastroenterology', 'Gastroenterology'),
]

BED_TYPES = [
    ('General', 'General Ward'),
    ('Semi-Private', 'Semi-Private'),
    ('Private', 'Private Room'),
    ('ICU', 'ICU'),
    ('NICU', 'NICU'),
]

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Cancelled', 'Cancelled'),
    ('Completed', 'Completed'),
]

PAYMENT_METHODS = [
    ('UPI', 'UPI / GPay / PhonePe'),
    ('Card', 'Credit / Debit Card'),
    ('NetBanking', 'Net Banking'),
    ('Cash', 'Cash at Counter'),
]


class Hospital(models.Model):
    name = models.CharField(max_length=200)
    area = models.CharField(max_length=100, choices=PUNE_AREAS)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="hospital_photos/", blank=True, null=True)
    image_url = models.URLField(blank=True, help_text="External image URL fallback")
    total_beds = models.PositiveIntegerField(default=0)
    available_beds = models.PositiveIntegerField(default=0)
    icu_beds = models.PositiveIntegerField(default=0)
    available_icu_beds = models.PositiveIntegerField(default=0)
    emergency = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.0)
    established_year = models.PositiveIntegerField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.area}"

    def occupied_beds(self):
        return self.total_beds - self.available_beds

    class Meta:
        ordering = ['name']


class Department(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=100, choices=DEPARTMENTS)

    def __str__(self):
        return f"{self.name} - {self.hospital.name}"

    class Meta:
        unique_together = ('hospital', 'name')


class Doctor(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='doctors')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='doctors')
    name = models.CharField(max_length=200)
    qualification = models.CharField(max_length=200, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    available_days = models.CharField(max_length=200, default='Mon-Sat')
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=500.00)

    def __str__(self):
        return f"Dr. {self.name} - {self.department.name}"


class BedBooking(models.Model):
    booking_id = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='bed_bookings')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='bed_bookings')

    # Patient details
    patient_name = models.CharField(max_length=200)
    patient_age = models.PositiveIntegerField()
    patient_gender = models.CharField(max_length=10, choices=[('Male','Male'),('Female','Female'),('Other','Other')])
    patient_phone = models.CharField(max_length=15)
    patient_email = models.EmailField(blank=True)
    patient_address = models.TextField()
    aadhar_number = models.CharField(max_length=12, blank=True)

    # Medical details
    medical_condition = models.TextField()
    bed_type = models.CharField(max_length=20, choices=BED_TYPES, default='General')
    admission_date = models.DateField()
    expected_days = models.PositiveIntegerField(default=1)
    services_required = models.TextField(blank=True)

    # Emergency contact
    emergency_contact_name = models.CharField(max_length=200)
    emergency_contact_phone = models.CharField(max_length=15)
    emergency_contact_relation = models.CharField(max_length=50)

    # Payment
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    payment_status = models.CharField(max_length=20, default='Paid')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = 'BED' + str(uuid.uuid4()).upper()[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_id} - {self.patient_name}"

    class Meta:
        ordering = ['-created_at']


class Appointment(models.Model):
    appointment_id = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='appointments')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)

    # Patient details
    patient_name = models.CharField(max_length=200)
    patient_age = models.PositiveIntegerField()
    patient_gender = models.CharField(max_length=10, choices=[('Male','Male'),('Female','Female'),('Other','Other')])
    patient_phone = models.CharField(max_length=15)
    patient_email = models.EmailField(blank=True)

    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason_for_visit = models.TextField()

    # Payment
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=300.00)
    payment_status = models.CharField(max_length=20, default='Paid')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.appointment_id:
            self.appointment_id = 'APT' + str(uuid.uuid4()).upper()[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.appointment_id} - {self.patient_name}"

    class Meta:
        ordering = ['-created_at']


class UserProfile(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"Profile: {self.user.username}"
