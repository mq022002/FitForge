from django.db import models
from users.models import UserProfile

class Exercise(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, null=True)
    muscle = models.CharField(max_length=255, null=True)
    equipment = models.CharField(max_length=255, null=True)
    difficulty = models.CharField(max_length=255, null=True)
    instructions = models.TextField()

    def __str__(self):
        return self.name

class Workout(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(UserProfile, to_field='user_id', on_delete=models.CASCADE)
    notes = models.TextField(blank=True)

class ExerciseInWorkout(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    workout_id = models.ForeignKey(Workout, on_delete=models.CASCADE)
    sets = models.IntegerField(default=0)
    reps = models.IntegerField(default=0)
    weight = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True)
