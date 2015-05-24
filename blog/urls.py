from django.conf.urls import include, url
from django.contrib import admin
from home.views import HomeIndexView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomeIndexView.as_view()),
    url(r'^', include('blogging.urls')),
]