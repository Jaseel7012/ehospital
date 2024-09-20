from django import forms
from django.contrib.auth.forms import UserCreationForm 
from .models import *

class DoctorRegistrationForm(UserCreationForm):
    username=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    specialization = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
    start_time = forms.TimeField(label='Starting Time',widget=forms.TimeInput(attrs={
        'type' : 'time',
        'class':'form-control'
    }),input_formats=['%H:%M'])
    avatar=forms.ImageField()
    end_time = forms.TimeField(label='End Time',widget=forms.TimeInput(attrs={
        'type' : 'time',
        'class':'form-control'
    }),input_formats=['%H:%M'])
    class Meta:
        model = User
        fields = ['username','password1','password2','specialization','avatar','start_time','end_time']
    
    def save(self,commit=True):
        user=super().save(commit=False)
        if commit:
            user.save()
            doctor = CreateDoctor(user=user,specialization=self.cleaned_data['specialization']
                                  ,start_time=self.cleaned_data['start_time'], end_time=self.cleaned_data['end_time'] ,avatar=self.cleaned_data['avatar']     )
            doctor.save()
        return user
