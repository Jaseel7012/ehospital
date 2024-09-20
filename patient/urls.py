from django.urls import path
from .views import *
urlpatterns = [
   
    path('',createPatient,name='register'),
    path('login/',patientLogin,name='patient-login'),
    path('index/',index,name='index'),
    path('appointment/',appointmentCreate,name='make-appointment'),
    path('my-appoints/',appointmentList,name='my-appoints'),
    path('cancel/<int:appoint_id>',deleteAppointment,name='cancel'),
    path('add-disease',diseaseCreate,name='disease-add'),
    path('view-more/<int:appoint_id>',bookingDetail,name='detail-more'),
    path('medical-records/',getMedicalRecord,name='medical-records'),
        path('health-tips/',getAllHealthTips,name='all-health-tips'),
    path('medical-history/',getMedicalHistory,name='medical-history'),
    path('apply-insurance/',addInsurance,name='add-insurance'),
    path('use-insurance/',useInsurance,name='use-insurance'),
    path('checkout-session/',checkout_session_create,name='checkout-session-create'),
    path('success/',success,name='success'),
    path('cancel/',cancel,name='cancel'),
    path('patient-logout/',logout_patient,name='patient-logout')
]