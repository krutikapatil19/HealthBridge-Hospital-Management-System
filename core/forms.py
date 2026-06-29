from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import BedBooking, Appointment, Doctor, Department


# ── Auth Forms ──────────────────────────────────────────────

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=50, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    phone = forms.CharField(
        max_length=15, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit mobile number'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Create password'}
        )
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirm password'}
        )
        for field in self.fields.values():
            field.help_text = None

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'autofocus': True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )


# ── Booking Forms ────────────────────────────────────────────

class BedBookingForm(forms.ModelForm):
    class Meta:
        model = BedBooking
        exclude = ['booking_id', 'user', 'hospital', 'status', 'created_at', 'updated_at',
                   'admin_notes', 'payment_method', 'payment_status', 'amount_paid']
        widgets = {
            'patient_name':               forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'patient_age':                forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 120}),
            'patient_gender':             forms.Select(attrs={'class': 'form-select'}),
            'patient_phone':              forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit mobile'}),
            'patient_email':              forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Optional'}),
            'patient_address':            forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'aadhar_number':              forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12-digit (optional)'}),
            'medical_condition':          forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'bed_type':                   forms.Select(attrs={'class': 'form-select'}),
            'admission_date':             forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expected_days':              forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'services_required':          forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'emergency_contact_name':     forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_phone':    forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_relation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Spouse, Parent'}),
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ['appointment_id', 'user', 'hospital', 'department', 'doctor', 'status',
                   'created_at', 'updated_at', 'admin_notes', 'payment_method',
                   'payment_status', 'amount_paid']
        widgets = {
            'patient_name':     forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'patient_age':      forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 120}),
            'patient_gender':   forms.Select(attrs={'class': 'form-select'}),
            'patient_phone':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit mobile'}),
            'patient_email':    forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Optional'}),
            'appointment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'reason_for_visit': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class PaymentForm(forms.Form):
    payment_method = forms.ChoiceField(
        choices=[
            ('UPI', 'UPI / GPay / PhonePe'),
            ('Card', 'Credit / Debit Card'),
            ('NetBanking', 'Net Banking'),
            ('Cash', 'Cash at Counter'),
        ],
        widget=forms.RadioSelect(attrs={'class': 'payment-radio'})
    )
