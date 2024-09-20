from django.db import models

# Create your models here.
from django.contrib.auth.models import User


# Create your models here.

class CreateDoctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    specialization=models.CharField(max_length=200)
    avatar = models.ImageField(upload_to='avatar_media')
    start_time = models.TimeField()
    end_time = models.TimeField()
    def __str__(self) -> str:
        return f'{self.user.username} - {self.specialization}'


# Create your models here.

