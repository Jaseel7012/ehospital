from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import PatientRegistrationForm
from django.contrib import auth
from django.contrib.auth import login,logout,authenticate
from .models import *
from eh_admin.models import Diseases
from django.contrib import messages
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage
# Create your views here.
def createPatient(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registered successfully')
            return redirect('patient-login')
        else:
            form = PatientRegistrationForm()
            messages.error(request,'Try again..')

    else:       
         form = PatientRegistrationForm()
    return render(request,'patient/register.html',{'form':form})
def patientLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            if username == 'admin' and password == '1234':
                login(request,user)
                return redirect('all-appoints')
            else:
                login(request,user)
                messages.success(request,'Logged Successfully')
                return redirect('index')
        else:
            messages.info(request,'Invalid Credential')
            return redirect('patient-login')
    return render(request,'patient/login.html')
@login_required(login_url='patient-login')
def index(request):
    context={
        'username' : request.user.username
    }
    return render(request,'patient/index.html',context=context)
@login_required(login_url='patient-login')
def appointmentCreate(request):
    disease=Diseases.objects.all()
    context={
        'username' : request.user.username,
        'diseases':disease
        
        }
    if request.method == 'POST':
        user = request.user
        disease = request.POST.get('disease')
        appoint_date = request.POST['appoint_date']
        
        disease = Diseases.objects.get(id=disease)

        appoint = Appointment.objects.create(user=user,disease=disease,appoint_date=appoint_date,is_confirm=False)
        
        return redirect('index')
    
    return render(request,'patient/appoinment.html',context=context)
@login_required(login_url='patient-login')
def appointmentList(request):
    appointments = Appointment.objects.filter(user=request.user)
    paginator = Paginator(appointments,6)
    page_number= request.GET.get('page')
    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page=paginator.page(page_number.num_pages)
    context={
        'appointments':appointments,
        'page':page
    }
    return render(request,'patient/my_appointment.html',context=context)
@login_required(login_url='patient-login')
def deleteAppointment(request,appoint_id):
    appoint = Appointment.objects.get(id=appoint_id)
    if request.method == 'POST':
        appoint.delete()
        return redirect('my-appoints')
    return render(request,'patient/cancel.html')
@login_required(login_url='patient-login')
def getAllHealthTips(request):
    healthTips = HealthTips.objects.all()
    return render(request,'patient/tips.html',{'healthTips':healthTips})
@login_required(login_url='patient-login')
def diseaseCreate(request):
    if  request.method == 'POST':
        name = request.POST['name']
        disease=Diseases.objects.create(name=name)
        return redirect('make-appointment')
    
    return render(request,'patient/disease.html')
@login_required(login_url='patient-login')
def bookingDetail(request,appoint_id):
    appointment=Appointment.objects.get(id=appoint_id)
    book = AppointmentBook.objects.get(token=appointment.token)
    
    context = {
        
        'appointment' : appointment,
        'doctor':book.doctor
    }
    
    return render(request,'patient/book_detail.html',context)
@login_required(login_url='patient-login')
def getMedicalRecord(request):
    patient = PatientRegistration.objects.get(user=request.user.id)
    my_records = CheckPatient.objects.filter(patient=patient)
    print(my_records)
    total =0
    testers = [records.scanner.all() for records in my_records]
    details = [records for records in my_records]
    total = sum([item.amount for  item in my_records ])
    print(details)
    res=[]
    for test_obj in testers:
        for n in test_obj:
            total += n.amount
            res.append({'name':n.name ,'price' : n.amount})
    
        
    print(res)
    tot_amnt =  CheckPatient.objects.filter(patient=patient).update(total_amnt=total)
    return render(request,'patient/medical_record.html',{'res':res,'details':details,'total':total})

@login_required(login_url='patient-login')
def getMedicalHistory(request):
    patient = PatientRegistration.objects.get(user=request.user.id)
    my_records = CheckPatient.objects.filter(patient=patient)
    return render(request,'patient/medical_history.html',{'my_records':my_records})
@login_required(login_url='patient-login')
def addInsurance(request):
    insurances=InsuraceBrand.objects.all()
    if request.method == 'POST':
        user_id= request.user.id
        user=PatientRegistration.objects.get(user=user_id)
        member_id = request.POST['member_id']
        member_name=request.POST['member_name']
        ins_brand_id=request.POST['ins_brand']
        ins_brand = InsuraceBrand.objects.get(id=ins_brand_id)

        insurancePatients = PatientInsurance.objects.create(patient=user,member_id=member_id,
                                                            member_name=member_name,ins_brand=ins_brand)
        return redirect('index')
    return render(request,'patient/insurance_create.html',{'user':request.user,'insurances':insurances})
@login_required(login_url='patient-login')
def useInsurance(request):
    user = request.user.id
    patient = PatientRegistration.objects.get(user=user)
    patientInsurance=PatientInsurance.objects.filter(patient=patient)
    checkpatient =CheckPatient.objects.filter(patient=patient)
    total =0
    amount =0
    for i in checkpatient:
        total+=i.amount
    print(patientInsurance,total)
    for ins in patientInsurance:
        if  (ins.ins_brand.name).lower() == 'humana':
            amount = float(total) - ((50.00/100.00)*float(total))
    patientInsurance.update(amount=amount)
    print(amount)
    return render(request,'patient/use_insurance.html',{'amount':amount,'insurances':patientInsurance})

#payment
@login_required(login_url='patient-login')
def checkout_session_create(request):
    patient = PatientRegistration.objects.get(user=request.user.id)

    patientInsurance = PatientInsurance.objects.filter(patient=patient)
    if patientInsurance:
        stripe.api_key=settings.STRIPE_SECRET_KEY
        if request.method == 'POST':
            line_items = []
            for item in  patientInsurance:
                if item:
                    line_item ={
                        'price_data':{
                            'currency' : 'INR',
                            'unit_amount':int(item.amount*100),
                            'product_data':{
                                'name':'Doctor Fee'
                            }
                        },
                        'quantity':1
                    }
                    line_items.append(line_item)
            if line_items:
                checkout_session = stripe.checkout.Session.create(
                payment_method_types= ['card'],
                line_items=line_items,
                mode='payment',
                success_url=request.build_absolute_uri(reverse('success')),
                cancel_url=request.build_absolute_uri(reverse('cancel')),
                )
                return redirect(checkout_session.url,code=303)
@login_required(login_url='patient-login')
def success(request):
    patient = PatientRegistration.objects.get(user=request.user.id)
    medicalRecord =CheckPatient.objects.filter(patient=patient)
    medicalRecord.update(amount=0,total_amnt =0)
    patientInsurance = PatientInsurance.objects.filter(patient=patient,is_verify=True)
    patientInsurance.delete()
    return render(request,'patient/success.html')
@login_required(login_url='patient-login')
def cancel(request):
    return render(request,'patient/cancel_payment.html')
def logout_patient(request):
    logout(request)
    return redirect('patient-login')
    
