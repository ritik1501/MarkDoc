from django.contrib import admin
from .models import Patient, Contact, Doctor, Appointment

# Register your models here.
admin.site.register((Patient, Contact, Doctor, Appointment))