from .models import Scanners
from django import forms
from .models import *

class ScannerCreateForms(forms.ModelForm):
    name=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
    amount = forms.DecimalField(decimal_places=2,max_digits=6,widget=forms.NumberInput(attrs={'class':'form-control'}))

    class Meta:
        model = Scanners
        fields = '__all__'
class  HealthTipsForm(forms.ModelForm):
    title=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(max_length=800,widget=forms.Textarea(attrs={'class':'form-control'}))
    prevention_tips=forms.CharField(max_length=400,widget=forms.Textarea(attrs={'class':'form-control'}))
    class Meta:
        model = HealthTips
        fields = '__all__'
class InsuranceBrandForm(forms.ModelForm):
    name =forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = InsuraceBrand
        fields = '__all__'  