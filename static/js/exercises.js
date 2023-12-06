$('.exercise-row').click(function() {
    // Toggle the next element which is the hidden details
    $(this).next('.exercise-details').toggle();
});
$('#filters').submit(function(event) {
    //$('.exercise-details').hide();
});

$.ajax({
    url: "/exercises",
    type: "POST",
    data: {
        'workout_form': true,
        'workout_id': 5,
        'csrfmiddlewaretoken': window.CSRF_TOKEN
    },
    success: function(data) {
        console.log(data);
    }
})

$('#workout-selector').on('change', (event) => {
    $.ajax({
        url: "/exercises",
        type: "POST",
        data: {
            'workout_form': true,
            'workout_id': event.target.value,
            'csrfmiddlewaretoken': window.CSRF_TOKEN
        },
        success: function(data) {
            $('#exercises').empty()
            for (let exercise of data.exercises) {
                $('#exercises').append(
                    `<div class='border text-center lead bg-white rounded p-1 my-1'>
                        ${exercise.name}
                    </div>`
                )
            }
        }
    })
})