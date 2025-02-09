from django.contrib import admin
from .models import Counsellor, AdmissionEnquiry,AdmissionForm, Payment, Course

class CounsellorAdmin(admin.ModelAdmin):
    list_display = ['name', 'assigned_students']  # Removed 'email' as it does not exist

class AdmissionEnquiryAdmin(admin.ModelAdmin):
    search_fields = ['name', 'phone_number', 'assigned_counsellor__name']
    list_filter = ['course_preferred_1', 'reference_source']

default_course = Course.objects.filter(name="MCA").first()
if default_course:
    AdmissionForm.objects.filter(course_preferred__isnull=True).update(course_preferred=default_course)

admin.site.register(Counsellor, CounsellorAdmin)
admin.site.register(AdmissionEnquiry, AdmissionEnquiryAdmin)
admin.site.register(Course)
admin.site.register(AdmissionForm)
admin.site.register(Payment)
