from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def home(request):
    # return HttpResponse("Hello, Django!")
    context = {'name': 'John'}
    return render(request, 'home.html', context)

def exercises(request):
    return render(request, 'exercises.html')