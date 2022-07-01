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

# Below are the temporary ables for Graphical Visual Data

class ClientSummaryCount(models.Model):
    client_name = models.CharField(max_length=200)
    no_of_matters = models.PositiveIntegerField(blank=True, null=True)

class CaseTypeSummary(models.Model):
    casetype = models.CharField(max_length=60)
    no_of_matters = models.PositiveIntegerField(blank=True, null=True)

class CaseTypeSummary_Month(models.Model):
    casetype = models.CharField(max_length=60)
    no_of_matters = models.PositiveIntegerField(blank=True, null=True)

class LawyerSummary(models.Model):
    Lawyer = models.CharField(max_length=5)
    no_of_matters = models.PositiveIntegerField(blank=True, null=True)

