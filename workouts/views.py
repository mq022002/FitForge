from django.shortcuts import render
from django.http import HttpResponse
import requests
from . import api

# Create your views here.

def home(request):
    # return HttpResponse("Hello, Django!")
    context = {'name': 'John'}
    return render(request, 'home.html', context)

def exercises(request):
    type_list = api.get_exercise_types()
    muscle_list = api.get_exercise_muscles()
    difficulty_list = api.get_exercise_difficulties()

    exercise_list = ""
    if request.method == 'POST':
        # Use the .get() method with a default value of None
        selected_muscle = request.POST.get('muscle', None)
        selected_type = request.POST.get('type', None)
        selected_difficulty = request.POST.get('difficulty', None)

        print(selected_muscle)
        print(selected_type)
        print(selected_difficulty)
        exercise_list = api.get_exercises(selected_muscle, selected_type, selected_difficulty, 0)



    context = {
        'muscles': muscle_list,
        'types': type_list,
        'difficulties': difficulty_list,
        'exercises': exercise_list
    }
    return render(request, 'exercises.html', context)
