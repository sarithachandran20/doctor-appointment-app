from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import *

# Create your views here.

# register for patient

def registeruser(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = False
            user.save()
            PatientPro.objects.create(patient = user)
            messages.success(request,'user has been created')
            subject = 'welcome mail'
            message = f'welcome to BookADoc website {user.username}'
            from_mail = settings.EMAIL_HOST_USER
            to_mail = [user.email]
            send_mail(
                subject,message,from_mail,to_mail
            )
            login(request, user)
            return redirect('home')
    else:
        form = RegForm()
    return render(request, 'register.html', {'form': form})

# patient profilepage

def patient_profile(request):
    usr = request.user
    pro = PatientPro.objects.get(patient = usr)
    booking = Bookings.objects.filter(patient = usr)
    return render(request,'patient_profile.html',{'pro':pro,'booking':booking})

def edit_patient_profile(request):
    usr = request.user
    pro = PatientPro.objects.get(patient = usr)
    
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES,instance=pro)
        if form.is_valid():
            form.save()
            return redirect(patient_profile)
    else:
        form = PatientForm(instance=pro)

    return render(request, 'edit_patient_profile.html', {'form': form,'pro':pro})

# register for doctors

def staff_register(request):
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True  # Mark the user as staff
            user.save()
            Dprofile.objects.create(doctor=user)
            messages.success(request,'user has been created')
            subject = 'welcome mail'
            message = f'welcome to BookADoc website {user.username}'
            from_mail = settings.EMAIL_HOST_USER
            to_mail = [user.email]
            send_mail(
                subject,message,from_mail,to_mail
            )
            return redirect('login')  # Redirect to login or dashboard
    else:
        form = StaffRegistrationForm()
    return render(request, 'register_staff.html', {'form': form})

# loginpage for users

def loginpage(request):
    if request.method == 'POST':
        usern = request.POST.get('username')
        passw = request.POST.get('password')

        user = authenticate(request, username=usern, password=passw)
        print(user)

        if user:
            login(request, user)
            if user.is_superuser:
                return redirect(admin_dashboard)
            elif user.is_staff:
                return redirect('doctor_home')
            
            else:
                return redirect('home')

        else:
            print('no such user')

        # print(username, password)

    return render(request, 'login.html')


def logoutpage(request):
    logout(request)
    #messages.success(request, 'user is logged out')
    return redirect(homepage)

# homepage for doctors

def doctor_home(request):
    user = request.user
    if user.is_staff:
        bookings = Bookings.objects.filter(doctor=user, booking_status='pending')
        doc = Dprofile.objects.get(doctor = user) 
        return render(request, 'doctor_home.html', {'bookings': bookings,'doc':doc})
    else:
        return HttpResponse('you are not authosrised to view this page')

def doctor_dashboard(request):

    return render(request,'doctor_dashboard.html')


def doctor_profilepage(request):
    usr = request.user
    pro = Dprofile.objects.get(doctor = usr)
    booking = Bookings.objects.filter(doctor = usr)
    return render(request,'doctor_profile.html',{'pro':pro,'booking':booking})

def edit_doctor_profile(request):
    usr = request.user
    pro = Dprofile.objects.get(doctor = usr)
    
    if request.method == 'POST':
        form = DoctorForm(request.POST,request.FILES,instance=pro)
        if form.is_valid():
            form.save()
            return redirect('doctor_profile')
        else:
            print(form.errors)
    else:
        form = DoctorForm(instance=pro)

    return render(request, 'edit_doctor_profile.html', {'form': form,'pro':pro})


def homepage(request):                 
        
        return render(request,'home.html')


def search_doctors(request,dep):

        form = search_by_location(request.POST)
        doctors = Dprofile.objects.filter(profile_status = 'aprove' , specilization = dep)
        
        
        if form.is_valid():
            location = form.cleaned_data.get('location')
            if location:
                doctors = doctors.filter(location__icontains=location)              
        
        return render(request,'search_doctors.html',{'form':form,'doctors':doctors})


def appointments(request):

    return render(request,'appointment.html')



def createbooking(request, uid):
    doctor = User.objects.get(id=uid)
    pro = PatientPro.objects.get(patient = request.user)
    patient = request.user
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.patient = patient
            a.doctor = doctor
            a.phone = pro.phone
            a.email = pro.patient.email
            a.save()
            return redirect(mybookings)
        else:   
            print("Form is NOT valid")
            print(form.errors)
    else:
        form = BookingForm()
    return render(request, 'create_booking.html', {'form': form,'pro':pro})


