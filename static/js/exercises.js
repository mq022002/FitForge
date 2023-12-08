$(document).ready(function() {
    
    $('.exercise-row').click(function() {
        // Toggle the next element which is the hidden details
        $(this).next('.exercise-details').toggle();
    });
    
    $('#exercises-form').submit(function(event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: readExercisesUrl,
            data: {
                'csrfmiddlewaretoken': CSRFToken,
                muscle: $('input[name=muscle]:checked').val(),
                type: $('input[name=type]:checked').val(),
                difficulty: $('input[name=difficulty]:checked').val(),
                // Add other form data as needed
            },
            success: function(data) {
                updateExercisesTable(data.exercises);
                if ($('#exercises').hasClass('d-none')) {
                    $('#exercises').removeClass('d-none');
                }
            },
            error: function(error) {
                console.log('Error:', error);
            }
        })
    });

    // When selecting which workout to add to
    $('#workout-selector').on('change', (event) => {
        readExercisesInWorkout();
    });

    // When submitting the form to add an exercise to a workout
    $('#add-exercise-to-workout').click(function() {
        console.log("adding exercise to workout");

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

// When clicking on any add button in each row of the exercises table
$(document).on('click', '.add-exercise', function() {
    selectedExercise = $(this).data('exercise');
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

function updateExercisesTable(exercises) {
    const tableBody = $('#exercises-table tbody');
    tableBody.empty(); // Clear current table body

    $.each(exercises, function(i, exercise) {
        const row = $(`<tr data-bs-toggle="collapse" data-bs-target="#collapse${i}" aria-expanded="false" aria-controls="collapse${i}"></tr>`);
        row.append($('<td id="exercise-name"></td>').text(exercise.name));
        row.append($('<td id="exercise-muscle"></td>').text(exercise.muscle));
        row.append($('<td id="exercise-type"></td>').text(exercise.type));
        row.append($('<td></td>').text(exercise.equipment));
        row.append($('<td></td>').text(exercise.difficulty));
        const addButton = $('<button class="btn btn-primary add-exercise"">Add</button>');
        addButton.data('exercise', exercise); // Attach the entire exercise object
        // Add click event to add exercise button to not open the modal if no workout selected
        addButton.click(function(e) {
            let workout = $('#workout-selector option:selected');
            if (!workout.is(':disabled')) {
                $('#exerciseModal').modal('toggle');
                $('#workout-error').toggleClass('d-none');
            } else {
                $('#workout-error').toggleClass('d-none');
            }
        });
        console.log(isAuthenticated);
        if(isAuthenticated === 'True') {
            console.log("code running");
            row.append($('<td></td>').append(addButton));
        }
        
        // Add collapsible instructions
        tableBody.append(row);

        const collapseRow = $(`<tr class="collapse" id="collapse${i}"><td colspan="6"><b>Instructions:</b> ${exercise.instructions}</td></tr>`);
        tableBody.append(collapseRow);

    });
}