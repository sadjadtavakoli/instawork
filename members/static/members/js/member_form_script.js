$(document).ready(function () {
    $('input').on('input', function () {
        console.log($(this).siblings('.error_message'))
        $(this).siblings('.error_message').css('display', 'none')
    })
})
