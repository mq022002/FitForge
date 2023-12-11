let parameters = JSON.parse(document.getElementById('parameters').textContent);
let exercise_list = JSON.parse(document.getElementById('exercises').textContent);

$(document).ready(function () {
    updatePagination(parameters.page)
});

function updatePagination(page) {
    let pages = $('.page-item');
    if (page == 1) {
        $('#previous').addClass('disabled');
        $.each(pages, function (index, value) {
            if (index == 0) {
                $(value).find('a').click(function() {
                    postPagination(page - 1)
                });
            } else if (index < $(pages).length - 1) {
                if (index == 1) {
                    $(value).addClass('active');
                    $(value).find('a').text(index)
                    $(value).find('a').click(function() {
                        postPagination(index)
                    });
                } else if (index > 1) {
                    console.log("above 1", index, value);
                    $(value).find('a').text(index)
                    $(value).find('a').click(function() {
                        postPagination(index)
                    });
                    $(value).removeClass('active');
                }
            } else {
                $(value).find('a').click(function() {
                    postPagination(page + 1)
                });
            }
        });
    } else {
        $('#previous').removeClass('disabled');
        $.each(pages, function (index, value) {
            if (index == 0) {
                $(value).find('a').click(function() {
                    postPagination(page - 1)
                });
            } else if (index < $(pages).length - 1) {
                if (index > 0) {  
                    console.log("math", page - 1 + index)
                    $(value).find('a').text(index + page - 2)
                    $(value).find('a').click(function() {
                        postPagination(index + page - 2);
                    });
                    if (index == 2) {
                        console.log("active index", index, page)
                        $(value).addClass('active');
                    } else  {
                        $(value).removeClass('active');
                    }
                }
            } else {
                $(value).removeClass('active');
                $(value).find('a').click(function() {
                    postPagination(page + 1)
                });
            }
        });
        $('#previous').removeClass('disabled');
    }
}


function postPagination(page) {
    console.log("postPagination", page)
    console.log("parameters", parameters)
    let data = {
        'pagination': true,
        'page': page,
        'search': parameters.search,
        'muscle': parameters.muscle,
        'type': parameters.type,
        'difficulty': parameters.difficulty,
        'csrfmiddlewaretoken': Cookies.get('csrftoken')
    };
    $.post('/exercises/', data, function (data) {
        let exercises = $('.container-fluid');
        console.log("data", data);
        exercises.html($(data).find('.container-fluid')[0]);
        parameters.page = page;
        $('#id_exercise_muscle_group').val(parameters.muscle);
        updatePagination(page); 
    });
}