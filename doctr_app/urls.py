from django.urls import path
from .views import *
urlpatterns = [

    path('',register,name='doctor-register'),
    path('login/',login_doctor,name='doctor-login'),
    path('home/',home,name='doctor-home'),
    path('doc-logout/',logout_doctor,name='logout-doctor'),
    path('all-patients/',getAllPatients,name='all-patients'),
    path('check-patient/<int:patient_id>',checkPatient,name='check-now'),
    path('checked-patients/',getAllCheckedPatients,name='all-checked-patients')
    ]