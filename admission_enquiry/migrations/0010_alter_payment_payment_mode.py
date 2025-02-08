# Generated by Django 5.1.1 on 2025-02-08 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admission_enquiry', '0009_auto_20250208_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_mode',
            field=models.CharField(choices=[('credit_card', 'Credit Card'), ('debit_card', 'Debit Card'), ('upi', 'UPI'), ('net_banking', 'Net Banking')], max_length=50),
        ),
    ]