@login_required
def mybookings(request):
    user = request.user
    if not user.is_staff:

        bookings = Bookings.objects.filter(patient=user)
    

        return render(request, 'mybookings.html', {'bookings': bookings})


def manage_appointments(request):
    user = request.user
    if not user.is_superuser:
       bookings = Bookings.objects.filter(booking_status = 'pending',doctor = user)
       return render(request,'manage_appointment.html',{'bookings':bookings})

def aprove_booking(request, bid):
    booking = Bookings.objects.get(id=bid)
    booking.booking_status = 'aproved'
    booking.save()
    return redirect(doctor_home)

def reject_booking(request, bid):
    booking = Bookings.objects.get(id=bid)
    booking.booking_status = 'reject'
    booking.save()
    return redirect(doctor_home)

def scheduled_appointments(request):
    bookings = Bookings.objects.filter(booking_status = 'aproved')
    return render(request,'scheduled_appointments.html',{'bookings':bookings})

def admin_dashboard(request):
    doctor_count = Dprofile.objects.all().count()
    patient_count = PatientPro.objects.all().count()
    appointment_count = Bookings.objects.all().count()
    return render(request,'admin_dashboard.html',{'doctor_count':doctor_count,'patient_count':patient_count,
                                                  'appointment_count':appointment_count})

def manage_doctors(request):

    return render(request,'manage_doctors.html')

def aprove_profile(request,doc_id):
    doc = Dprofile.objects.get(id=doc_id)
    doc.profile_status = 'aprove'
    doc.save()
    return redirect(admin_dashboard)

def reject_profile(request,doc_id):
    doc = Dprofile.objects.get(id=doc_id)
    doc.profile_status = 'reject'
    doc.save()
    return redirect(admin_dashboard) 

def rejected_doctor_profiles(request):

    doc =Dprofile.objects.filter(profile_status = 'reject')

    return render(request,'rejected_profiles.html',{'doc':doc})

def aproved_doctor_profiles(request):

    doc = Dprofile.objects.filter(profile_status = 'aprove')

    return render(request,'aproved_profiles.html',{'doc':doc})

def all_doctors(request):

    doc = Dprofile.objects.all()

    return render(request, 'alldoctors.html',{'doc':doc})

def profile_verification(request):
    
    doc = Dprofile.objects.filter(profile_status ='pending')
    return render(request,'profile_verification.html',{'doc':doc})

def all_patients(request):

    patients = PatientPro.objects.all()
    return render(request,'all_patients.html',{'patients':patients})

def manage_patients(request):

    patients = PatientPro.objects.all()
    
    return render(request,'manage_patients.html',{'patients':patients})

def view_patient(request,p_id):
    
    pro = PatientPro.objects.get(id = p_id)
    
    return render(request,'view_patient.html',{'pro':pro})

def view_doctor(request,doc_id):
    
    pro = Dprofile.objects.get(id = doc_id)
    
    return render(request,'view_doctor.html',{'pro':pro})
 

def all_appointments(request):

    appointments = Bookings.objects.all()
    return render(request,'all_appointments.html',{'appointments':appointments})

def manage_all_appointments(request):

    appointments = Bookings.objects.all()
    return render(request,'manage_all_appointments.html',{'appointments':appointments})


def aproved_patients(request):

    patients = Bookings.objects.filter(booking_status = 'aproved')

    return render(request,'aproved_patients.html',{'patients':patients})

def rejected_patients(request):

    patients = Bookings.objects.filter(booking_status = 'reject')

    return render(request,'rejected_patients.html',{'patients':patients})

def delete_appointment(request, appointment_id):
    appointment = Bookings.objects.get(id=appointment_id)
    appointment.delete()
    # messages.success(request, "Appointment deleted successfully.")
    return redirect('admin_appointment_list')


def doctors_list(request):
    doc = Dprofile.objects.all()
    return render(request,'delete_doctor.html',{'doc':doc})

def delete_doctor(request, doctor_id):
    doc = Dprofile.objects.get(id=doctor_id)
    doc.delete()
    # messages.success(request, "Appointment deleted successfully.")
    return redirect('admin_dashboard')

def delete_patient(request, patient_id):
    p = Dprofile.objects.get(id=patient_id)
    p.delete()
    # messages.success(request, "Appointment deleted successfully.")
    return redirect('admin_dashboard')


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            # messages.success(request, 'Feedback submitted successfully!')
            return redirect('home') 
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})

def feedback_list(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'feedback_list.html', {'feedbacks': feedbacks})