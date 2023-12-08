from django import forms
from .models import Workout

EXERCISE_MUSCLE_GROUP_CHOICES = [
    ('abdominals', 'Abdominals'),
    ('abductors', 'Abductors'),
    ('adductors', 'Adductors'),
    ('biceps', 'Biceps'),
    ('calves', 'Calves'),
    ('chest', 'Chest'),
    ('forearms', 'Forearms'),
    ('glutes', 'Glutes'),
    ('hamstrings', 'Hamstrings'),
    ('lats', 'Lats'),
    ('lower_back', 'Lower Back'),
    ('middle_back', 'Middle Back'),
    ('neck', 'Neck'),
    ('quadriceps', 'Quadriceps'),
    ('traps', 'Traps'),
    ('triceps', 'Triceps'),
]

EXERCISE_TYPE_CHOICES = {
    "": "None",
    # "cardio": "Cardio",
    # "olympic_weightlifting": "Olympic Weightlifting",
    # "plyometrics": "Plyometrics",
    "powerlifting": "Powerlifting",
    "strength": "Strength",
    "stretching": "Stretching",
    "strongman": "Strongman"
}


EXERCISE_DIFFICULTY_CHOICES = {
    "": "None",
    "beginner": "Beginner",
    "intermediate": "Intermediate",
    "expert": "Expert"
}

class ExerciseForm(forms.Form):
    muscle_group = forms.ChoiceField(choices=EXERCISE_MUSCLE_GROUP_CHOICES, label="Muscle Group")
    exercise_type = forms.ChoiceField(choices=[(k, v) for k, v in EXERCISE_TYPE_CHOICES.items()], label="Exercise Type")
    difficulty = forms.ChoiceField(choices=[(k, v) for k, v in EXERCISE_DIFFICULTY_CHOICES.items()], label="Difficulty")

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['name', 'notes']