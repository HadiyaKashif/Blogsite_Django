#made our own form because the usercreationform doesn't have the email field
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta: #class meta has configurations and namespaces and is used to change the 
        #behavior of model fields like changing order options,verbose_name, and a lot of other options.
        model = User
        fields = ['username' , 'email' , 'password1' , 'password2']

class UserUpdationForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta: 
        model = User
        fields = ['username' , 'email']

class ProfileUpdationForm(forms.ModelForm):
    class Meta: 
        model = Profile
        fields = ['about','linkedIn_url','instagram_url','twitter_url','facebook_url','image']