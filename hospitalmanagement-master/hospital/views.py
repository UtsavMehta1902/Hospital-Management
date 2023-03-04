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

# Create your views here.

def home_view(request):
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/index.html')

def login_doctor(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            db_user = models.DB_User.objects.get(user=user, type='Doctor')
            if db_user is not None:
                login(request, user)
                return redirect('/doctor-dashboard')
            else:
                messages.error(request, 'You are not a doctor')
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

def login_frontdesk(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            db_user = models.DB_User.objects.get(user=user, type='FrontDesk')
            if db_user is not None:
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
            db_user = models.DB_User.objects.get(user=user, type='DataEntry')
            if db_user is not None:
                login(request, user)
                return redirect('/dataentry-dashboard')
            else:
                messages.error(request, 'You are not a data entry operator')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'hospital/doctor-login.html')

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

#for showing signup/login button for patient(by sumit)
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
            if test.test_slot is not None:
                context['tests'].append(test)
    return render(request, 'hospital/dataentry-dashboard.html', context)

@login_required(login_url='/dataentrylogin')
@user_passes_test(is_dataentry, login_url='/dataentrylogin')
def add_test_results(request, id, name):
    context = {
        'dataentry': models.DB_User.objects.get(user=request.user, type='DataEntry'),
    }
    if request.method == 'POST':
        Patient = models.Patient.objects.get(patientId=id)
        testname = name
        if models.Test_Results.objects.filter(patient=Patient, test_name=testname).exists():
            test = models.Test_Results.objects.get(patient=Patient, test_name=testname)
            test = models.Test_Results.objects.get(patient=Patient, test_name=testname)
            test_results = request.POST.get('test_results')
            test.test_results = test_results
            # image_results = request.FILES.get('image_results')
            # test.image_results = image_results
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
    appointments = models.Appointment.objects.filter(appointmentDateSlot = today)
    #Get all tests for today
    tests = models.Test_Results.objects.filter(test_slot = today)

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
    # In context also add slot availability for each doctor by calling a function
    # Now add the new_doc to context
    patient = models.DB_User.objects.all()
    # Remove those patient which are admitted or discharged from the list
    new_patient = []
    for p in patient:
        if p.status == 'Admitted' or p.status == 'Discharged':
            continue
        else:
            new_patient.append(p)
    
    context = {
        'doctors': models.DB_User.objects.filter(type='Doctor'),
        'patients': new_patient,
    }
    if request.method == 'POST':
        patientId = request.POST.get('patientId')
        assignedDoctor = request.POST.get('assignedDoctor') #DoctorID
        # appointment_date_slot = request.POST.get('appointmentDateSlot')
        appointment_date_slot = frontdesk_available_slots(assignedDoctor)
        description = request.POST.get('description')
        # Save the appointment in the database
        appointment = models.Appointment.objects.create(
            patient=patientId,
            doctor=assignedDoctor,
            appointmentDateSlot=appointment_date_slot,
            description=description
        )
        appointment.save()

        messages.success(request, 'Appointment scheduled successfully')
        return redirect('frontdesk_dashboard/schedule_appointment')
    return render(request, 'hospital/frontdesk_dashboard/schedule_appointment.html', context)

def frontdesk_available_slots(doctor):
    # Get all appointments of the doctor
    appointments = models.Appointment.objects.filter(assignedDoctorId=doctor)
    # Get today Date from system
    today = datetime.datetime.today().replace(microsecond=0)
    next_day =  datetime.datetime.today().replace(microsecond=0) + datetime.timedelta(days=1)
    available_slots = []

    for i in range(8,18):
        # Create a datetime object for each slot
        slot = datetime.datetime(today.year, today.month, today.day, i, 0, 0)
        # Check if the slot is in the future
        if slot > today:
            # Check if the slot is already booked
            if not appointments.filter(appointmentDateSlot=slot).exists():
                available_slots.append(slot)
    for i in range(8,18):
        # Create a datetime object for each slot
        slot = datetime.datetime(next_day.year, next_day.month, next_day.day, i, 0, 0)
        # Check if the slot is in the future
        if slot > today:
            # Check if the slot is already booked
            if not appointments.filter(appointmentDateSlot=slot).exists():
                available_slots.append(slot)
    
    # # If size of available slots greater than 5 then return only 5 slots
    # if len(available_slots) > 5:
    #     return available_slots[:5]
    
    return available_slots[0]

@login_required(login_url='/frontdesklogin')
@user_passes_test(is_frontdesk, login_url='/frontdesklogin')
def frontdesk_schedule_tests(request):
    P = models.Patient.objects.all()

    patient = []
    for i in P:
        pending_test = frontdesk_pending_tests(i.id)
        if len(pending_test) > 0:
            for j in pending_test:
                patient.append(
                    {
                        'id': i.id,
                        'name': i.name,
                        'test': j.test_name,
                        'doctor_id' : j.doctor.id,
                        'doctor_name' : j.doctor.name,
                        # 'SLOT': frontdesk_availaible_test_slot(j.test_name)
                    }
                )
    context = {
        'patients': patient,
    }
    if request.method == 'POST':
        patientId = request.POST.get('patientId')
        doctorId = request.POST.get('doctorId')
        test_name = request.POST.get('test_name')
        test_slot = frontdesk_available_slots(test_name)
        test = models.Test.objects.create(
            patient=patientId,
            doctor=doctorId,
            test_name=test_name,
            test_slot=test_slot,
        )
        test.save()
        messages.success(request, 'Test scheduled successfully')
        return redirect('frontdesk_dashboard/schedule_test')

    return render(request, 'hospital/frontdesk_dashboard/schedule_test.html', context)

def frontdesk_availaible_test_slot(test_name):
    tests = models.Test.objects.filter(test_name=test_name)
    # Get today Date from system
    today = datetime.datetime.today().replace(microsecond=0)
    next_day = datetime.datetime.today().replace(
        microsecond=0) + datetime.timedelta(days=1)
    available_slots = []

    for i in range(8, 18):
        # Create a datetime object for each slot
        slot = datetime.datetime(today.year, today.month, today.day, i, 0, 0)
        # Check if the slot is in the future
        if slot > today:
            # Check if the slot is already booked
            if not tests.filter(test_slot=slot).exists():
                available_slots.append(slot)
    for i in range(8, 18):
        # Create a datetime object for each slot
        slot = datetime.datetime(
            next_day.year, next_day.month, next_day.day, i, 0, 0)
        # Check if the slot is in the future
        if slot > today:
            # Check if the slot is already booked
            if not tests.filter(test_slot=slot).exists():
                available_slots.append(slot)

    return available_slots[0]

def frontdesk_pending_tests(id):
    tests = models.Test.objects.filter(patient=id)
    # Now among these tests remove those which are already done
    pending_tests = []
    for i in tests:
        if i.test_result is None:
            pending_tests.append(i)

    return pending_tests
#####################################Frontdesk Dashboard End#######################################



## ##################### Doctor Dashboard ############################
 
# doctor dashboard functionality to view all patients treated by him
@login_required(login_url='/doctorlogin')
@user_passes_test(is_doctor, login_url='/doctorlogin')
def doctor_dashboard(request):
    # doctor12 = models.DB_User.objects.get(id=6)
    doctor = models.DB_User.objects.get(user=request.user)
    appointments = models.Appointment.objects.filter(doctor=doctor)
    patients = [appointment.patient for appointment in appointments]
    context = {
        'doctor': doctor,
        'patients': patients,
    }
    return render(request, 'hospital/doctor-dashboard.html', context)

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
                      settings.EMAIL_RECEIVING_USER, fail_silently=False)
            return render(request, 'hospital/contactussuccess.html')
    return render(request, 'hospital/contactus.html', {'form': sub})

