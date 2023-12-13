from django.contrib import admin
from .models import Workout, ExerciseInWorkout

class ExerciseInWorkoutInline(admin.TabularInline):
    model = ExerciseInWorkout

class WorkoutAdmin(admin.ModelAdmin):
    inlines = [ExerciseInWorkoutInline]

admin.site.register(Workout, WorkoutAdmin)
