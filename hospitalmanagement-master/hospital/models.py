from django.db import models
from django.contrib.auth.models import User


# departments=[('Cardiologist','Cardiologist'),
# ('Dermatologists','Dermatologists'),
# ('Emergency Medicine Specialists','Emergency Medicine Specialists'),
# ('Allergists/Immunologists','Allergists/Immunologists'),
# ('Anesthesiologists','Anesthesiologists'),
# ('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
# ]


class DB_User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=[(
        'Doctor', 'Doctor'), ('FrontDesk', 'FrontDesk'), ('DataEntry', 'DataEntry')])
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=False)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.first_name+" ("+self.type+")"

# class Doctor(models.Model):
    # user=models.OneToOneField(User,on_delete=models.CASCADE)
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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # profile_pic= models.ImageField(upload_to='profile_pic/PatientProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=False)
    # symptoms = models.CharField(max_length=100,null=False)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    roomNumber = models.ForeignKey('Room', on_delete=models.SET_NULL,null=True)
    admitDate = models.DateField(null=False)
    dischargeDate = models.DateField(null=False)
    status = models.CharField(max_length=50, choices=[('Admitted', 'Admitted'), ('Discharged', 'Discharged'), ('Registered', 'Registered')], default='Registered')

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.first_name + " (" + Patient + ")"


class Appointment(models.Model):
    patientId = models.ForeignKey('Patient', on_delete=models.CASCADE)
    doctorId = models.ForeignKey('DB_User', on_delete=models.CASCADE)
    appointmentDate = models.DateField(auto_now=True)
    description = models.TextField(max_length=500)


# class PatientDischargeDetails(models.Model):
#     patientId = models.ForeignKey('Patient', on_delete=models.SET_NULL)
#     patientName = models.CharField(max_length=40)
#     assignedDoctorName = models.CharField(max_length=40)
#     address = models.CharField(max_length=40)
#     mobile = models.CharField(max_length=20, null=True)
#     symptoms = models.CharField(max_length=100, null=True)

#     roomCharge = models.PositiveIntegerField(null=False)
#     medicineCost = models.PositiveIntegerField(null=False)
#     doctorFee = models.PositiveIntegerField(null=False)
#     OtherCharge = models.PositiveIntegerField(null=False)
#     total = models.PositiveIntegerField(null=False)


class Prescription(models.Model):
    patientId = models.ForeignKey('Patient', on_delete=models.CASCADE)
    doctorId = models.ForeignKey('DB_User', on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=50)
    medicine_description = models.TextField(max_length=500)


class Room(models.Model):
    room_number = models.PositiveIntegerField(null=True)
    room_status = models.BooleanField(default=True)


class Test_Results(models.Model):
    patientId = models.ForeignKey('Patient', on_delete=models.CASCADE)
    doctorId = models.ForeignKey('DB_User', on_delete=models.SET_NULL)
    Test_name = models.CharField(max_length=100)
    Test_Results = models.BooleanField(default=False)
    Test_slot = models.DateTimeField(null=True)

    @property
    def get_test_results(self):
        return self.Test_Results
