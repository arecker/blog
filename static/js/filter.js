function filter(element) {
    var value = $(element).val().toUpperCase();

    $("#archives-list > li").each(function() {
        if ($(this).children().text().toUpperCase().search(value) > -1) {
            $(this).show();
        } else {
            $(this).hide();
        }
    });
}