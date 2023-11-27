from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms

class UserCreateForm(UserCreationForm):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    username = forms.CharField()
    email = forms.EmailField()
    age = forms.IntegerField()
    gender = forms.ChoiceField(choices=GENDER_CHOICES)


    class Meta:
        model = User
        fields = ['username', 'email', 'age', 'gender', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Username"}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "Email"}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Age"}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Confirm Password"}),
        }

class ChangePasswordForm(PasswordChangeForm):

    class Meta:
        model = User
        fields = '__all__'
        
        widgets = {
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Confirm Password"}),
        }