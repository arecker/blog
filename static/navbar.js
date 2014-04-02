function Activate(id)
{
	$('.nav-pills').find('ul').removeClass('active');
	$( id ).addClass('active');
}

var title = $(document).find("title").text().replace(' | ', '').replace('Blog by Alex Recker', '');
switch(title)
{
	case "":
		Activate("#home-button");
		break;
	case "Archives":
		Activate("#archives-button");
		break;
	case "Projects":
		Activate("#projects-button");
		break;
	case "Friends":
		Activate("#friends-button");
		break;
}