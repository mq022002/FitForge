from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('exercises/', views.view_exercises, name='exercises'),

    path('workouts/', views.workouts, name='workouts'),
    path('workouts/view/<int:workout_index>', views.view_workout, name='view_workout'),
    path('workouts/create', views.create_workout, name='create_workout'),
    path('workouts/update/<int:workout_index>', views.update_workout, name='update_workout'),
    path('workouts/delete/<int:workout_index>', views.delete_workout, name='delete_workout'),
    path('workouts/<str:workout_name>', views.workout, name='workout_detail'),
    path('workout/read', views.read_workout, name='read_workout'),

    path('exercise-in-workout/create/<str:exercise_name>/', views.create_exercise_in_workout, name='create_exercise_in_workout'),
    path('exercise-in-workout/delete/<int:exercise_in_workout_id>', views.delete_exercise_in_workout, name='delete_exercise_in_workout'),
    path('exercise-in-workout/update/<int:exercise_in_workout_id>', views.update_exercise_in_workout, name='update_exercise_in_workout')
]