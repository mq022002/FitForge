$(document).ready(function() { 
    // When selecting which workout to add to
    $('#workout-selector').on('change', (event) => {
        readExercisesInWorkout();
    });

    // When submitting the form to add an exercise to a workout
    $('#add-exercise-to-workout').click(function() {
        console.log("adding exercise to workout");
        // Retrieve the data-exercise-id attribute
        const selectedExercise = $(this).data('exercise');

        const workout_id = $('#workout-selector').val();
        const sets = $('#sets').val();
        const reps = $('#reps').val();
        const weight = $('#weight').val();
        const notes = $('#notes').val();

        $.ajax({
            type: 'POST',
            url: addExercisesUrl,
            data: {
                'csrfmiddlewaretoken': CSRFToken,
                'exercise_name': selectedExercise.name,
                'exercise_type': selectedExercise.type,
                'exercise_muscle': selectedExercise.muscle,
                'exercise_equipment': selectedExercise.equipment,
                'exercise_difficulty': selectedExercise.difficulty,
                'exercise_instructions': selectedExercise.instructions,
                'sets': sets,
                'reps': reps,
                'weight': weight,
                'rest_time': 5,
                'notes': notes,
                'workout_id': workout_id
            },
            success: function(data) {
                readExercisesInWorkout();
            }
        })
    });
});

function readExercisesInWorkout(){
    $.ajax({
        type: 'POST',
        url: readWorkoutUrl,
        data: {
            'csrfmiddlewaretoken': CSRFToken,
            'workout_id': $('#workout-selector').val()
        },
        success: function(data) {
            const workout = data.workout;
            $('#exercises-in-workout').empty();
            for (let exercise of workout.exercises) {
                $('#exercises-in-workout').append(
                    `<div class='border text-center lead bg-white rounded p-1 my-1 fs-6'>
                        ${exercise.name}
                    </div>`
                )
            }
        }
    });
}