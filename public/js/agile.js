$(function(){
    /* Use jQuery UI buttons */
    $('input[type=submit], .button').button();
    
    /* Use selectmenu jQuery UI plugin */
    $('select:not([multiple])').each(function(){
        var $this = $(this);
        $this.selectmenu({
            style: 'popup',
            menuWidth: $this.width()
        });
    });
    
    /* Add jQuery UI tabs */
    $('#tabs').tabs({
        select: function(event, ui){
            var href = $(ui.tab).attr('href');
            window.location.hash = href;
        }
    });
    
    /* Add X-CSRFToken to the request headers */
    $('html').ajaxSend(function(event, xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });
});

function move_story(number, phase, index, successCallback){
    if(typeof index == 'undefined')
        index = '';
    else if(typeof index == 'function'){
        successCallback = index;
        index = '';
    }
    successCallback = successCallback || null;
    $.ajax({
        url: '/project/' + PROJECT_ID + '/story/' + number + '/move',
        type: 'post',
        data: {
            phase: phase,
            index: index
        },
        dataType: 'json',
        success: successCallback
    });    
}
