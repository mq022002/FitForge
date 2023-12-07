from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from . import api
from django.views.generic import ListView, DetailView, TemplateView
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import WorkoutForm
from django.http import HttpResponse, JsonResponse, Http404
from django.db import transaction, IntegrityError
# Create your views here.

def home(request):
    # return HttpResponse("Hello, Django!")
    context = {'name': 'John'}
    return render(request, 'home.html', context)

# Only responsible for grabbing information that should be shown when the page loads
def exercises(request):
    type_list = api.exercise_types
    muscle_list = api.exercise_muscles
    difficulty_list = api.exercise_difficulties

    workouts = Workout.objects.filter(user=request.user.id)
    workout_list = []
    for workout in workouts:
        workout_list.append({'id': workout.id, 'name': workout.name})

    context = {
        'muscles': muscle_list,
        'types': type_list,
        'difficulties': difficulty_list,
        'workout_list': workout_list
    }
    return render(request, 'exercises/exercises.html', context)


def read_exercises(request):
    if request.method == 'POST':
        # Use the .get() method with a default value of None
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

        # Process exercises to remove underscores from keys

        # Process exercises to remove underscores from keys and capitalize them

        # for i, exercise in enumerate(exercises):
        #     formatted_exercise = {key.replace('_', ' ').title(): value for key, value in exercise.items()}
        #     exercises[i] = formatted_exercise

        return JsonResponse({'exercises': exercises})


def read_workout(request):
    if request.method == 'POST':
        workout_id = request.POST.get('workout_id', None)
        user_id = request.user.id
        print(user_id, workout_id)
        workout = Workout.objects.get(id=workout_id, user=user_id)
        workout_details = workout.get_workout_details()
        return JsonResponse({'workout': workout_details})


def add_exercise(request):
    if request.method == 'POST':
        try:
            exercise_name = request.POST.get('exercise_name')
            exercise_type = request.POST.get('exercise_type')
            exercise_muscle = request.POST.get('exercise_muscle')
            exercise_equipment = request.POST.get('exercise_equipment')
            exercise_difficulty = request.POST.get('exercise_difficulty')
            exercise_instructions = request.POST.get('exercise_instructions')
            sets = request.POST.get('sets')
            reps = request.POST.get('reps')
            weight = request.POST.get('weight')
            notes = request.POST.get('notes')
            workout_id = request.POST.get('workout_id')
            # makes sure both db inserts are successful
            with transaction.atomic():
                # if exercise doesn't exist in db, add it
                if not Exercise.objects.filter(name=exercise_name).exists():
                    exercise_insert = Exercise(
                        name=exercise_name, 
                        type=exercise_type,
                        muscle=exercise_muscle,
                        equipment=exercise_equipment,
                        difficulty=exercise_difficulty,
                        instructions=exercise_instructions
                    )
                    exercise_insert.save()
                # add exercise to workout
                exercise = Exercise.objects.get(name=exercise_name)
                workout = Workout.objects.get(id=workout_id)
                exercise_in_workout = ExerciseInWorkout(
                    exercise_id=exercise,
                    workout_id=workout,
                    sets=sets,
                    reps=reps,
                    weight=weight,
                    notes=notes
                )
                exercise_in_workout.save()
        except IntegrityError:
            # if there is an error, return a bad request
            return HttpResponse(status=400)
        # return a success response
        return HttpResponse(status=200)


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
        workout = workouts[id].get_workout_details()
        for exercise in workout['exercises']:
            exercise['youtube'] = api.fetch_youtube_link(exercise['name'] + " tutorial")
        #for exercise in workout['exercises']:
        #    exercise['image'] = api.fetch_exercise_image(exercise['name'])
        print('workout: ', workout)
    except:
        print("Workout does not exist")
        raise Http404("Workout does not exist")

    context = { 'workout': workout }
    return render(request, 'workouts/workout.html', context=context)


@login_required
def delete_exercise_from_workout(request):
    if request.method == 'POST':
        exercise_id = request.POST.get('id', None)  
        exercise = ExerciseInWorkout.objects.get(id=exercise_id)
        
        workout_id = exercise.workout_id.id
        user = request.user.id
        # check if workout belongs to user
        workout = Workout.objects.get(id=workout_id, user=user)
        if workout:
            exercise.delete()
            return JsonResponse({'success': True, 'workout_id': workout_id})
        
        return JsonResponse({'success': False, 'workout_id': workout_id})

def error_404(request, *args, **kwargs):
    response = render(request, '404.html')
    response.status_code = 404
    return response


def error_500(request, *args, **kwargs):
    response = render(request, '404.html')
    response.status_code = 500
    return response