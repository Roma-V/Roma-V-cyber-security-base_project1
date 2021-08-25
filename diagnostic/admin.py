from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import Record, Diagnose

# Register your models here.
admin.site.register(Record)
admin.site.register(Diagnose)

# Patients:
# michael.schumacher - racer.legend
# roald.amundsen - antarctic
# Doctors:
# ian.fleming - bondfather
# semiramis - thequeen
