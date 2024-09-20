from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib import auth
from eh_admin.models import *
from django.contrib import messages
from patient.models import AppointmentBook,Appointment,PatientRegistration,CheckPatient
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage
def register(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Registered Successfully')
            return redirect('doctor-login')
              
        else:
            form = DoctorRegistrationForm()
            messages.error(request,'Some error occur')
            return redirect('doctor-register')
            
    else:
        form = DoctorRegistrationForm()
    return render(request,'doctor/register.html',{'form':form})

def login_doctor(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'Successfully Logged')
            return redirect('doctor-home')
        else:
            return redirect('doctor-login')
        messages.error(request,'Invalid Credential')
    return render(request,'doctor/login.html')
@login_required(login_url='doctor-login')
def home(request):

    return render(request,'doctor/components/home.html')
@login_required(login_url='doctor-login')
def getAllPatients(request):
    appointmentBook = AppointmentBook.objects.filter(doctor_id__user_id=request.user)
    
    patients  = []
    for ab in appointmentBook:
        patient = Appointment.objects.filter(token=ab.token).first()
        patients.append(patient)
    print(patients)
    paginator = Paginator(appointmentBook,4)
    page_number= request.GET.get('page')
    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page=paginator.page(page_number.num_pages)

    

           


    

    return render(request,'doctor/components/patient.html',{'patients':patients,'page':page})
def logout_doctor(request):
    logout(request)
    return redirect('doctor-login') 
@login_required(login_url='doctor-login')
def checkPatient(request,patient_id):
    appointment=Appointment.objects.all()
    scanners = Scanners.objects.all()
    print(request.user.id)
    user_detail = PatientRegistration.objects.get(user=patient_id)
    doc_detail = CreateDoctor.objects.get(user=request.user.id)
    print(doc_detail)
    appointment = Appointment.objects.filter(user=patient_id).first()
    print(appointment)
    # appointmentf=Appointment.objects.filter(user=patient_id)
    # print(appointmentf)
    # for i in appointment:
    #     if i.user.id == patient_id: 
    #         res=Appointment.objects.get(token=i.token)
            
    # user=PatientRegistration.objects.get(id=patient_id)
    # age=user.age
    # patient = PatientRegistration.objects.get(id=patient_id)
    if request.method == 'POST':
        
        name = request.POST['name']
        token = request.POST['token']
        diagnose =request.POST['diagnose']
        description = request.POST['description']
        amount = request.POST['amount']
        scanners = request.POST.getlist('scanner_ids')
        visited_date = request.POST['visited_date']
        next_date = request.POST['next_date']        
        
        checked_patient = CheckPatient.objects.create(patient=user_detail,doctor=doc_detail,token=token,visited_date=visited_date,next_date=next_date,diagnose=diagnose,
                                                      description=description,is_checked=True,amount=amount)
        appointment1=Appointment.objects.filter(user=patient_id,token=token).update(is_checked=True)
        print(appointment.is_checked)
        checked_patient.scanner.set(scanners)
        print(checked_patient.scanner)
        return redirect('doctor-home')
    return render(request,'doctor/components/detail.html',{'scanners':scanners,'appointment':appointment,'user_detail':user_detail})
@login_required(login_url='doctor-login')
def getAllCheckedPatients(request):
    doctor_detail=CreateDoctor.objects.get(user=request.user.id)
    checkedPatients = CheckPatient.objects.filter(is_checked=True,doctor=doctor_detail)
    print(checkedPatients)
    paginator = Paginator(checkedPatients,4)
    page_number= request.GET.get('page')
    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page=paginator.page(page_number.num_pages)
    return render(request,'doctor/components/checked_patients.html',{'checkedpatients':checkedPatients,'page':page})