'''
### -------------------- sumit starts here -----------------------

# for showing signup/login button for admin(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'hospital/adminclick.html')

def admin_signup_view(request):
    form = forms.AdminSigupForm()
    if request.method == 'POST':
        form = forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request, 'hospital/adminsignup.html', {'form': form})


def doctor_signup_view(request):
    userForm = forms.DoctorUserForm()
    doctorForm = forms.DoctorForm()
    mydict = {'userForm': userForm, 'doctorForm': doctorForm}
    if request.method == 'POST':
        userForm = forms.DoctorUserForm(request.POST)
        doctorForm = forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorForm.save(commit=False)
            doctor.user = user
            doctor = doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect('doctorlogin')
    return render(request, 'hospital/doctorsignup.html', context=mydict)


def patient_signup_view(request):
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    mydict = {'userForm': userForm, 'patientForm': patientForm}
    if request.method == 'POST':
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST, request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.user = user
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient = patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('patientlogin')
    return render(request, 'hospital/patientsignup.html', context=mydict)


# # -----------for checking user is doctor , patient or admin(by sumit)
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


# def is_doctor(user):
#     return user.groups.filter(name='DOCTOR').exists()


def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


# ---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_doctor(request.user):
        accountapproval = models.Doctor.objects.all().filter(
            user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('doctor-dashboard')
        else:
            return render(request, 'hospital/doctor_wait_for_approval.html')
    elif is_patient(request.user):
        accountapproval = models.Patient.objects.all().filter(
            user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('patient-dashboard')
        else:
            return render(request, 'hospital/patient_wait_for_approval.html')


# ---------------------------------------------------------------------------------
# ------------------------ ADMIN RELATED VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    # for both table in admin dashboard
    # doctors = models.Doctor.objects.all().order_by('-id')
    # patients = models.Patient.objects.all().order_by('-id')
    # # for three cards
    # doctorcount = models.Doctor.objects.all().filter(status=True).count()
    # pendingdoctorcount = models.Doctor.objects.all().filter(status=False).count()

    # patientcount = models.Patient.objects.all().filter(status=True).count()
    # pendingpatientcount = models.Patient.objects.all().filter(status=False).count()

    # appointmentcount = models.Appointment.objects.all().filter(status=True).count()
    # pendingappointmentcount = models.Appointment.objects.all().filter(status=False).count()
    # mydict = {
    #     'doctors': doctors,
    #     'patients': patients,
    #     'doctorcount': doctorcount,
    #     'pendingdoctorcount': pendingdoctorcount,
    #     'patientcount': patientcount,
    #     'pendingpatientcount': pendingpatientcount,
    #     'appointmentcount': appointmentcount,
    #     'pendingappointmentcount': pendingappointmentcount,
    # }
    # return render(request, 'hospital/doctor-dashboard.html', context=mydict)

    patients = [{
        'id': 1,
        'name': 'John',
    }, {
        'id': 2,
        'name': 'Yates',
    }, {
        'id': 3,
        'name': 'Smith',
    }]
    return render(request, 'hospital/doctor-dashboard.html', {'patients': patients})


# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request, 'hospital/admin_doctor.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors = models.Doctor.objects.all().filter(status=True)
    return render(request, 'hospital/admin_view_doctor.html', {'doctors': doctors})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-view-doctor')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_doctor_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)

    userForm = forms.DoctorUserForm(instance=user)
    doctorForm = forms.DoctorForm(request.FILES, instance=doctor)
    mydict = {'userForm': userForm, 'doctorForm': doctorForm}
    if request.method == 'POST':
        userForm = forms.DoctorUserForm(request.POST, instance=user)
        doctorForm = forms.DoctorForm(
            request.POST, request.FILES, instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorForm.save(commit=False)
            doctor.status = True
            doctor.save()
            return redirect('admin-view-doctor')
    return render(request, 'hospital/admin_update_doctor.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userForm = forms.DoctorUserForm()
    doctorForm = forms.DoctorForm()
    mydict = {'userForm': userForm, 'doctorForm': doctorForm}
    if request.method == 'POST':
        userForm = forms.DoctorUserForm(request.POST)
        doctorForm = forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            doctor = doctorForm.save(commit=False)
            doctor.user = user
            doctor.status = True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-doctor')
    return render(request, 'hospital/admin_add_doctor.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    # those whose approval are needed
    doctors = models.Doctor.objects.all().filter(status=False)
    return render(request, 'hospital/admin_approve_doctor.html', {'doctors': doctors})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_doctor_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    doctor.status = True
    doctor.save()
    return redirect(reverse('admin-approve-doctor'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_doctor_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-approve-doctor')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_specialisation_view(request):
    doctors = models.Doctor.objects.all().filter(status=True)
    return render(request, 'hospital/admin_view_doctor_specialisation.html', {'doctors': doctors})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_patient_view(request):
    return render(request, 'hospital/admin_patient.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients = models.Patient.objects.all().filter(status=True)
    return render(request, 'hospital/admin_view_patient.html', {'patients': patients})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_patient_from_hospital_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-view-patient')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)

    userForm = forms.PatientUserForm(instance=user)
    patientForm = forms.PatientForm(request.FILES, instance=patient)
    mydict = {'userForm': userForm, 'patientForm': patientForm}
    if request.method == 'POST':
        userForm = forms.PatientUserForm(request.POST, instance=user)
        patientForm = forms.PatientForm(
            request.POST, request.FILES, instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.status = True
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient.save()
            return redirect('admin-view-patient')
    return render(request, 'hospital/admin_update_patient.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    mydict = {'userForm': userForm, 'patientForm': patientForm}
    if request.method == 'POST':
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST, request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            patient = patientForm.save(commit=False)
            patient.user = user
            patient.status = True
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-patient')
    return render(request, 'hospital/admin_add_patient.html', context=mydict)


# ------------------FOR APPROVING PATIENT BY ADMIN----------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_patient_view(request):
    # those whose approval are needed
    patients = models.Patient.objects.all().filter(status=False)
    return render(request, 'hospital/admin_approve_patient.html', {'patients': patients})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    patient.status = True
    patient.save()
    return redirect(reverse('admin-approve-patient'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-approve-patient')


# --------------------- FOR DISCHARGING PATIENT BY ADMIN START-------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_discharge_patient_view(request):
    patients = models.Patient.objects.all().filter(status=True)
    return render(request, 'hospital/admin_discharge_patient.html', {'patients': patients})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def discharge_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    days = (date.today()-patient.admitDate)  # 2 days, 0:00:00
    assignedDoctor = models.User.objects.all().filter(id=patient.assignedDoctorId)
    d = days.days  # only how many day that is 2
    patientDict = {
        'patientId': pk,
        'name': patient.get_name,
        'mobile': patient.mobile,
        'address': patient.address,
        'symptoms': patient.symptoms,
        'admitDate': patient.admitDate,
        'todayDate': date.today(),
        'day': d,
        'assignedDoctorName': assignedDoctor[0].first_name,
    }
    if request.method == 'POST':
        feeDict = {
            'roomCharge': int(request.POST['roomCharge'])*int(d),
            'doctorFee': request.POST['doctorFee'],
            'medicineCost': request.POST['medicineCost'],
            'OtherCharge': request.POST['OtherCharge'],
            'total': (int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        }
        patientDict.update(feeDict)
        # for updating to database patientDischargeDetails (pDD)
        pDD = models.PatientDischargeDetails()
        pDD.patientId = pk
        pDD.patientName = patient.get_name
        pDD.assignedDoctorName = assignedDoctor[0].first_name
        pDD.address = patient.address
        pDD.mobile = patient.mobile
        pDD.symptoms = patient.symptoms
        pDD.admitDate = patient.admitDate
        pDD.releaseDate = date.today()
        pDD.daySpent = int(d)
        pDD.medicineCost = int(request.POST['medicineCost'])
        pDD.roomCharge = int(request.POST['roomCharge'])*int(d)
        pDD.doctorFee = int(request.POST['doctorFee'])
        pDD.OtherCharge = int(request.POST['OtherCharge'])
        pDD.total = (int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(
            request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        pDD.save()
        return render(request, 'hospital/patient_final_bill.html', context=patientDict)
    return render(request, 'hospital/patient_generate_bill.html', context=patientDict)


# --------------for discharge patient bill (pdf) download and printing


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return


def download_pdf_view(request, pk):
    dischargeDetails = models.PatientDischargeDetails.objects.all().filter(
        patientId=pk).order_by('-id')[:1]
    dict = {
        'patientName': dischargeDetails[0].patientName,
        'assignedDoctorName': dischargeDetails[0].assignedDoctorName,
        'address': dischargeDetails[0].address,
        'mobile': dischargeDetails[0].mobile,
        'symptoms': dischargeDetails[0].symptoms,
        'admitDate': dischargeDetails[0].admitDate,
        'releaseDate': dischargeDetails[0].releaseDate,
        'daySpent': dischargeDetails[0].daySpent,
        'medicineCost': dischargeDetails[0].medicineCost,
        'roomCharge': dischargeDetails[0].roomCharge,
        'doctorFee': dischargeDetails[0].doctorFee,
        'OtherCharge': dischargeDetails[0].OtherCharge,
        'total': dischargeDetails[0].total,
    }
    return render_to_pdf('hospital/download_bill.html', dict)


# -----------------APPOINTMENT START--------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request, 'hospital/admin_appointment.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments = models.Appointment.objects.all().filter(status=True)
    return render(request, 'hospital/admin_view_appointment.html', {'appointments': appointments})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    appointmentForm = forms.AppointmentForm()
    mydict = {'appointmentForm': appointmentForm, }
    if request.method == 'POST':
        appointmentForm = forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment = appointmentForm.save(commit=False)
            appointment.doctorId = request.POST.get('doctorId')
            appointment.patientId = request.POST.get('patientId')
            appointment.doctorName = models.User.objects.get(
                id=request.POST.get('doctorId')).first_name
            appointment.patientName = models.User.objects.get(
                id=request.POST.get('patientId')).first_name
            appointment.status = True
            appointment.save()
        return HttpResponseRedirect('admin-view-appointment')
    return render(request, 'hospital/admin_add_appointment.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    # those whose approval are needed
    appointments = models.Appointment.objects.all().filter(status=False)
    return render(request, 'hospital/admin_approve_appointment.html', {'appointments': appointments})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.status = True
    appointment.save()
    return redirect(reverse('admin-approve-appointment'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-approve-appointment')
# ---------------------------------------------------------------------------------
# ------------------------ ADMIN RELATED VIEWS END ------------------------------
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# ------------------------ DOCTOR RELATED VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    # # for three cards
    patientcount = models.Patient.objects.all().filter(
        status=True, assignedDoctorId=request.user.id).count()
    appointmentcount = models.Appointment.objects.all().filter(
        status=True, doctorId=request.user.id).count()
    patientdischarged = models.PatientDischargeDetails.objects.all(
    ).distinct().filter(assignedDoctorName=request.user.first_name).count()

    # for  table in doctor dashboard
    appointments = models.Appointment.objects.all().filter(
        status=True, doctorId=request.user.id).order_by('-id')
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = models.Patient.objects.all().filter(
        status=True, user_id__in=patientid).order_by('-id')
    appointments = zip(appointments, patients)
    mydict = {
        'patientcount': patientcount,
        'appointmentcount': appointmentcount,
        'patientdischarged': patientdischarged,
        'appointments': appointments,
        # for profile picture of doctor in sidebar
        'doctor': models.Doctor.objects.get(user_id=request.user.id),
    }
    return render(request, 'hospital/doctor-dashboard.html', context=mydict)


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict = {
        # for profile picture of doctor in sidebar
        'doctor': models.Doctor.objects.get(user_id=request.user.id),
    }
    return render(request, 'hospital/doctor_patient.html', context=mydict)


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients = models.Patient.objects.all().filter(
        status=True, assignedDoctorId=request.user.id)
    # for profile picture of doctor in sidebar
    doctor = models.Doctor.objects.get(user_id=request.user.id)
    return render(request, 'hospital/doctor_view_patient.html', {'patients': patients, 'doctor': doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def search_view(request):
    # for profile picture of doctor in sidebar
    doctor = models.Doctor.objects.get(user_id=request.user.id)
    # whatever user write in search box we get in query
    query = request.GET['query']
    patients = models.Patient.objects.all().filter(status=True, assignedDoctorId=request.user.id).filter(
        Q(symptoms__icontains=query) | Q(user__first_name__icontains=query))
    return render(request, 'hospital/doctor_view_patient.html', {'patients': patients, 'doctor': doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    dischargedpatients = models.PatientDischargeDetails.objects.all(
    ).distinct().filter(assignedDoctorName=request.user.first_name)
    # for profile picture of doctor in sidebar
    doctor = models.Doctor.objects.get(user_id=request.user.id)
    return render(request, 'hospital/doctor_view_discharge_patient.html', {'dischargedpatients': dischargedpatients, 'doctor': doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    # for profile picture of doctor in sidebar
    doctor = models.Doctor.objects.get(user_id=request.user.id)
    return render(request, 'hospital/doctor_appointment.html', {'doctor': doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    # for profile picture of doctor in sidebar
    doctor = models.Doctor.objects.get(user_id=request.user.id)
    appointments = models.Appointment.objects.all().filter(
        status=True, doctorId=request.user.id)
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = models.Patient.objects.all().filter(
        status=True, user_id__in=patientid)
    appointments = zip(appointments, patients)
    return render(request, 'hospital/doctor_view_appointment.html', {'appointments': appointments, 'doctor': doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    # for profile picture of doctor in sidebar
    doctor = models.Doctor.objects.get(user_id=request.user.id)
    appointments = models.Appointment.objects.all().filter(
        status=True, doctorId=request.user.id)
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = models.Patient.objects.all().filter(
        status=True, user_id__in=patientid)
    appointments = zip(appointments, patients)
    return render(request, 'hospital/doctor_delete_appointment.html', {'appointments': appointments, 'doctor': doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def delete_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.delete()
    # for profile picture of doctor in sidebar
    doctor = models.Doctor.objects.get(user_id=request.user.id)
    appointments = models.Appointment.objects.all().filter(
        status=True, doctorId=request.user.id)
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = models.Patient.objects.all().filter(
        status=True, user_id__in=patientid)
    appointments = zip(appointments, patients)
    return render(request, 'hospital/doctor_delete_appointment.html', {'appointments': appointments, 'doctor': doctor})


# ---------------------------------------------------------------------------------
# ------------------------ DOCTOR RELATED VIEWS END ------------------------------
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# ------------------------ PATIENT RELATED VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    patient = models.Patient.objects.get(user_id=request.user.id)
    doctor = models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    mydict = {
        'patient': patient,
        'doctorName': doctor.get_name,
        'doctorMobile': doctor.mobile,
        'doctorAddress': doctor.address,
        'symptoms': patient.symptoms,
        'doctorDepartment': doctor.department,
        'admitDate': patient.admitDate,
    }
    return render(request, 'hospital/patient_dashboard.html', context=mydict)


@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_appointment_view(request):
    # for profile picture of patient in sidebar
    patient = models.Patient.objects.get(user_id=request.user.id)
    return render(request, 'hospital/patient_appointment.html', {'patient': patient})


@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    appointmentForm = forms.PatientAppointmentForm()
    # for profile picture of patient in sidebar
    patient = models.Patient.objects.get(user_id=request.user.id)
    message = None
    mydict = {'appointmentForm': appointmentForm,
              'patient': patient, 'message': message}
    if request.method == 'POST':
        appointmentForm = forms.PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            print(request.POST.get('doctorId'))
            desc = request.POST.get('description')

            doctor = models.Doctor.objects.get(
                user_id=request.POST.get('doctorId'))

            appointment = appointmentForm.save(commit=False)
            appointment.doctorId = request.POST.get('doctorId')
            # ----user can choose any patient but only their info will be stored
            appointment.patientId = request.user.id
            appointment.doctorName = models.User.objects.get(
                id=request.POST.get('doctorId')).first_name
            # ----user can choose any patient but only their info will be stored
            appointment.patientName = request.user.first_name
            appointment.status = False
            appointment.save()
        return HttpResponseRedirect('patient-view-appointment')
    return render(request, 'hospital/patient_book_appointment.html', context=mydict)


def patient_view_doctor_view(request):
    doctors = models.Doctor.objects.all().filter(status=True)
    # for profile picture of patient in sidebar
    patient = models.Patient.objects.get(user_id=request.user.id)
    return render(request, 'hospital/patient_view_doctor.html', {'patient': patient, 'doctors': doctors})


def search_doctor_view(request):
    # for profile picture of patient in sidebar
    patient = models.Patient.objects.get(user_id=request.user.id)

    # whatever user write in search box we get in query
    query = request.GET['query']
    doctors = models.Doctor.objects.all().filter(status=True).filter(
        Q(department__icontains=query) | Q(user__first_name__icontains=query))
    return render(request, 'hospital/patient_view_doctor.html', {'patient': patient, 'doctors': doctors})


@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    # for profile picture of patient in sidebar
    patient = models.Patient.objects.get(user_id=request.user.id)
    appointments = models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(request, 'hospital/patient_view_appointment.html', {'appointments': appointments, 'patient': patient})


@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_discharge_view(request):
    # for profile picture of patient in sidebar
    patient = models.Patient.objects.get(user_id=request.user.id)
    dischargeDetails = models.PatientDischargeDetails.objects.all().filter(
        patientId=patient.id).order_by('-id')[:1]
    patientDict = None
    if dischargeDetails:
        patientDict = {
            'is_discharged': True,
            'patient': patient,
            'patientId': patient.id,
            'patientName': patient.get_name,
            'assignedDoctorName': dischargeDetails[0].assignedDoctorName,
            'address': patient.address,
            'mobile': patient.mobile,
            'symptoms': patient.symptoms,
            'admitDate': patient.admitDate,
            'releaseDate': dischargeDetails[0].releaseDate,
            'daySpent': dischargeDetails[0].daySpent,
            'medicineCost': dischargeDetails[0].medicineCost,
            'roomCharge': dischargeDetails[0].roomCharge,
            'doctorFee': dischargeDetails[0].doctorFee,
            'OtherCharge': dischargeDetails[0].OtherCharge,
            'total': dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict = {
            'is_discharged': False,
            'patient': patient,
            'patientId': request.user.id,
        }
    return render(request, 'hospital/patient_discharge.html', context=patientDict)


# ------------------------ PATIENT RELATED VIEWS END ------------------------------
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# ------------------------ ABOUT US AND CONTACT US VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
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
                      settings.EMAIL_RECEIVING_USER, fail_silently=False)
            return render(request, 'hospital/contactussuccess.html')
    return render(request, 'hospital/contactus.html', {'form': sub})


# ---------------------------------------------------------------------------------
# ------------------------ ADMIN RELATED VIEWS END ------------------------------
# ---------------------------------------------------------------------------------

def patient_view(request, id):
    patient = {
        'id': id,
        'name': 'Rahul',
        'address': 'Kathmandu',
        'mobile': '9841234567',
        'room': 'A-101',
        'status': 'Discharged',
    }
    return render(request, 'hospital/doctor_view_patient.html', {'patient': patient})

'''