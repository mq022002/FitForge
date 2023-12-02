from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('exercises', views.exercises, name='exercises'),
    path('exercises/<str:exercise_name>', views.exercise_detail, name='exercise_detail'),
    path('workouts/', views.workouts, name='workout'),
    path('workouts/<str:workout_name>', views.workout, name='workout_detail'),
]