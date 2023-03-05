
from django.contrib import admin
from django.urls import path
from hospital import views
from django.contrib.auth.views import LoginView,LogoutView

'''
#-------------FOR ADMIN RELATED URLS
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),

    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),

    path('doctorclick', views.doctorclick_view),
    path('frontdeskclick', views.frontdeskclick_view),
    path('dataentryclick', views.dataentryclick_view),
    
    path('frontdesklogin', views.login_frontdesk, name='login_frontdesk'),
    path('doctorlogin', views.login_doctor, name='login_doctor'),
    path('dataentrylogin', views.login_dataentry, name='login_dataentry'),

    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    

    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('patient/<int:patient_id>', views.doctor_view_patient,name='patient'),

    path('admin-doctor', views.admin_doctor_view,name='admin-doctor'),
    path('admin-view-doctor', views.admin_view_doctor_view,name='admin-view-doctor'),
    path('delete-doctor-from-hospital/<int:pk>', views.delete_doctor_from_hospital_view,name='delete-doctor-from-hospital'),
    path('update-doctor/<int:pk>', views.update_doctor_view,name='update-doctor'),
    path('admin-add-doctor', views.admin_add_doctor_view,name='admin-add-doctor'),
    path('admin-approve-doctor', views.admin_approve_doctor_view,name='admin-approve-doctor'),
    path('approve-doctor/<int:pk>', views.approve_doctor_view,name='approve-doctor'),
    path('reject-doctor/<int:pk>', views.reject_doctor_view,name='reject-doctor'),
    path('admin-view-doctor-specialisation',views.admin_view_doctor_specialisation_view,name='admin-view-doctor-specialisation'),

    path('admin-patient', views.admin_patient_view,name='admin-patient'),
    path('admin-view-patient', views.admin_view_patient_view,name='admin-view-patient'),
    path('delete-patient-from-hospital/<int:pk>', views.delete_patient_from_hospital_view,name='delete-patient-from-hospital'),
    path('update-patient/<int:pk>', views.update_patient_view,name='update-patient'),
    path('admin-add-patient', views.admin_add_patient_view,name='admin-add-patient'),
    path('admin-approve-patient', views.admin_approve_patient_view,name='admin-approve-patient'),
    path('approve-patient/<int:pk>', views.approve_patient_view,name='approve-patient'),
    path('reject-patient/<int:pk>', views.reject_patient_view,name='reject-patient'),
    path('admin-discharge-patient', views.admin_discharge_patient_view,name='admin-discharge-patient'),
    path('discharge-patient/<int:pk>', views.discharge_patient_view,name='discharge-patient'),
    path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),

    path('admin-appointment', views.admin_appointment_view,name='admin-appointment'),
    path('admin-view-appointment', views.admin_view_appointment_view,name='admin-view-appointment'),
    path('admin-add-appointment', views.admin_add_appointment_view,name='admin-add-appointment'),
    path('admin-approve-appointment', views.admin_approve_appointment_view,name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment_view,name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment_view,name='reject-appointment'),


    
]
'''

# --- For intial URLs (by Pranav) ---
urlpatterns = [
    path('',views.home_view,name=''),
    path('admin/', admin.site.urls),
    path('frontdesklogin', views.login_frontdesk, name='login_frontdesk'),
    path('doctorlogin', views.login_doctor, name='login_doctor'),
    path('dataentrylogin', views.login_dataentry, name='login_dataentry'),
    path('logout', views.logout_view,name='logout'),
    path('doctorclick', views.doctorclick_view),
    path('frontdeskclick', views.frontdeskclick_view),
    path('dataentryclick', views.dataentryclick_view),
    path('adminclick', views.adminclick_view),
    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),
]

# --- FOR FrontDesk Related URLs (by Pranav) ---
urlpatterns += [
    path('frontdesk-dashboard', views.frontdesk_dashboard, name='frontdesk-dashboard'),
    path('frontdesk-add-patient', views.frontdesk_add_patient, name='frontdesk-add-patient'),
    path('frontdesk-schedule-appointment', views.frontdesk_schedule_appointment, name='frontdesk-schedule-appointment'),
    path('frontdesk-schedule-test', views.frontdesk_schedule_tests, name='frontdesk-schedule-test'),
    path('frontdesk-schedule-test/<int:test_id>', views.frontdesk_schedule_tests, name='frontdesk-schedule-test'),
    path('frontdesk-admit-patient/<int:patient_id>', views.frontdesk_admit_patient, name='frontdesk-admit-patient'),
    path('frontdesk-discharge-patient/<int:patient_id>', views.frontdesk_discharge_patient, name='frontdesk-discharge-patient'),
]

# --- FOR Doctor Related URLs (by Pranav) ---
urlpatterns += [
    path('doctor-dashboard', views.doctor_dashboard, name='doctor-dashboard'),
    path('doctor-view-patient/<int:patient_id>', views.doctor_view_patient, name='doctor-view-patient'),
    path('doctor-prescribe-meds/<int:patient_id>', views.doctor_prescribe_medicine,name='doctor-prescribe-meds'),
    path('doctor-prescribe-tests/<int:patient_id>', views.doctor_prescribe_test,name='doctor-prescribe-test'),
    path('doctor-notifications', views.doctor_notification, name='doctor-notifications'),
]

# --- FOR DataEntry Related URLs (by Pranav) ---
urlpatterns += [
    path('dataentry-dashboard', views.dataentry_dashboard,name='dataentry-dashboard'),
    path('dataentry/<int:id>/<str:name>', views.add_test_results, name='add_test_results')
]


# #---------FOR DOCTOR RELATED URLS-------------------------------------
# urlpatterns +=[
#     path('doctor-dashboard', views.doctor_dashboard,name='doctor-dashboard'),
#     path('search', views.search_view,name='search'),

#     path('doctor-patient', views.doctor_patient_view,name='doctor-patient'),
#     path('doctor-view-patient', views.doctor_view_patient_view,name='doctor-view-patient'),
#     path('doctor-view-discharge-patient',views.doctor_view_discharge_patient_view,name='doctor-view-discharge-patient'),
#     path('doctor-prescribe-meds/<int:patient_id>', views.doctor_prescribe_medicine,name='doctor-prescribe-meds'),
#     path('doctor-prescribe-tests/<int:patient_id>', views.doctor_prescribe_test,name='doctor-prescribe-test'),
#     path('doctor-appointment', views.doctor_appointment_view,name='doctor-appointment'),
#     path('doctor-view-appointment', views.doctor_view_appointment_view,name='doctor-view-appointment'),
#     path('doctor-delete-appointment',views.doctor_delete_appointment_view,name='doctor-delete-appointment'),
#     path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),
# ]
