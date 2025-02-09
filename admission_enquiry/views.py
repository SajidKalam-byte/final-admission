from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from .forms import AdmissionEnquiryForm, AdmissionFormForm, PaymentForm
from django.contrib import messages
from .models import Counsellor, AdmissionEnquiry, AdmissionForm, Payment
from django.urls import reverse
from .models import AdmissionForm
from reportlab.pdfgen import canvas 
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import AdmissionForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.conf import settings
import os
from reportlab.lib.utils import ImageReader

def download_invoice(request, admission_form_id):  # Accept admission_form_id as an argument
    admission_form = get_object_or_404(AdmissionForm, id=admission_form_id)
    payment = get_object_or_404(Payment, admission_form=admission_form)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice_{admission_form.name}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Header
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, "XYZ Institute of Technology")
    p.setFont("Helvetica", 12)
    p.drawString(200, height - 70, "123, ABC Road, City, Country - 567890")
    p.drawString(200, height - 90, "Email: info@xyzinstitute.com | Phone: +91-1234567890")

    p.line(50, height - 100, width - 50, height - 100)

    # Invoice Title
    p.setFont("Helvetica-Bold", 14)
    p.drawString(250, height - 130, "Fee Payment Invoice")

    # Invoice Details
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 160, f"Invoice No: INV-{payment.id}")
    p.drawString(50, height - 180, f"Student Name: {admission_form.name}")
    p.drawString(50, height - 200, f"Course: {admission_form.course_preferred.name}")
    p.drawString(50, height - 200, f"Transaction ID: {payment.transaction_id}")
    p.drawString(50, height - 220, f"Payment Date: {payment.date.strftime('%d-%m-%Y')}")
    p.drawString(50, height - 240, f"Payment Method: {payment.get_payment_mode_display()}")
    p.drawString(50, height - 260, f"Amount Paid: Rs. {payment.amount}")

    # Footer
    p.line(50, 100, width - 50, 100)
    p.drawString(50, 80, "Authorized Signatory")
    p.drawString(50, 60, "XYZ Institute of Technology")

    p.showPage()
    p.save()
    return response



def download_allotment_letter(request):
    admission_form_id = request.GET.get('admission_form_id')
    if not admission_form_id:
        return HttpResponse("Missing 'admission_form_id' parameter.", status=400)

    admission_form = get_object_or_404(AdmissionForm, id=admission_form_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Allotment_Letter_{admission_form.name}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Header
    p.setFont("Helvetica-Bold", 16)
    p.drawString(150, height - 50, "XYZ Institute of Technology")
    p.setFont("Helvetica", 12)
    p.drawString(150, height - 70, "123, ABC Road, City, Country - 567890")
    p.drawString(150, height - 90, "Email: info@xyzinstitute.com | Phone: +91-1234567890")

    p.line(50, height - 100, width - 50, height - 100)

    # Title
    p.setFont("Helvetica-Bold", 14)
    p.drawString(220, height - 130, "Admission Allotment Letter")

    # Student Details Table
    data = [
        ["Student Name:", admission_form.name],
        ["Parent's Name:", admission_form.parent_name],
        ["Phone Number:", admission_form.phone_number],
        ["Aadhar Number:", admission_form.aadhar_number],
        ["Last Qualification:", admission_form.last_qualification],
        ["Course Opted:", admission_form.course_preferred],  # Replace if available
    ]

    table = Table(data, colWidths=[200, 250])
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    table.wrapOn(p, width, height)
    table.drawOn(p, 50, height - 300)

    # Add Images if available
    y_position = height - 370  # Adjust based on table position

    if admission_form.passport_photo:
        passport_path = os.path.join(settings.MEDIA_ROOT, str(admission_form.passport_photo))
        if os.path.exists(passport_path):
            p.drawString(50, y_position, "Passport Photo:")
            p.drawImage(ImageReader(passport_path), 50, y_position - 70, width=100, height=100)
            y_position -= 120  # Move down for next content

    if admission_form.signature:
        signature_path = os.path.join(settings.MEDIA_ROOT, str(admission_form.signature))
        if os.path.exists(signature_path):
            p.drawString(50, y_position, "Signature:")
            p.drawImage(ImageReader(signature_path), 50, y_position - 70, width=100, height=50)

    # Footer
    p.line(50, 100, width - 50, 100)
    p.drawString(50, 80, "Authorized Signatory")
    p.drawString(50, 60, "XYZ Institute of Technology")

    p.showPage()
    p.save()
    return response


def assign_counsellor():
    try:
        counsellors = Counsellor.objects.order_by('assigned_students')
        if counsellors.exists():
            selected = counsellors.first()
            selected.assigned_students += 1
            selected.save()
            return selected
        return None
    except Exception as e:
        print(f"Error assigning counsellor: {e}")
        return None

def enquiry_form(request):
    if request.method == 'POST':
        form = AdmissionEnquiryForm(request.POST)
        if form.is_valid():
            try:
                enquiry = form.save(commit=False)
                counsellor = assign_counsellor()
                if counsellor:
                    enquiry.assigned_counsellor = counsellor
                enquiry.save()
                return render(request, 'admission_enquiry/assigned_counsellor.html', {'counsellor': counsellor})
            except Exception as e:
                print(f"Error saving enquiry: {e}")
                messages.error(request, "Error saving your enquiry. Please try again.")
        else:
            print("Form is invalid")
            print(form.errors)
    else:
        form = AdmissionEnquiryForm()
    return render(request, 'admission_enquiry/enquiry_form.html', {'form': form})

def admission_form(request):
    if request.method == 'POST':
        form = AdmissionFormForm(request.POST, request.FILES)
        if form.is_valid():
            admission_form = form.save()
            return redirect(f"/payment/?admission_form_id={admission_form.id}")
        else:
            print("Form errors:", form.errors)  # Debugging line
    else:
        form = AdmissionFormForm()
    return render(request, 'admission_enquiry/admission_form.html', {'form': form})


def payment(request):
    admission_form_id = request.GET.get('admission_form_id')
    if not admission_form_id:
        return HttpResponseBadRequest("Missing 'admission_form_id' parameter.")

    admission_form = get_object_or_404(AdmissionForm, id=admission_form_id)
    course_fee = admission_form.course_preferred.fee if admission_form.course_preferred else 0

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.admission_form = admission_form
            payment.amount = course_fee  # Ensure the correct amount is used
            payment.save()
            return redirect(reverse('final_step') + f'?admission_form_id={admission_form.id}')
    else:
        form = PaymentForm(initial={'amount': course_fee})  # Pre-fill amount

    return render(request, 'admission_enquiry/payment.html', {'form': form, 'admission_form': admission_form})

def final_step(request):
    admission_form_id = request.GET.get('admission_form_id')
    if not admission_form_id:
        return HttpResponseBadRequest("Missing 'admission_form_id' parameter.")

    admission_form = get_object_or_404(AdmissionForm, id=admission_form_id)
    payment = get_object_or_404(Payment, admission_form=admission_form)

    return render(request, 'admission_enquiry/final_step.html', {
        'admission_form': admission_form,
        'payment': payment
    })


