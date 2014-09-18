function Filter(element) {
    var value = $(element).val().toUpperCase();

    $(".panel p").find('a').each(function() {
        if ($(this).text().toUpperCase().search(value) > -1) {
            $(this).show();
            $(this).next().show();
        } else {
            $(this).hide();
            $(this).next().hide();
        }
    });
}

$(document).ready(function(){
	$('.panel').find('a').tooltip();
});