from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa
import io
from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta, date
from django.conf import settings
from django.db.models import Q
import datetime

START_HRS = 8
END_HRS = 22
BUFFER = 15

# Create your views here.

def home_view(request):
    # send email to doctor about the patient test results every sunday
    if datetime.datetime.today().weekday() == 6:
        reports = models.Test_Results.objects.exclude(test_results=None)
        reports = reports.exclude(test_results='')
        for report in reports:
            doctor_email = report.doctor.user.email
            open('log.txt', 'a').close()
            with open('log.txt', 'r') as f:
                if str(report.id) not in f.read():
                    send_mail(
                        'Test results',
                        'Patient name: ' + report.patient.name + '\n' + 'Test results: ' + report.test_results,
                        settings.EMAIL_HOST_USER,
                        [doctor_email],
                        fail_silently=True,
                        auth_user=settings.EMAIL_HOST_USER,
                        auth_password=settings.EMAIL_HOST_PASSWORD
                    )
                    # add the report id to the file
                    with open('log.txt', 'a') as f:
                        f.write(str(report.id) + '\n')
    return render(request,'hospital/index.html')

def login_doctor(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if is_doctor(user):
                login(request, user)
                return redirect('/doctor-dashboard')
            else:
                messages.error(request, 'You are not a doctor')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'hospital/doctor-login.html')

def login_frontdesk(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if is_frontdesk(user):
                login(request, user)
                return redirect('/frontdesk-dashboard')
            else:
                messages.error(request, 'You are not a frontdesk operator')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'hospital/doctor-login.html')

def login_dataentry(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if is_dataentry(user):
                login(request, user)
                return redirect('/dataentry-dashboard')
            else:
                messages.error(request, 'You are not a data entry operator')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'hospital/doctor-login.html')

# @login_required(login_url='doctorlogin')
# def doctor_dashboard(request):
#     context = {
#         'doctor': models.DB_User.objects.get(user=request.user, type='Doctor'),
#         'patients': []
#     }
#     Doctor = models.DB_User.objects.get(user=request.user, type='Doctor')
#     for appointment in models.Appointment.objects.filter(doctor=Doctor):
#         context['patients'].append(appointment.patient)
#     return render(request, 'hospital/doctor_dashboard.html', context)

def is_doctor(user):
    return models.DB_User.objects.filter(user=user, type='Doctor').exists()

def is_frontdesk(user):
    return models.DB_User.objects.filter(user=user, type='FrontDesk').exists()

def is_dataentry(user):
    return models.DB_User.objects.filter(user=user, type='DataEntry').exists()

def doctorclick_view(request):
    if request.user.is_authenticated:
        if is_doctor(request.user):
            return HttpResponseRedirect('/doctor-dashboard')
    return redirect('/doctorlogin')

def frontdeskclick_view(request):
    if request.user.is_authenticated:
        if is_frontdesk(request.user):
            return HttpResponseRedirect('/frontdesk-dashboard')
    return redirect('/frontdesklogin')

def dataentryclick_view(request):
    if request.user.is_authenticated:
        if is_dataentry(request.user):
            return HttpResponseRedirect('/dataentry-dashboard')
    return redirect('/dataentrylogin')

def adminclick_view(request):
    return redirect('/admin')

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/dataentrylogin')
@user_passes_test(is_dataentry, login_url='/dataentrylogin')
def dataentry_dashboard(request):
    context = {
        'dataentry': models.DB_User.objects.get(user=request.user, type='DataEntry'),
        'tests': [],
    }
    for test in models.Test_Results.objects.all():
        if test.test_results == None or test.test_results== '':
            if test.test_slot is not None and test.test_slot <= datetime.datetime.now():
                context['tests'].append(test)
    return render(request, 'hospital/dataentry-dashboard.html', context)

