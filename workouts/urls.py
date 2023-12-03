from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('exercises', views.exercises, name='exercises'),
    path('exercises/<str:exercise_name>', views.exercise_detail, name='exercise_detail'),
    path('workouts/', views.read_workouts, name='read_workouts'),
    path('workouts/create', views.create_workout, name='create_workout'),
    path('workouts/update/<int:id>', views.update_workout, name='update_workout'),
    path('workouts/delete/<int:id>', views.delete_workout, name='delete_workout'),
    path('workouts/<str:workout_name>', views.workout, name='workout_detail'),
]