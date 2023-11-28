$('.exercise-row').click(function() {
    // Toggle the next element which is the hidden details
    $(this).next('.exercise-details').toggle();
});
$('#filters').submit(function(event) {
    //$('.exercise-details').hide();
});