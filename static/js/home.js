function Filter(element) {
    var value = $(element).val().toUpperCase();

    $(".panel p").find('a').each(function() {
        if ($(this).text().toUpperCase().search(value) > -1) {
            $(this).show();
        } else {
            $(this).hide();
        }
    });
}

$(document).ready(function(){
	$('.panel').find('a').tooltip();

	$('.hover').bloxhover({
		effect: "square",
		delay: 30,
		color: 'rgb(1,1,1)',
	});
});