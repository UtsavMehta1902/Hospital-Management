from django.db import models
from django.contrib.auth.models import User
import matplotlib.pyplot as plt


# departments=[('Cardiologist','Cardiologist'),
# ('Dermatologists','Dermatologists'),
# ('Emergency Medicine Specialists','Emergency Medicine Specialists'),
# ('Allergists/Immunologists','Allergists/Immunologists'),
# ('Anesthesiologists','Anesthesiologists'),
# ('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
# ]


class DB_User(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=[('Doctor', 'Doctor'), ('FrontDesk', 'FrontDesk'), ('DataEntry', 'DataEntry')])
    address = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.first_name+" ("+self.type+")"

# class Doctor(models.Model):
#     user=models.OneToOneField(User,on_delete=models.CASCADE)
#     address = models.CharField(max_length=40)
#     mobile = models.CharField(max_length=20,null=True)
#     department= models.CharField(max_length=50,choices=departments,default='Cardiologist')
#     status=models.BooleanField(default=False)
#     @property
#     def get_name(self):
#         return self.user.first_name+" "+self.user.last_name
#     @property
#     def get_id(self):
#         return self.user.id
#     def __str__(self):
#         return "{} ({})".format(self.user.first_name,self.department)


class Patient(models.Model):
    patientId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    # profile_pic= models.ImageField(upload_to='profile_pic/PatientProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20)
    # symptoms = models.CharField(max_length=100,null=False)
    roomNumber = models.ForeignKey('Room', on_delete=models.SET_NULL,null=True, default=None)
    admitDate = models.DateField(null=True, default=None)
    dischargeDate = models.DateField(null=True, default=None)
    status = models.CharField(max_length=50, choices=[('Admitted', 'Admitted'), ('Discharged', 'Discharged'), ('Registered', 'Registered')], default='Registered')

    @property
    def get_name(self):
        return self.name

    @property
    def get_id(self):
        return self.patientId
    def __str__(self):
        return self.name + " (" + str(self.patientId) + ")"


class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('DB_User', on_delete=models.CASCADE)
    appointmentDateSlot = models.DateTimeField(null=True, default=None)
    description = models.TextField(max_length=500, blank=True, default='')

class Prescription(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('DB_User', on_delete=models.SET_NULL, null=True)
    medicine_name = models.CharField(max_length=50)
    medicine_description = models.TextField(max_length=500, blank=True, default='')


class Room(models.Model):
    room_number = models.PositiveIntegerField(primary_key=True)
    room_status = models.CharField(max_length=50, choices=[('Available', 'Available'), ('Occupied', 'Occupied')], default='Available')


class Test_Results(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('DB_User', on_delete=models.SET_NULL, null=True)
    test_name = models.CharField(max_length=100)
    test_results = models.TextField(max_length=500, null=True, blank=True, default=None)
    image_results = models.ImageField(upload_to='Test_Results/', null=True, blank=True, default=None)
    test_slot = models.DateTimeField(null=True, default=None)

    @property
    def get_test_results(self):
        return self.test_results
    
    @property
    def show_test_image(self):
        plt.imshow(self.image_results)
