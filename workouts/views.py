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
from django.http import JsonResponse
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

    #     elif 'add_exercise' in request.POST:
    #         exercise = request.POST.get('exercise', None)
    #         exercise_parameters = request.POST.get('exercise_parameters', None)
    #         workout_id = request.POST.get('workout_id', None)
    #         # if exercise doesn't exist in db, add it
    #         if not Exercise.objects.filter(name=exercise['name']).exists():
    #             exercise_insert = Exercise(
    #                 name=exercise['name'], 
    #                 type=exercise['type'],
    #                 muscle=exercise['muscle'],
    #                 equipment=exercise['equipment'],
    #                 difficulty=exercise['difficulty'],
    #                 instructions=exercise['instructions']
    #             )
    #             exercise_insert.save()
    #         # add exercise to workout
    #         exercise_id = Exercise.objects.get(name=exercise['name']).id
    #         exercise_in_workout = ExerciseInWorkout(
    #             exercise_id=exercise_id,
    #             workout_id=workout_id,
    #             sets=exercise_parameters['sets'],
    #             reps=exercise_parameters['reps'],
    #             weight=exercise_parameters['weight'],
    #             notes=exercise_parameters['notes']
    #         )
    #         exercise_in_workout.save()
    #         return HttpResponse(json.dumps({'success': True}), content_type='application/json')
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

        return JsonResponse({'exercises': exercises})


def read_workout(request):
    if request.method == 'POST':
        print("reading workout")
        # workout_id = request.POST.get('workout_id', None)
        # workout_exercises = _workout_exercises(workout_id, request.user.id)
        # return JsonResponse({'exercises': workout_exercises})
        workout_id = request.POST.get('workout_id', None)
        user_id = request.user.id
        workout = Workout.objects.get(id=workout_id, user=user_id)
        workout_details = workout.get_workout_details();
        print(workout_details)
        return JsonResponse({'workout': workout_details})


def add_exercise(request):
    if request.method == 'POST':
        try:
            exercise = request.POST.get('exercise', None)
            exercise_parameters = request.POST.get('exercise_parameters', None)
            workout_id = request.POST.get('workout_id', None)
            # makes sure both db inserts are successful
            with transaction.atomic():
                # if exercise doesn't exist in db, add it
                if not Exercise.objects.filter(name=exercise['name']).exists():
                    exercise_insert = Exercise(
                        name=exercise['name'], 
                        type=exercise['type'],
                        muscle=exercise['muscle'],
                        equipment=exercise['equipment'],
                        difficulty=exercise['difficulty'],
                        instructions=exercise['instructions']
                    )
                    exercise_insert.save()
                # add exercise to workout
                exercise_id = Exercise.objects.get(name=exercise['name']).id
                exercise_in_workout = ExerciseInWorkout(
                    exercise_id=exercise_id,
                    workout_id=workout_id,
                    sets=exercise_parameters['sets'],
                    reps=exercise_parameters['reps'],
                    weight=exercise_parameters['weight'],
                    notes=exercise_parameters['notes']
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
    context = { 'workout': workout }
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