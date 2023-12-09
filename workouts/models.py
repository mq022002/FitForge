from django.db import models
from users.models import UserProfile


class Workout(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(UserProfile, to_field='user_id', on_delete=models.CASCADE)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ExerciseInWorkout(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    sets = models.IntegerField(default=0)
    reps = models.IntegerField(default=0)
    weight = models.FloatField(null=True, blank=True)
    rest_time = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
