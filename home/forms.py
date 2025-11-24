from django import forms
from .models import Track, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['name', 'sets', 'reps', 'weight', 'muscle_group']

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['age', 'height', 'weight','gender','activity_level',]

class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField(required=True)
    class Meta:
        model=User
        fields=['username','email','password1','password2']