from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    date_of_birth=models.DateTimeField(verbose_name="تاریخ تولد", blank=True, null=True)
    bio=models.TextField(verbose_name=" بایو ", blank=True, null=True )
    photo=models.ImageField(verbose_name="تصاویر",upload_to="account_images/",null=True, blank=True)
    job=models.CharField(max_length=250,verbose_name="شغل", blank=True, null=True)
    phone=models.CharField(verbose_name="شماره تلفن",max_length=11, blank=True, null=True)

