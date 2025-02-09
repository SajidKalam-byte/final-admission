from django import forms
from .models import AdmissionEnquiry, AdmissionForm, Payment, Course

class AdmissionEnquiryForm(forms.ModelForm):
    class Meta:
        model = AdmissionEnquiry
        fields = ['name', 'parent_name', 'phone_number', 'course_preferred_1', 'course_preferred_2', 'course_preferred_3', 'reference_source']

class AdmissionFormForm(forms.ModelForm):
    course_preferred = forms.ModelChoiceField(
        queryset=Course.objects.all(), empty_label="Select a Course"
    )  # Fetch courses from DB

    class Meta:
        model = AdmissionForm
        fields = ['name', 'parent_name', 'phone_number', 'course_preferred', 'last_qualification', 'aadhar_number', 'documents', 'passport_photo', 'signature']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_mode', 'transaction_id', 'payee_name']