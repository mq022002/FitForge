from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from .forms import UserProfileForm, UserCreateForm
from django.contrib.auth import update_session_auth_hash
from .models import UserProfile
from django.http import JsonResponse

# Create your views here.
@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'users/profile.html', {'form': form, 'user_profile': user_profile})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
        else:
            return render(request, 'registration/password_change.html', {'form': form, 'error': 'Invalid new password'})
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # get the user info from the form data and log in the user
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
        
    return render(request, 'registration/login.html', {'form': form})

    
def register(request):
    form = UserCreateForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    return render(request, 'registration/register.html', {'form': form})


@require_POST
def toggle_dark_mode(request):
    if request.session.get('dark_mode', False):
        request.session['dark_mode'] = False
    else:
        request.session['dark_mode'] = True
    #return JsonResponse({'dark_mode': request.session['dark_mode']})
    return redirect(request.META.get('HTTP_REFERER', 'home'))