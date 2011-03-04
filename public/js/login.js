/*
    Show and hide script
*/
$(document).ready(function(){
    if($('.error').length){
        $('.error').show('slow');
        setTimeout(function(){
            $('.error').hide('fast');
        }, 1000*5);
    }
});