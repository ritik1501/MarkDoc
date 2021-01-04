from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Patient(models.Model):
    sno = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    user_type = models.CharField(max_length=10, default='user')

    def __str__(self):
        return self.first_name+" ..."

class Doctor(models.Model):
    sno = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    authority = models.CharField(max_length=20, default='no auth')
    specialization = models.CharField(max_length=50, default='heart')
    user_type = models.CharField(max_length=10, default='doctor')
    visible = models.CharField(max_length=10, default='False')

    def __str__(self):
        return self.first_name+" ..."

class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100) 
    message = models.CharField(max_length=100) 
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.name + " ..."

class Appointment(models.Model):
    sno = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    pat_name = models.CharField(max_length=100) 
    doc_name = models.CharField(max_length=100) 
    pat_email = models.CharField(max_length=100) 
    doc_email = models.CharField(max_length=100) 
    disease = models.CharField(max_length=100)
    meeting_link = models.CharField(max_length=100)
    status = models.CharField(max_length=25, default='pending')
    timing = models.DateTimeField(default=now)

    def __str__(self):
        return self.pat_name + " " + self.doc_name + " ..."