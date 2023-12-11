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
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    user_count = User.objects.count()
    context = {'user_count': user_count}
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
            search = filterform.cleaned_data['exercise_name']
            selected_muscle = filterform.cleaned_data['exercise_muscle_group']
            selected_type = filterform.cleaned_data['exercise_type']
            selected_difficulty = filterform.cleaned_data['exercise_difficulty']

            exercises = api.get_exercises(name=search, muscle=selected_muscle, e_type=selected_type, difficulty=selected_difficulty, pages=3)
            context['exercises'] = exercises
        
    return render(request, 'exercises/exercises.html', context)


def read_workout(request):
    if request.method == 'POST':
        workout_id = request.POST.get('workout_id', None)
        user_id = request.user.id
        print(user_id, workout_id)
        workout = Workout.objects.get(id=workout_id, user=user_id)
        workout_details = workout.get_workout_details()
        return JsonResponse({'workout': workout_details})




    
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
    form = WorkoutForm(request.POST or None)
    user_profile = request.user.userprofile
    
    if request.method == 'POST':
        action = request.POST.get('action')

        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user.userprofile 
            workout.save()

            print(f"User's fitness goal: {user_profile.fitness_goal}")

            if action == 'auto-generate':
                for muscle_group in user_profile.focused_muscle_groups:
                    exercises = api.get_exercises(muscle=muscle_group)
                    if exercises:
                        for exercise in exercises[:2]:  # Get the first two exercises
                            sets, reps, rest_time = 0, 0, 0

                            if user_profile.fitness_goal == 'Get Stronger':
                                sets, reps, rest_time = 4, 5, 4
                                
                            if user_profile.fitness_goal == 'Gain Muscle':
                                sets, reps, rest_time = 3, 8, 2
                                
                            if user_profile.fitness_goal == 'Lose Fat':
                                sets, reps, rest_time = 3, 12, 1

                            ExerciseInWorkout.objects.create(
                                workout=workout,
                                name=exercise['name'],
                                sets=sets,
                                reps=reps,
                                weight=None,
                                rest_time=rest_time,
                                notes=''
                            )

            return redirect('workouts')
        
    context = {
        'form': form,
        'user_profile': user_profile,
    }
    return render(request, 'workouts/workout-form.html', context)
        
    context = {
        'form': form,
        'user_profile': user_profile,
    }
    return render(request, 'workouts/workout-form.html', context)

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

@login_required
def view_workout(request, workout_id):
     # make id 0-indexed
    workout_id -= 1
    if workout_id < 0:
        raise Http404()

    workouts = list(Workout.objects.filter(user=request.user.id))
    try:
        workout = workouts[workout_id]
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
        raise Http404()
    
    context = {
        'workout': workout,
        'exercises': exercises_in_workout
    }
    return render(request, 'workouts/workout.html', context=context)


@login_required
def delete_exercise_in_workout(request, workout_id):
    if request.method == 'POST':
        exercise = ExerciseInWorkout.objects.get(id=workout_id)
        workout_id = exercise.workout.id
        user = request.user.id
        # check if workout belongs to user
        workout = Workout.objects.get(id=workout_id, user=user)
        if workout:
            exercise.delete()
        workouts = list(Workout.objects.filter(user=request.user.id))
        workout_index = workouts.index(workout) + 1
        print(workout_index)
    return redirect('view_workout', workout_index)

@login_required
def create_exercise_in_workout(request, exercise_name):
    form = ExerciseInWorkoutForm(request.POST or None, user=request.user)
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



def error_404(request, *args, **kwargs):
    context = {"error": "404"}
    response = render(request, 'error.html', context=context)
    response.status_code = 404
    return response


def error_500(request, *args, **kwargs):
    context = {"error": "500"}
    response = render(request, 'error.html', context=context)
    response.status_code = 500
    return response