from django.contrib import admin
from .models import Exercise, UserProfile, Workout, ExerciseInWorkout

class ExerciseInWorkoutInline(admin.TabularInline):
    model = ExerciseInWorkout

class WorkoutAdmin(admin.ModelAdmin):
    inlines = [ExerciseInWorkoutInline]

admin.site.register(Exercise)
admin.site.register(UserProfile)
admin.site.register(Workout, WorkoutAdmin)
