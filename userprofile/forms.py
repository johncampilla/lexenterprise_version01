from django import forms
from .models import User_Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CreateUserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'last_name', 'first_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User_Profile
        fields = ['address', 'rank', 'mobile', 'image', 'remarks']

