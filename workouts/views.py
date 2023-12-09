from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from . import api
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import WorkoutForm
from django.http import HttpResponse, JsonResponse, Http404
from django.db import transaction, IntegrityError
from .forms import ExerciseFilterForm, ExerciseInWorkoutForm
import json
# Create your views here.

def home(request):
    # return HttpResponse("Hello, Django!")
    context = {'name': 'John'}
    return render(request, 'home.html', context)

def view_exercises(request):
    filterform = ExerciseFilterForm(request.POST or None)
    exerciseinworkoutform = ExerciseInWorkoutForm(request.POST or None)

    context = {
        'filterform': filterform,
        'exerciseinworkoutform': exerciseinworkoutform
    }

    if request.method == 'POST':
        if filterform.is_valid():
            # Call the API with the selected options
            selected_muscle = filterform.cleaned_data['muscle_group']
            selected_type = filterform.cleaned_data['exercise_type']
            selected_difficulty = filterform.cleaned_data['difficulty']

            exercises = api.get_exercises(muscle=selected_muscle, e_type=selected_type, difficulty=selected_difficulty)
            context['exercises'] = exercises
        
    return render(request, 'exercises/exercises.html', context)

def read_workouts(request):
    workouts = Workout.objects.filter(user=request.user.userprofile)
    return JsonResponse({'workouts': workouts})

def read_exercises(request):
    if request.method == 'POST':
        # Use the .get() method with a default value of None
        # Filters
        selected_muscle = request.POST.get('muscle', None)
        selected_type = request.POST.get('type', None)
        selected_difficulty = request.POST.get('difficulty', None)
        page = request.POST.get('page', 0)

        # how many pages to fetch from api (page = 10 results)
        api_pages_to_return = 3

        # offset from api = page from request * 10 * pages to return from api
        offset = page * api_pages_to_return * 10

        # API call
        exercises = api.get_exercises(muscle=selected_muscle, e_type=selected_type, difficulty=selected_difficulty, pages=api_pages_to_return, offset=offset)


        return JsonResponse({'exercises': exercises})


def read_workout(request):
    if request.method == 'POST':
        workout_id = request.POST.get('workout_id', None)
        user_id = request.user.id
        print(user_id, workout_id)
        workout = Workout.objects.get(id=workout_id, user=user_id)
        workout_details = workout.get_workout_details()
        return JsonResponse({'workout': workout_details})


def create_exercise_in_workout(request, exercise_name):
    form = ExerciseInWorkoutForm(request.POST or None)
    context = {
        'form': form,
        'exercise_name': exercise_name
    }
    if request.method == 'POST':
        if form.is_valid():
            exercise_in_workout = form.save(commit=False)
            exercise_in_workout.name = exercise_name
            exercise_in_workout.save()
            return redirect('exercises')

    return render(request, 'exercises/create_exercise_in_workout.html', context)


# def exercise_detail(request, exercise_name):
#     try:
#         exercise = api.get_exercises(name=exercise_name)[0]
#         video = api.fetch_youtube_link(exercise['name'])
#         if(video):
#             url = "https://www.youtube.com/embed/" + video['id']
#             context = {
#                 'exercise': exercise,
#                 'url': url
#             }
#         else:
#             context = {
#                 'exercise': exercise,
#             }
#     except Exception as e:
#         print(f"Error in exercise_detail: {e}")
#         raise Http404("Invalid exercise search")
    
#     return render(request, 'exercises/exercise_detail.html', context)

    
@login_required
@require_POST
def workout(request, workout_name):
    user_id = request.user.id
    workout_id = get_object_or_404(Workout, name=workout_name, user=user_id).id
    workout = ExerciseInWorkout.objects.filter(workout_id=workout_id)
    workout_details = workout.get_workout_details()
    context = { 'workout': workout_details }
    return render(request, 'workouts/workout.html', context=context)


@login_required
def workouts(request):
    workouts = Workout.objects.filter(user=request.user.id)
    context = { 'workouts': workouts }
    return render(request, 'workouts/workouts.html', context=context)

@login_required
def create_workout(request):
    # Create a form instance and populate it with data from the request
    form = WorkoutForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user.userprofile  # Set the user from the currently authenticated user
            workout.save()
            return redirect('workouts')
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
    
    return redirect('workouts')
    
@login_required
def delete_workout(request, id):
    workout = Workout.objects.get(id=id)

    # if this is a POST request, we need to delete the form data
    if request.method == 'POST':
        workout.delete()
        # after deleting redirect to view_product page
    return redirect('workouts')


def view_workout(request, id):
    # make id 0-indexed
    id -= 1
    if id < 0:
        raise Http404("Workout does not exist")

    workouts = list(Workout.objects.filter(user=request.user.id))
    print('workouts: ', workouts)
    try:
        workout = workouts[id]
        exercises_in_workout = ExerciseInWorkout.objects.filter(workout=workout)

        for exercise in exercises_in_workout:
            exercise_detail = api.get_exercises(name=exercise.name)[0]
            exercise.type = exercise_detail['type']
            exercise.equipment = exercise_detail['equipment']
            exercise.muscle = exercise_detail['muscle']
            exercise.difficulty = exercise_detail['difficulty']
            exercise.instructions = exercise_detail['instructions']
            exercise.youtube = api.fetch_youtube_link(exercise.name + " tutorial")

    except Exception as e:
        print(e)
        raise Http404("Workout does not exist")
    
    context = {
        'workout': workout,
        'exercises': exercises_in_workout
    }
    return render(request, 'workouts/workout.html', context=context)


@login_required
def delete_exercise_in_workout(request, id):
    if request.method == 'POST':
        exercise = ExerciseInWorkout.objects.get(id=id)
        workout_id = exercise.workout.id
        user = request.user.id
        # check if workout belongs to user
        workout = Workout.objects.get(id=workout_id, user=user)
        if workout:
            exercise.delete()

    return redirect('view_workout', workout_id)

def error_404(request, *args, **kwargs):
    response = render(request, '404.html')
    response.status_code = 404
    return response


def error_500(request, *args, **kwargs):
    response = render(request, '404.html')
    response.status_code = 500
    return response