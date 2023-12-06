from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from . import api
from django.views.generic import ListView, DetailView, TemplateView
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import WorkoutForm
from django.http import HttpResponse
import json
# Create your views here.

def home(request):
    # return HttpResponse("Hello, Django!")
    context = {'name': 'John'}
    return render(request, 'home.html', context)


def exercises(request):
    type_list = api.exercise_types
    muscle_list = api.exercise_muscles
    difficulty_list = api.exercise_difficulties

    workouts = Workout.objects.filter(user=request.user.id)
    workout_list = []
    for workout in workouts:
        print(workout.id)
        workout_list.append({'id': workout.id, 'name': workout.name})
    print(workout_list)

    exercise_list = ""
    if request.method == 'POST':
        if 'exercise_form' in request.POST:
            # Use the .get() method with a default value of None
            selected_muscle = request.POST.get('muscle', None)
            selected_type = request.POST.get('type', None)
            selected_difficulty = request.POST.get('difficulty', None)
            exercise_list = api.get_exercises(muscle=selected_muscle, e_type=selected_type, difficulty=selected_difficulty, pages=3)
        elif 'workout_form' in request.POST:
            workout_id = request.POST.get('workout_id', None)
            workout = _workout_exercises(workout_id, request.user.id)
            exercises = {'exercises': workout}
            return HttpResponse(json.dumps(exercises), content_type='application/json')
            #return render(request, 'exercises/exercises.html', {'exercises': exercise_list, 'workouts': workout_list})
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
        'exercises': exercise_list,
        'workout_list': workout_list
    }
    return render(request, 'exercises/exercises.html', context)

def _workout_exercises(workout_id, user_id):
    workout_id = Workout.objects.get(id=workout_id, user=user_id).id
    workout_exercises  = ExerciseInWorkout.objects.filter(workout_id=workout_id)
    exercise_list = []
    for exercise in workout_exercises:
        exercise_data = {}
        exercise_data.update(exercise.exercise_id.__dict__)
        exercise_data.update(exercise.__dict__)
        del exercise_data['_state']
        exercise_list.append(exercise_data)
    return exercise_list

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

    return render(request, 'exercises/exercise_detail.html', context)

    
@login_required
@require_POST
def workout(request, workout_name):
    user_id = request.user.id
    workout_id = get_object_or_404(Workout, name=workout_name, user=user_id).id
    workout = ExerciseInWorkout.objects.filter(workout_id=workout_id)
    context = { 'workout': workout }
    return render(request, 'workouts/workout.html', context=context)


@login_required
def read_workouts(request):
    workouts = Workout.objects.filter(user=request.user.id)
    context = { 'workouts': workouts }
    return render(request, 'workouts/workouts.html', context=context)


@login_required
def create_workout(request):
    # Create a form instance and populate it with data from the request
    form = WorkoutForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            print("valid")
            form.save()
            # return redirect('workouts')
            return redirect('read_workouts')
    # if the request does not have post data, a blank form will be rendered
    return render(request, 'workouts/workout-form.html', {'form': form})

@login_required
def update_workout(request, id):
    workout = Workout.objects.get(id=id)
    form = WorkoutForm(request.POST or None, instance=workout)
    # check whether it's valid:
    if form.is_valid():
        # update the record in the db
        form.save()
    
    return redirect('read_workouts')
    
@login_required
def delete_workout(request, id):
    workout = Workout.objects.get(id=id)

    # if this is a POST request, we need to delete the form data
    if request.method == 'POST':
        workout.delete()
        # after deleting redirect to view_product page
    return redirect('read_workouts')