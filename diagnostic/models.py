from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse # Used to generate URLs by reversing the URL 

from django.contrib.auth.models import User
# Create your models here.

class Diagnose(models.Model):
    """Model representing a diagnose"""
    name = models.CharField(max_length=200, help_text='Enter the diagnose based on provided symptoms')

    class Meta:
        permissions = (("can_create_diagnoses", "Create diagnose"),)

    def __str__(self):
        """String for representing the Model object."""
        return self.name
    
    def get_absolute_url(self):
        """Returns the url to duagnose list."""
        return reverse('diagnoses')

class Record(models.Model):
    """Model representing a Diagnostic Record"""
    title = models.CharField(max_length=200)

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE, 
        null=False, 
        blank=False,
        limit_choices_to={'groups__name': 'Patients'},
        related_name='patients'
        )
    doctor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'groups__name': 'Doctors'},
        related_name='doctors'
        )

    symptoms = models.TextField(max_length=1000, help_text='Enter a brief description of the symptoms')
    diagnose = models.ForeignKey(Diagnose, on_delete=models.SET_NULL, null=True, help_text='Select a diagnose')

    permissions = (("can_assign_diagnose", "Assign diagnose"),)

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access details for this record."""
        return reverse('record-detail', args=[str(self.id)])