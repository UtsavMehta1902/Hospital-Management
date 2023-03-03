from django.contrib import admin
from .models import DB_User, Patient, Appointment, Prescription, Room, Test_Results
# Register your models here.
admin.site.register(DB_User)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Prescription)
admin.site.register(Room)
admin.site.register(Test_Results)

