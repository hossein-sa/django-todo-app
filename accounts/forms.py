from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm

class UserRegisterationForm(UserCreationForm):
    username = forms.CharField(
        label="نام کاربری", 
        widget=forms.TextInput(attrs={'class': 'form-input',})
    )
    email = forms.EmailField(
        label="ایمیل", 
        widget=forms.EmailInput(attrs={'class': 'form-input',})
    )
    password1 = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(attrs={'class': 'form-input',})
    )
    password2 = forms.CharField(
        label="تکرار رمز عبور",
        widget=forms.PasswordInput(attrs={'class': 'form-input',})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    
class UserLoginForm(forms.Form):
    username = forms.CharField(
        label="نام کاربری",
        widget=forms.TextInput(attrs={'class':'from-input',})
    )
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(attrs={'class':'from-input',})
        )