from django.db import models
from django.contrib.auth.models import User
from doctr_app.models import *
from eh_admin.models import *
# Create your models here.
class PatientRegistration(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    location = models.CharField(max_length=200)
    mobileNo=models.CharField(max_length=16)

    def __str__(self) -> str:
        return f'{self.user.username}'
# class DiseasePatients(models.Model):
#     name = models.CharField(max_length=200)
#     def __str__(self):
#         return f"{self.name}"
    
class Appointment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    disease = models.ForeignKey(Diseases,on_delete=models.CASCADE)
    appoint_date=models.DateField()
    
    token=models.CharField(max_length=180,default='')
    is_confirm=models.BooleanField(default=False)
    is_checked = models.BooleanField(default=False)
    def __str__(self) -> str:
        return f'{self.user}'
class AppointmentBook(models.Model):
    appointment=models.ForeignKey(Appointment,on_delete=models.CASCADE)
    token=models.CharField(max_length=200)
    doctor=models.ForeignKey(CreateDoctor,on_delete=models.CASCADE)
class CheckPatient(models.Model):
    doctor = models.ForeignKey(CreateDoctor,on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientRegistration,on_delete=models.CASCADE)
    token = models.CharField(max_length=200)
    diagnose = models.CharField(max_length=200)
    description = models.TextField()
    visited_date = models.DateField()
    next_date = models.DateField()
    scanner = models.ManyToManyField(Scanners)
    amount = models.DecimalField(max_digits=8,decimal_places=2)
    is_checked=models.BooleanField(default=False)
    total_amnt = models.DecimalField(default=0,max_digits=8,decimal_places=2)
    def __str__(self) -> str:
        return f'{self.patient}'
class PatientInsurance(models.Model):
    patient = models.ForeignKey(PatientRegistration,on_delete=models.CASCADE)
    member_id = models.CharField(max_length=200,unique=True)
    member_name = models.CharField(max_length=200)
    ins_brand = models.ForeignKey(InsuraceBrand,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=5,decimal_places=2,default=0.00)
    is_verify = models.BooleanField(default=False)
    def __str__(self) -> str:
        return f"{self.ins_brand}"