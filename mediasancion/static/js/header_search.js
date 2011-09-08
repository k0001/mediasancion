$(document).ready(function() {
    $('#search-q').focus(function() {
        $(this).addClass('highlight').prev('label').hide();
    }).blur(function() {
            $(this).removeClass('highlight');
            if ($(this).val().trim() == "")
            $(this).val("").prev('label').show();
    });
});
