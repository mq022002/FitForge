from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('exercises/', views.exercises, name='exercises'),
    path('exercises/read', views.read_exercises, name='read_exercises'),
    path('exercises/<str:exercise_name>', views.exercise_detail, name='exercise_detail'),

    path('workouts/', views.workouts, name='workouts'),
    path('workouts/create', views.create_workout, name='create_workout'),
    path('workouts/update/<int:id>', views.update_workout, name='update_workout'),
    path('workouts/delete/<int:id>', views.delete_workout, name='delete_workout'),
    path('workouts/<str:workout_name>', views.workout, name='workout_detail'),
    
    path('workout/read', views.read_workout, name='read_workout'),
]