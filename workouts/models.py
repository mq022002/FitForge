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

    def get_workout_details(self):
        details = {
            'name': self.name,
            'notes': self.notes,
            'exercises': []
        }
        exercises_in_workout = ExerciseInWorkout.objects.filter(workout_id=self)
        for exercise in exercises_in_workout:
            exercise_detail = exercise.exercise_id
            details['exercises'].append({
                'name': exercise_detail.name,
                'sets': exercise.sets,
                'reps': exercise.reps,
                'weight': exercise.weight,
                'exercise_notes': exercise.notes
            })
        return details

    def __str__(self):
        workout_info = f"Workout Name: {self.name}, Notes: {self.notes}"
        exercises_in_workout = ExerciseInWorkout.objects.filter(workout_id=self)

        exercises_info = []
        for exercise in exercises_in_workout:
            exercise_detail = exercise.exercise_id
            exercises_info.append(f"Exercise: {exercise_detail.name}, Sets: {exercise.sets}, Reps: {exercise.reps}, Weight: {exercise.weight}, Notes: {exercise.notes}")

        return workout_info + "\n" + "\n".join(exercises_info)


class ExerciseInWorkout(models.Model):
    exercise_id = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    workout_id = models.ForeignKey(Workout, on_delete=models.CASCADE)
    sets = models.IntegerField(default=0)
    reps = models.IntegerField(default=0)
    weight = models.FloatField(null=True, blank=True)
    rest_time = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
