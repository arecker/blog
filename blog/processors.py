from django.conf import settings


def analytics(request):
    """
    Inject google analytics tracking code into context
    """
    ga_prop_id = getattr(settings, 'GOOGLE_ANALYTICS_PROPERTY_ID', False)
    ga_domain = getattr(settings, 'GOOGLE_ANALYTICS_DOMAIN', False)
    if not settings.DEBUG and ga_prop_id and ga_domain:
        return {
            'GOOGLE_ANALYTICS_PROPERTY_ID': ga_prop_id,
            'GOOGLE_ANALYTICS_DOMAIN': ga_domain,
        }
    return {}


def domain(request):
    """
    Inject site domain into context
    """
    domain = getattr(settings, 'SITE_DOMAIN', 'localhost:8000')
    return {
        'SITE_DOMAIN': domain
    }
