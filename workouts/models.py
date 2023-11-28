from django.db import models

class Exercise(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, null=True)
    muscle = models.CharField(max_length=255, null=True)
    equipment = models.CharField(max_length=255, null=True)
    difficulty = models.CharField(max_length=255, null=True)
    instructions = models.TextField()

    def __str__(self):
        return self.name

class ExerciseInWorkout(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    workout = models.ForeignKey('Workout', on_delete=models.CASCADE)
    sets = models.IntegerField(default=0)
    reps = models.IntegerField(default=0)
    weight = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True)

class Workout(models.Model):
    exercises = models.ManyToManyField(Exercise, through=ExerciseInWorkout)