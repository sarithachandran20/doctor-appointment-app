from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class PatientPro(models.Model):

    choice = (('male','male'),('female','female'))
    
    

    profile_pic = models.ImageField(upload_to='patient_photos/', blank=True,null=True)
    patient = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField(null=True)
    bio = models.TextField(blank=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=100,choices=choice)
    blood = models.CharField(max_length=50,blank=True)
    created = models.DateField(default=timezone.now)
    def __str__(self):
        return self.patient.username


class Dprofile(models.Model):

    specs = (('dentist', 'dentist'),
             ('cardiologist', 'cardiologist'),
             ('otolaryngologist', 'otolaryngologist'),
             ('orthopedist','orthopedist'),
             ('pediatrics','pediatrics'),
             ('ophthalmologist','ophthalmologist'),
             ('gynecologist','gynecologist'),
             ('dermatologist','dermatologist'),
             ('neurologist','neurologist'),
             ('psychiatrist','psychiatrist'),
             )
    
    choice = (('male','male'),('female','female'))

    permision = (('aproved','aproved'),('rejected','rejected'),('pending','pending'))
    
    profile_pic = models.ImageField(upload_to='doctors_photos/',null=True,blank=True)
    doctor = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100,blank=True)
    phone = models.IntegerField(null=True)
    bio = models.TextField(blank=True)
    specilization = models.CharField(max_length=300, choices=specs,blank=True)
    qualifications = models.CharField(max_length=50,blank=True)
    gender = models.CharField(max_length=50,choices=choice)
    profile_status =  models.CharField(max_length=100,choices=permision,default='pending')
    location = models.CharField(max_length=100,blank=True,null=True)
    clinic_name = models.CharField(max_length=100,blank=True)
    clinic_address = models.TextField(blank=True)
    consultation_days = models.CharField(max_length=100,blank=True,null=True)
    consultation_fee = models.IntegerField(null=True)
    created = models.DateField(default=timezone.now)
    def __str__(self):
        return self.doctor.username
    
    
 


class Bookings(models.Model):

    status = (('approved', 'approved'),
              ('pending', 'pending'),
              ('rejected', 'rejected'),)
    choice = (('completed','completed'),
               ('absent','absent'),
               ('pending','pending'))

    patient = models.ForeignKey(User, on_delete=models.CASCADE,related_name='patient')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE,related_name='doctor')
    Name = models.CharField(max_length=50,blank=True,default='your name',null=True)
    Phone = models.CharField(max_length=12,null=True,default='contact number')
    Email = models.EmailField(default='example@gmail.com')
    booking_time = models.DateField()
    description = models.TextField(blank=True)
    booking_status = models.CharField(default='pending',choices=status,max_length=100)
    treatment_status = models.CharField(max_length=100,choices=choice,default='pending')


class Feedback(models.Model):
    FEEDBACK_TYPE_CHOICES = [
        ('feedback', 'Feedback'),
        ('complaint', 'Complaint'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPE_CHOICES)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.feedback_type}"