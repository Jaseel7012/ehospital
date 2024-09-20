from django.urls import path
from .views import *
urlpatterns = [
    path('all-appoints/', allAppoints,name='all-appoints'),
    path('home/',allPatient,name='all-patient'),
    path('book-appointment/<int:appoint_id>',bookingAppointment,name='book-appointment'),
    path('create-scanner/',createScanner,name='create-scanner'),
    path('create-health-tips/',createHealthTips,name='health-tips'),
    path('insurance-create/', insuranceBrandAdd,name='insurance-brand'),
    path('request-insurance/',allInsurances,name='insurance-request'),
    path('detail-insurance/<int:ins_id>',detailInsurance,name = 'insurance-detail'),
    path('all-doctors/',allDoctors,name='all-doctors')
    ]