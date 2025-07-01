from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . models import *


# registration form for patient

class RegForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# registration form for doctor

class StaffRegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class DoctorForm(forms.ModelForm):
    class Meta:
        model = Dprofile
        exclude = ['doctor','profile_status','created']
        


class PatientForm(forms.ModelForm):
    class Meta:
        model = PatientPro
        exclude = ['patient','created']
    

class search_by_location(forms.Form):
             
        location = forms.CharField(required=False, label='Search by Location')
        

class BookingForm(forms.ModelForm):

    class Meta:
        model = Bookings
        fields = ['Name','booking_time','description']
        widgets = {
            'booking_time': forms.DateInput(attrs={'type': 'date'}),
            
        }

    

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback_type', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }