$('.hover').hover(function()
{
	var page = $( this ).find('a').attr('href').replace('/', '').replace('/', '');
	ChangeSitePageTitle(page);
});

$('.hover').mouseleave(function()
{
	$('#site-page-title').text('');
});

function ChangeSitePageTitle(title)
{
	$('#site-page-title').text(title);
}