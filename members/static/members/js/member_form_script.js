$(document).ready(function () {
    $('input').on('input', function () {
        $(this).siblings('.error_message').css('display', 'none');
    });

    $('#delete-confirmation').on('click', function (event) {
        let deleteUrl = $(this).attr('href');
        $.ajax(deleteUrl, {
            type: 'DELETE',
            headers: {
                'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (data, status, xhr) {   // success callback function
                window.location = '/';
            },
            error: function (jqXhr, textStatus, errorMessage) { // error callback
            }
        });
    });
});
