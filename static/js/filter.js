function filter(element) {
    var value = $(element).val().toUpperCase();

    $(".thumbnail-body").find('.media-body').each(function() {
        if ($(this).children().text().toUpperCase().search(value) > -1) {
            $(this).show();
        } else {
            $(this).hide();
        }
    });
}