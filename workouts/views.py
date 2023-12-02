from typing import Any
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import requests
from . import api
from django.views.generic import ListView, DetailView
from .models import *

# Create your views here.

def home(request):
    # return HttpResponse("Hello, Django!")
    context = {'name': 'John'}
    return render(request, 'home.html', context)

def exercises(request):
    type_list = api.exercise_types
    muscle_list = api.exercise_muscles
    difficulty_list = api.exercise_difficulties

    exercise_list = ""
    if request.method == 'POST':
        # Use the .get() method with a default value of None
        selected_muscle = request.POST.get('muscle', None)
        selected_type = request.POST.get('type', None)
        selected_difficulty = request.POST.get('difficulty', None)
        exercise_list = api.get_exercises(muscle=selected_muscle, e_type=selected_type, difficulty=selected_difficulty, pages=3)

        # Remove backslashes from exercise names
        # To prevent errors in routes
        # for exercise in exercise_list:
        #     exercise['name'] = exercise['name'].replace('/', ' ')
        #     exercise['equipment'] = exercise['equipment'].replace('_', ' ').capitalize()
        #     exercise['muscle'] = exercise['muscle'].replace('_', ' ').capitalize()
        #     exercise['type'] = exercise['type'].replace('_', ' ').capitalize()
        #     exercise['difficulty'] = exercise['difficulty'].capitalize()
    

    context = {
        'muscles': muscle_list,
        'types': type_list,
        'difficulties': difficulty_list,
        'exercises': exercise_list
    }
    return render(request, 'exercises.html', context)

def exercise_detail(request, exercise_name):
    exercise = api.get_exercises(name=exercise_name)[0]
    video = api.fetch_youtube_link(exercise['name'])
    if(video):
        url = "https://www.youtube.com/embed/" + video['id']
        context = {
            'exercise': exercise,
            'url': url
        }
    else:
        context = {
            'exercise': exercise,
        }

    return render(request, 'exercise_detail.html', context)

    
def workouts(request):
    user_id = request.user.id
    print(user_id)
    workouts = Workout.objects.get(user=user_id)
    context = { 'workouts': workouts }
    print(context)
    return render(request, 'workout.html', context=context)


def workout(request, workout_name):
    user_id = request.user.id
    print(workout_name)
    #workout_id = Workout.objects.get(name=workout, user=user_id).id
    workout_id = get_object_or_404(Workout, name=workout_name, user=user_id).id
    print(workout_id)
    workout = ExerciseInWorkout.objects.filter(workout_id=workout_id)
    context = {'workout': workout}
    return render(request, 'workout.html', context=context)
