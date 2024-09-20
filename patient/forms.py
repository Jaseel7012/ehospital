from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms

class PatientRegistrationForm(UserCreationForm):
    username=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
    age = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
    location= forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
    mobileNo= forms.CharField(max_length=16,widget=forms.TextInput(attrs={'class':'form-control'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username','mobileNo','age','location','password1','password2']
        
    def save(self,commit=True):
        user=super().save(commit=False)
        if commit:
            user.save()
            patient = PatientRegistration(user=user,age=self.cleaned_data['age'],
                                          location=self.cleaned_data['location'],
                                          mobileNo=self.cleaned_data['mobileNo'])
            patient.save()
        return user

