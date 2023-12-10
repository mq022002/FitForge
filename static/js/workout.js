$(document).ready(function() {
    $(".details").click(function() {
        if ($(this).attr("aria-expanded") == "true") {
            $(this).html("Less Details");
        } else {
            $(this).html("More Details");
        }
    });

    $('.delete').click(function() {
        let id = $(this).data('id');
        console.log("id", id);
        $.ajax({
            url: deleteExerciseURL,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': CSRFToken,
                id: id
            },
            success: function(response) {
                location.reload();
            }
        });
    })
});