@login_required(login_url='/dataentrylogin')
@user_passes_test(is_dataentry, login_url='/dataentrylogin')
def add_test_results(request, id=None):
    context = {
        'dataentry': models.DB_User.objects.get(user=request.user, type='DataEntry'),
    }
    if request.method == 'POST':
        test = models.Test_Results.objects.get(id=id)
        if test is not None:
            test_results = request.POST.get('test_results')
            test.test_results = test_results
            image_results = request.FILES.get('image_results')
            test.image_results = image_results
            test.save()
            messages.success(request, 'Test results added successfully')
            return redirect('/dataentry-dashboard')
        else:
            messages.error(request, 'Test not found')
            return redirect('/dataentry-dashboard')
    return render(request, 'hospital/dataentry-add-test-results.html', context)

####### at current we are redirecting to index page after pressing logout button from any user
# def logout_doctor(request):
#     logout(request)
#     messages.success(request, 'You have been logged out')
#     return redirect('')

# def logout_frontdesk(request):
#     logout(request)
#     messages.success(request, 'You have been logged out')
#     return redirect('')

# def logout_dataentry(request):
#     logout(request)
#     messages.success(request, 'You have been logged out')
#     return redirect('')

# # @login_required(login_url='frontdesklogin')
# def frontdesk_dashboard(request):
#     frontuser12 = models.DB_User.objects.get(id=3)
#     context = {
#         'frontdesk' : frontuser12,
#     }
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         address = request.POST.get('address')
#         mobile = request.POST.get('mobile')

#         patient = models.Patient.objects.create(
#             name=name,
#             address=address,
#             mobile=mobile,
#         )        
#         patient.save()
#         messages.success(request, 'Patient added successfully')
#         return redirect('frontdesk-dashboard')
#     return render(request, 'hospital/frontdesk-add-patient.html', context)

####################################FrontDesk####################################
@login_required(login_url='/frontdesklogin')
@user_passes_test(is_frontdesk, login_url='/frontdesklogin')
def frontdesk_dashboard(request):
    # frontuser12 = models.DB_User.objects.get(id=3) # after login workds replace frontuser12 with request.user
    frontdeskuser = models.DB_User.objects.get(user=request.user, type='FrontDesk')
    today = datetime.datetime.today().replace(microsecond=0)
    # Get all appointments for today
    all_appointments = models.Appointment.objects.all()
    appointments = []
    for appointment in all_appointments:
        now = appointment.appointmentDateSlot
        now_year = now.strftime("%Y")
        now_month = now.strftime("%m")
        now_date = now.strftime("%d")
        n = today
        n_year = n.strftime("%Y")
        n_month = n.strftime("%m")
        n_date = n.strftime("%d")
        
        if now_date == n_date and now_month == n_month and n_year == now_year:
            appointments.append(appointment)
    #Get all tests for today
    all_tests = models.Test_Results.objects.all()
    tests = []
    for test in all_tests:
        if test.test_slot == None:
            continue
        now = test.test_slot
        now_year = now.strftime("%Y")
        now_month = now.strftime("%m")
        now_date = now.strftime("%d")
        n = today
        n_year = n.strftime("%Y")
        n_month = n.strftime("%m")
        n_date = n.strftime("%d")
        
        if now_date == n_date and now_month == n_month and n_year == now_year:
            tests.append(test)

    context = {
        'frontdesk' : frontdeskuser,
        'patients': models.Patient.objects.all(),
        'appointments': appointments,
        'tests': tests,
        'rooms': models.Room.objects.all(),
    }
    return render(request, 'hospital/frontdesk-dashboard.html', context)

@login_required(login_url='/frontdesklogin')
@user_passes_test(is_frontdesk, login_url='/frontdesklogin')
def frontdesk_admit_patient(request, patient_id):
    P = models.Patient.objects.get(patientId = patient_id)
    if P.status == 'Admitted':
        messages.error(request, 'Patient already admitted')
        return redirect('/frontdesk-dashboard')
    # Now we look for a empty room
    room = models.Room.objects.filter(room_status='Available').first()
    # If no room is available then we return an error
    if room is None:
        messages.error(request, 'No room available')
        return redirect('/frontdesk-dashboard')
    # Now we update the room status to occupied
    room.room_status = 'Occupied'
    room.save()

    # Now we update the patient status to admitted
    P.status = 'Admitted'
    P.roomNumber = room
    P.admitDate = datetime.datetime.today().replace(microsecond=0)
    P.save()

    messages.success(
        request, 'Patient admitted successfully in room number '+str(room.room_number))
    return redirect('/frontdesk-dashboard')

