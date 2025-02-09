from django.db import models
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    valid_extensions = ['.pdf', '.docx', '.jpg', '.jpeg', '.png']
    if not any(value.name.lower().endswith(ext) for ext in valid_extensions):
        raise ValidationError("Only .pdf, .docx, .jpg, .jpeg, and .png files are allowed.")


class Counsellor(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=254, unique=True, null=True)
    contact_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    assigned_students = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class AdmissionEnquiry(models.Model):
    name = models.CharField(max_length=100)
    parent_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    course_preferred_1 = models.CharField(max_length=50)
    course_preferred_2 = models.CharField(max_length=50, blank=True, null=True)
    course_preferred_3 = models.CharField(max_length=50, blank=True, null=True)
    reference_source = models.CharField(max_length=50)
    assigned_counsellor = models.ForeignKey(Counsellor, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100, unique=True)
    fee = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class AdmissionForm(models.Model):
    name = models.CharField(max_length=100)
    parent_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    course_preferred = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    last_qualification = models.CharField(max_length=100)
    aadhar_number = models.CharField(max_length=12)
    documents = models.FileField(upload_to='supporting_documents/')
    passport_photo = models.ImageField(upload_to='passport_photos/', null=True, blank=True)
    signature = models.ImageField(upload_to='signatures/', null=True, blank=True)


    def __str__(self):
        return self.name

class Payment(models.Model):
    admission_form = models.OneToOneField(AdmissionForm, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=50, choices=[
        ('offline', 'OFFLINE'),
        ('debit_card', 'Debit Card'),
        ('upi', 'UPI'),
        ('net_banking', 'Net Banking'),
    ])
    transaction_id = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    payee_name = models.CharField(max_length=100)

    def __str__(self):
        return f"Payment for {self.admission_form.name}"

# PAYMENT_CHOICES = [
#     ('offline', 'OFFLINE'),
#     ('debit_card', 'Debit Card'),
#     ('upi', 'UPI'),
#     ('net_banking', 'Net Banking'),
# ]

# class Payment(models.Model):
#     admission_form = models.OneToOneField(AdmissionForm, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_mode = models.CharField(max_length=50, choices=PAYMENT_CHOICES)
#     transaction_id = models.CharField(max_length=50, blank=True, null=True)
#     date = models.DateField(auto_now_add=True)
#     payee_name = models.CharField(max_length=100)

#     def __str__(self):
#       return f"Payment for {self.admission_form.name}"