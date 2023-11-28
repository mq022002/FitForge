from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fitness_goal = models.CharField(max_length=255, choices=[
        ('Get Stronger', 'Get Stronger'),
        ('Gain Muscle', 'Gain Muscle'),
        ('Lose Fat', 'Lose Fat'),
    ])
    
    frequency = models.IntegerField(choices=[
        (1, '1 day per week'),
        (2, '2 days per week'),
        (3, '3 days per week'),
        (4, '4 days per week'),
        (5, '5 days per week'),
        (6, '6 days per week'),
        (7, '7 days per week'),
    ], default=1)
    
    workout_duration = models.IntegerField(default=0)
    overall_intensity = models.CharField(max_length=255, choices=[
        ('High Intensity', 'High Intensity'),
        ('Medium Intensity', 'Medium Intensity'),
        ('Low Intensity', 'Low Intensity'),
    ])
    
    focused_muscle_groups = models.JSONField(default=list)
    
    def __str__(self):
        return self.user.username