@login_required(login_url='/frontdesklogin')
@user_passes_test(is_frontdesk, login_url='/frontdesklogin')
def frontdesk_discharge_patient(request, patient_id):
    P = models.Patient.objects.get(patientId=patient_id)
    if P.status == 'Discharged':
        messages.error(request, 'Patient already discharged')
        return redirect('/frontdesk-dashboard')
    
    if P.status == 'Registered':
        messages.error(request, 'Patient not admitted')
        return redirect('/frontdesk-dashboard')

    # Now we update the room status to occupied
    room = models.Room.objects.get(room_number = P.roomNumber.room_number)
    room.room_status = 'Available'
    room.save()

    # Now we update the patient status to admitted
    P.status = 'Discharged'
    P.dischargeDate = datetime.datetime.today().replace(microsecond=0)
    P.roomNumber = None
    P.save()
    messages.success(request, 'Patient discharged successfully')
    return redirect('/frontdesk-dashboard')

@login_required(login_url='/frontdesklogin')
@user_passes_test(is_frontdesk, login_url='/frontdesklogin')
def frontdesk_add_patient(request):
    # frontdeskuser = models.DB_User.objects.get(id=3)
    frontdeskuser = models.DB_User.objects.get(user=request.user, type='FrontDesk')
    context = {
        'frontdesk' : frontdeskuser,
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')

        patient = models.Patient.objects.create(
            name=name,
            address=address,
            mobile=mobile,
        )        
        patient.save()
        messages.success(request, 'Patient added successfully')
        return redirect('/frontdesk-dashboard')
    return render(request, 'hospital/frontdesk-add-patient.html', context)

@login_required(login_url='/frontdesklogin')
@user_passes_test(is_frontdesk, login_url='/frontdesklogin')
def frontdesk_schedule_appointment(request):
    patient = models.Patient.objects.all()
    new_patient = []
    for p in patient:
        if p.status == 'Admitted':
            continue
        else:
            if p.status == 'Discharged':
                p.status = 'Registered'
                p.save()
            new_patient.append(p)
    
    doctors = models.DB_User.objects.filter(type='Doctor')
    context = {
        'frontdesk': models.DB_User.objects.get(user=request.user), # after login workds replace frontuser12 with request.user
        'doctors': doctors,
        'patients': new_patient,
    }

    if request.method == 'POST':
        patientId = request.POST.get('patient')
        # patient id is invalid, then return error
        if not models.Patient.objects.filter(patientId=patientId).exists():
            messages.error(request, 'Patient ID is invalid')
            return redirect('/frontdesk-dashboard')
        patient = models.Patient.objects.get(patientId=patientId)
        assignedDoctor = request.POST.get('doctor') 
        if(int(assignedDoctor) > len(doctors)):
            messages.error(request, 'Doctor ID is invalid')
            return redirect('/frontdesk-dashboard')
        doctor = doctors[int(assignedDoctor)-1]
        appointment_date_slot = frontdesk_available_slots(doctor)
        description = request.POST.get('description')
        appointment = models.Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointmentDateSlot=appointment_date_slot,
            description=description
        )
        appointment.save()

        messages.success(request, 'Appointment scheduled successfully')
        return redirect('/frontdesk-dashboard')
    return render(request, 'hospital/frontdesk-schedule-appointment.html', context)

