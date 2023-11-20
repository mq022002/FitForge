from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


# Create your views here.
@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def change_password(request):
    return render(request, 'registration/password_change.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
    return render(request, 'registration/login.html')