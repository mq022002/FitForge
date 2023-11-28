from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile

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

class UserProfileForm(forms.ModelForm):
    MUSCLE_GROUP_CHOICES = [
        ('abdominals', 'Abdominals'),
        ('abductors', 'Abductors'),
        ('adductors', 'Adductors'),
        ('biceps', 'Biceps'),
        ('calves', 'Calves'),
        ('chest', 'Chest'),
        ('forearms', 'Forearms'),
        ('glutes', 'Glutes'),
        ('hamstrings', 'Hamstrings'),
        ('lats', 'Lats'),
        ('lower_back', 'Lower Back'),
        ('middle_back', 'Middle Back'),
        ('neck', 'Neck'),
        ('quadriceps', 'Quadriceps'),
        ('traps', 'Traps'),
        ('triceps', 'Triceps'),
    ]
    
    focused_muscle_groups = forms.MultipleChoiceField(
        choices=MUSCLE_GROUP_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'list-unstyled'}),
        label='Focused Muscle Groups (Select Up to 3)',
    )

    def clean_focused_muscle_groups(self):
        selected_muscle_groups = self.cleaned_data['focused_muscle_groups']

        if len(selected_muscle_groups) > 3:
            raise forms.ValidationError('Too many muscle groups selected. Please select up to 3.')

        return selected_muscle_groups

    
    class Meta:
        model = UserProfile
        fields = ['fitness_goal', 'frequency', 'workout_duration', 'overall_intensity', 'focused_muscle_groups']

        widgets = {
            'fitness_goal': forms.Select(attrs={'class': 'form-control'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
            'workout_duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'overall_intensity': forms.Select(attrs={'class': 'form-control'}),
            'focused_muscle_groups': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }