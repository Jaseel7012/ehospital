from django.db import models

from doctr_app.models  import CreateDoctor
# Create your models here.
class Diseases(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return f"{self.name}"
    
class Scanners(models.Model):
    name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=5,decimal_places=2)
    def __str__(self) -> str:
        return f'{self.name}'
    
class HealthTips(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    prevention_tips = models.TextField()
    def __str__(self) -> str:
        return f'{self.title}'
class InsuraceBrand(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self) -> str:
        return f'{self.name}'


    