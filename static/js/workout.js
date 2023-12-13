$(document).ready(function() {
    $(".details").click(function() {
        if ($(this).attr("aria-expanded") == "true") {
            $(this).html("Less Details");
        } else {
            $(this).html("More Details");
        }
    });
});