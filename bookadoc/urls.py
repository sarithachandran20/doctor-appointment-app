from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('homepage',homepage,name='home'),
    path('register',registeruser,name='reg'),
    path('login',loginpage,name='login'),
    path('logout',logoutpage,name='logout'),
    path('staffreg',staff_register,name='staff_register'),

    path('searchdoctors/<dep>',search_doctors,name='search_doctors'),
    path('patientprofile',patient_profile,name='patient_profile'),
    path('editpatientprofile',edit_patient_profile,name='edit_patientprofile'),
    path('appointments',appointments,name='appointments'),
    path('createbooking/<int:uid>',createbooking,name='createbooking'),
    
    path('doctorpage',doctor_home,name='doctor_home'),
    path('doctorprofile',doctor_profilepage,name='doctor_profile'),
    path('edit_doctorprofile',edit_doctor_profile,name='edit_doctor_profile'),
    path('mybookings',mybookings,name='mybookings'),
    path('manageappointments',manage_appointments,name='manage_appointments'),
    path('approvebooking/<int:bid>',aprove_booking,name='aprove_booking'),
    path('rejectbooking/<int:bid>',reject_booking,name='reject_booking'),
    path('scheduled_appointment',scheduled_appointments,name='scheduled_appointments'),
   
    path('admindashboard',admin_dashboard,name='admin_dashboard'),
    path('aproveprofile/<int:doc_id>',aprove_profile,name='aprove_profile'),
    path('rejectprofile/<int:doc_id>',reject_profile,name='reject_profile'),
    path('aprovedprofiles',aproved_doctor_profiles,name='aproved_profiles'),
    path('rejectedprofiles',rejected_doctor_profiles,name='rejected_profiles'),
    path('alldoctors',all_doctors,name='alldoctors'),
    path('managedoctors',manage_doctors,name='manage_doctors'),
    path('profileverification',profile_verification,name='profile_verification'),
    path('allpatients',all_patients,name='allpatients'),
    path('managepatients',manage_patients,name='manage_patients'),
    path('viewpatient/<int:p_id>',view_patient,name='view_patient'),
    path('allappointments',all_appointments,name='all_appointments'),
    path('manageallappointments',manage_all_appointments,name='manage_all_appointments'),
    path('aprovedpatients',aproved_patients,name='aproved_patients'),
    path('rejctedpatients',rejected_patients,name='rejected_patients'),
    path('deleteappointment/<int:appointment_id>',delete_appointment,name='delete_appointment'),
    path('deletedoctor/<int:doctor_id>',delete_doctor,name='delete_doctor'),
    path('doctors_list',doctors_list,name='doctors_list'),
    path('deletepatient/<int:patient_id>',delete_patient,name='delete_patient'),
    path('viewdoctor/<int:doc_id>',view_doctor,name='view_doctor'),
    
    path('feedback',feedback,name='feedback'),
    path('feedbacklist',feedback_list,name='feedback_list')

   
]