def frontdesk_available_slots(doctor):
    # Get all appointments of the doctor
    appointments = models.Appointment.objects.filter(doctor=doctor)
    # Get today Date from system
    # today = datetime.datetime.today().replace(microsecond=0)
    today = datetime.datetime.now().replace(microsecond=0)
    if(today.minute > BUFFER):
        hour = today.hour + 1
    else: 
        hour = today.hour
    next_day =  datetime.datetime.today().replace(microsecond=0) + datetime.timedelta(days=1)
    available_slots = []

    for i in range(hour,END_HRS):
        # Create a datetime object for each slot
        slot = datetime.datetime(today.year, today.month, today.day, i, 0, 0)
            # Check if the slot is already booked
        if not appointments.filter(appointmentDateSlot=slot).exists():
            available_slots.append(slot)
    for i in range(START_HRS,END_HRS):
        # Create a datetime object for each slot
        slot = datetime.datetime(next_day.year, next_day.month, next_day.day, i, 0, 0)
        # Check if the slot is already booked
        if not appointments.filter(appointmentDateSlot=slot).exists():
            available_slots.append(slot)

    return available_slots[0]

@login_required(login_url='/frontdesklogin')
@user_passes_test(is_frontdesk, login_url='/frontdesklogin')
def frontdesk_schedule_tests(request, test_id = None):
    tests = models.Test_Results.objects.filter(test_slot = None)
    context = {
        'frontdesk': models.DB_User.objects.get(user=request.user), 
        'tests': tests,
    }
    if test_id is not None:
        test = tests.get(id=test_id)
        test_slot = frontdesk_available_test_slot(test.test_name)

        if(test_slot is None):
            messages.error(request, 'No Available Slot within upcoming two days')
            return redirect('/frontdesk-dashboard')

        test.test_slot = test_slot
        test.save()
        messages.success(request, 'Test scheduled successfully')
        return redirect('/frontdesk-dashboard')

    return render(request, 'hospital/frontdesk-schedule-test.html', context)

def frontdesk_available_test_slot(test_name):
    tests = models.Test_Results.objects.filter(test_name=test_name)
    # Get today Date from system
    today = datetime.datetime.now().replace(microsecond=0)
    if(today.minute > BUFFER):
        hour = today.hour + 1
    else: 
        hour = today.hour
    next_day = datetime.datetime.today().replace(
        microsecond=0) + datetime.timedelta(days=1)
    available_slots = []

    for i in range(hour, END_HRS):
        # Create a datetime object for each slot
        slot = datetime.datetime(today.year, today.month, today.day, i, 0, 0)
            # Check if the slot is already booked
        if not tests.filter(test_slot=slot).exists():
            available_slots.append(slot)
    for i in range(START_HRS, END_HRS):
        # Create a datetime object for each slot
        slot = datetime.datetime(
            next_day.year, next_day.month, next_day.day, i, 0, 0)
        # Check if the slot is already booked
        if not tests.filter(test_slot=slot).exists():
            available_slots.append(slot)
    if available_slots is None:
        return None
    return available_slots[0]

def frontdesk_pending_tests(id):

    tests = models.Test_Results.objects.filter(patient=id)
    # Now among these tests remove those which are already done
    pending_tests = []
    for i in tests:
        if i.test_results is None:
            pending_tests.append(i)

    return pending_tests
#####################################Frontdesk Dashboard End#######################################



## ##################### Doctor Dashboard ############################
 
# doctor dashboard functionality to view all patients treated by him
@login_required(login_url='/doctorlogin')
@user_passes_test(is_doctor, login_url='/doctorlogin')
def doctor_dashboard(request):
    doctor = models.DB_User.objects.get(user=request.user)
    appointments = models.Appointment.objects.filter(doctor=doctor)
    patients = [appointment.patient for appointment in appointments]
    patients = list(set(patients))
    context = {
        'doctor': doctor,
        'patients': patients,
    }
    return render(request, 'hospital/doctor-dashboard.html', context)

