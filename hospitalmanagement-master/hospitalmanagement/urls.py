
from django.contrib import admin
from django.urls import path
from hospital import views
from django.contrib.auth.views import LoginView,LogoutView
from django.conf import settings
from django.conf.urls.static import static

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
    path('view-image/media/Test_Results/<str:url>', views.doctor_view_image, name='doctor-view-image')
]

# --- FOR DataEntry Related URLs (by Pranav) ---
urlpatterns += [
    path('dataentry-dashboard', views.dataentry_dashboard,name='dataentry-dashboard'),
    path('dataentry/<int:id>', views.add_test_results, name='add_test_results')
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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)