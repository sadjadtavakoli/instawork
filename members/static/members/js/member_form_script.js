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

    $('input[name="phone"]').on('input', function(){
        let value = this.value.replaceAll('-','');
        const areaCode = value.substring(0,3);
        const middle = value.substring(3,6);
        const last = value.substring(6,10);
        let replacement = areaCode;
        if(areaCode.length === 3) replacement+="-";
        if(middle) replacement+=middle;
        if(middle.length === 3) replacement+="-";
        if(last) replacement+=last;
        this.value= replacement;
    });
});
