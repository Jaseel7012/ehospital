from django.shortcuts import render,redirect
from patient.models import *
from .models import *
from .forms import *
from django.core.paginator import Paginator,EmptyPage
from doctr_app.models import CreateDoctor
# Create your views here.
def allAppoints(request): 
    appoints = Appointment.objects.all()
    paginator = Paginator(appoints,6)
    page_number= request.GET.get('page')
    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page=paginator.page(page_number.num_pages)
    return render(request,'admin/all_appoints.html',{'appoints':appoints,'page':page})
def allPatient(request):
    patients = PatientRegistration.objects.all()
    paginator = Paginator(patients,6)
    page_number= request.GET.get('page')
    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page=paginator.page(page_number.num_pages)
    return render(request,'admin/patients.html',{'patients':patients,'page':page})
def allDoctors(request):
    doctors = CreateDoctor.objects.all()
    
        
    paginator=Paginator(doctors,5)
    page_number=request.GET.get('page')
    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page=paginator.page(page_number.num_pages)
    return render(request,'admin/doctors.html',{'doctors':doctors,'page':page})
def index(request):
    return render(request,'admin/index.html')

def bookingAppointment(request,appoint_id):
    appointment=Appointment.objects.get(id=appoint_id)
    doctors=CreateDoctor.objects.all()
    if request.method == 'POST':
        name=request.POST['name']
        appoint_date=request.POST['appoint_date']
        disease = request.POST['disease']
        doctor = request.POST['doctor']
        token=request.POST['token']
        
        appointment.appoint_date = appoint_date
        appointment.token = token
        appointment.is_confirm = True
        appointment=Appointment.objects.filter(id=appoint_id).update(appoint_date=appoint_date,token=token,is_confirm=True)
        
        doctor = CreateDoctor.objects.get(id=doctor)
        appointment_obj = Appointment.objects.get(id=appointment)
        
        appointmentBook=AppointmentBook.objects.create(appointment=appointment_obj,doctor=doctor,token=token)
        return redirect('all-appoints') 
    return render(request,'admin/book_appoints.html',{'appointment':appointment,'doctors':doctors})

def createScanner(request):
    if (request.method == 'POST'):
        form = ScannerCreateForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create-scanner')
    else:
        form = ScannerCreateForms()
     
    
    return render(request,'admin/scanners.html',{'form':form})

def createHealthTips(request):
    if request.method == 'POST':
        form = HealthTipsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all-patient')
    else:
        form = HealthTipsForm()
    return render(request,'admin/tips.html',{'forms':form})

def insuranceBrandAdd(request):
    if request.method == 'POST':
        form =InsuranceBrandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('insurance-brand')
    else :
        form =InsuranceBrandForm()
    return render(request,'admin/insurance_brand.html',{'form':form})
def allInsurances(request):
    insurances = PatientInsurance.objects.all()
    return render(request,'admin/insurance_list.html',{'insurances':insurances})

def detailInsurance(request,ins_id):
    insurance = PatientInsurance.objects.get(id=ins_id)
    if request.method == 'POST':
        insurance=PatientInsurance.objects.filter(id=ins_id).update(
            is_verify=True
        )
        return redirect('insurance-request')
    return render(request,'admin/detail_insurance.html',{'insurance':insurance})

