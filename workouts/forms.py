from django import forms
from .models import Workout, ExerciseInWorkout

EXERCISE_MUSCLE_GROUP_CHOICES = [
    ('', 'Select Muscle'),  # Empty option
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
    
    # "cardio": "Cardio",
    # "olympic_weightlifting": "Olympic Weightlifting",
    # "plyometrics": "Plyometrics",
    '': 'Select Type',
    "powerlifting": "Powerlifting",
    "strength": "Strength",
    "stretching": "Stretching",
    "strongman": "Strongman"
}


EXERCISE_DIFFICULTY_CHOICES = {
    '': 'Select Difficulty',
    "beginner": "Beginner",
    "intermediate": "Intermediate",
    "expert": "Expert"
}

class ExerciseFilterForm(forms.Form):
    exercise_name = forms.CharField(required=False, label="Exercise Name", widget=forms.TextInput(attrs={'placeholder': 'Search by name'}))
    exercise_muscle_group = forms.ChoiceField(choices=EXERCISE_MUSCLE_GROUP_CHOICES, required=False, label="Muscle Group")
    exercise_type = forms.ChoiceField(choices=[(k, v) for k, v in EXERCISE_TYPE_CHOICES.items()], required=False, label="Exercise Type")
    exercise_difficulty = forms.ChoiceField(choices=[(k, v) for k, v in EXERCISE_DIFFICULTY_CHOICES.items()], required=False, label="Difficulty")

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['name', 'notes']

class ExerciseInWorkoutForm(forms.ModelForm):
    class Meta:
        model = ExerciseInWorkout
        fields = '__all__'
        exclude = ('name',)

    def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super(ExerciseInWorkoutForm, self).__init__(*args, **kwargs)
            if user is not None:
                self.fields['workout'].queryset = Workout.objects.filter(user__user=user)