@login_required(login_url='/doctorlogin')
@user_passes_test(is_doctor, login_url='/doctorlogin')
def doctor_notification(request):
    doctor = models.DB_User.objects.get(user=request.user)
    appointments = models.Appointment.objects.filter(doctor=doctor)

    time_now = datetime.datetime.now().replace(microsecond=0)
    app = []
    for appointment in appointments:
        if appointment.appointmentDateSlot.year == time_now.year and appointment.appointmentDateSlot.month == time_now.month and appointment.appointmentDateSlot.day == time_now.day and (appointment.appointmentDateSlot.hour > time_now.hour or (appointment.appointmentDateSlot.hour == time_now.hour and appointment.appointmentDateSlot.minute >= time_now.minute)):
            app.append(appointment)

    context = {
        'doctor': doctor,
        'appointments': app,
    }
    return render(request, 'hospital/doctor-notification.html', context)

# doctor dashboard functionality to prescribe medicine and add it to model Prescription 
@login_required(login_url='/doctorlogin')
@user_passes_test(is_doctor, login_url='/doctorlogin')
def doctor_prescribe_medicine(request, patient_id):
    # doctor12 = models.DB_User.objects.get(id=6)
    doctor = models.DB_User.objects.get(user=request.user)
    context = {
        'doctor': doctor,
        'patient': models.Patient.objects.get(patientId=patient_id),
    }
    if request.method == 'POST':
        medicine_name = request.POST.get('medicine_name')
        medicine_description = request.POST.get('medicine_description')
        medicine = models.Prescription.objects.create(
            patient=models.Patient.objects.get(patientId=patient_id),
            doctor=doctor,
            medicine_name=medicine_name,
            medicine_description=medicine_description
        )
        medicine.save()
        messages.success(request, 'Patient medicine added successfully')
        return redirect('/doctor-dashboard')
    return render(request, 'hospital/doctor-prescribe-meds.html', context)

# doctor dashboard functionality to prescribe test and add it to model Test_Results
@login_required(login_url='/doctorlogin')
@user_passes_test(is_doctor, login_url='/doctorlogin')
def doctor_prescribe_test(request, patient_id):
    # doctor12 = models.DB_User.objects.get(id=6)
    doctor = models.DB_User.objects.get(user=request.user)
    context = {
        'doctor': doctor,
        'patient': models.Patient.objects.get(patientId=patient_id),
    }
    if request.method == 'POST':
        test_name = request.POST.get('test_name')
        test = models.Test_Results.objects.create(
            patient=models.Patient.objects.get(patientId=patient_id),
            doctor=doctor,
            test_name=test_name,
        )
        test.save()
        messages.success(request, 'Patient test added successfully')
        return redirect('/doctor-dashboard')
    return render(request, 'hospital/doctor-prescribe-test.html', context)

# doctor dashboard functionality to view all information of a patient
@login_required(login_url='/doctorlogin')
@user_passes_test(is_doctor, login_url='/doctorlogin')
def doctor_view_patient(request, patient_id):
    # doctor12 = models.DB_User.objects.get(id=6)
    doctor = models.DB_User.objects.get(user=request.user)
    context = {
        'doctor': doctor,
        'patient': models.Patient.objects.get(patientId=patient_id),
        'prescriptions': models.Prescription.objects.filter(patient=patient_id),
        'test_results': models.Test_Results.objects.filter(patient=patient_id),
    }
    
    return render(request, 'hospital/doctor_view_patient.html', context)

@login_required(login_url='/doctorlogin')
@user_passes_test(is_doctor, login_url='/doctorlogin')
def doctor_view_image(request, url):
    context = {
        'doctor': models.DB_User.objects.get(user=request.user),
        'url': url
    }
    return render(request, 'hospital/doctor-view-image.html', context);

def aboutus_view(request):
    return render(request, 'hospital/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name = sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email), message, settings.EMAIL_HOST_USER,
                      settings.EMAIL_RECEIVING_USER, fail_silently=True)
            return render(request, 'hospital/contactussuccess.html')
    return render(request, 'hospital/contactus.html', {'form': sub})
