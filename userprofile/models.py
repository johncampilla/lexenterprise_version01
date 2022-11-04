from multiprocessing.connection import Client
from tabnanny import verbose
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

RANK = (
    ('MANAGING PARTNER', 'MANAGING PARTNER'),
    ('PARTNER', 'PARTNER'),
    ('ASSOCIATES', 'ASSOCIATES'),
    ('SECRETARY', 'SECRETARY'),
    ('PARALEGAL', 'PARALEGAL'),
    ('MIS STAFF', 'MIS STAFF'),
    ('SYSTEM ADMIN', 'SYSTEM ADMIN'),
    ('ACCOUNTING STAFF', 'ACCOUNTING STAFF'),
    ('DATA ENCODER', 'DATA ENCODER'),
    ('FRONTEND DEVELOPER', 'FRONTEND DEVELOPER'),
    ('BACKEND DEVELOPER', 'BACKEND DEVELOPER'),
    ('SYSTEM DEVELOPER', 'SYSTEM DEVELOPER'),
    ('CLIENT', 'CLIENT'),

)


class User_Profile(models.Model):
    userid = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, null=True)
    rank = models.CharField(max_length=30, choices=RANK, null=True)
    access_code = models.CharField(max_length=5, null=True, blank=True)
    supporto = models.CharField(max_length=60, null=True, blank=True)
    mobile = models.CharField(max_length=60, null=True)
    image = models.ImageField(upload_to='Profile_Images/', blank=True)
    remarks = models.TextField(null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    date_acquired = models.DateField(null=True, blank=True)
    

    class Meta:
        verbose_name_plural = 'User Profile'

    def __str__(self):
        return f'{self.userid.username}'
    
# Create your models here.
