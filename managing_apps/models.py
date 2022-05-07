from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, PositiveIntegerField
from adminapps.models import Lawyer_Data


# Create your models here.
APPTYPE = (
    ('INV','Invention'),
    ('UM','Utility Model'),
    ('DS','Design'),
    ('TM','Trademark'),
    ('PCT','PCT'),
)
class AppType(models.Model):
    applicationtype = CharField(max_length=10, choices = APPTYPE)
    number = PositiveIntegerField()

    def __str__(self):
        return f'{self.applicationtype} - {self.number}'

class LawyersCases(models.Model):
    lawyer = models.ForeignKey(Lawyer_Data, on_delete=CASCADE, null=True)
    noofcases = models.PositiveIntegerField()
    