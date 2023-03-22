from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    firstname= models.CharField(max_length=20) 
    lastname= models.CharField(max_length=20)
    address = models.CharField(max_length=100)  
    age= models.PositiveSmallIntegerField()
    gender= models.CharField(max_length=10) 
    patientID= models.PositiveIntegerField()
    aadhaar= models.PositiveIntegerField()
    email = models.EmailField()


    def __str__(self):
        return f'{self.user.username} Profile'