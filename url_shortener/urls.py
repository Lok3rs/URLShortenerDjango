from url_shortener import views
from django.conf.urls import url

urlpatterns = [
    url(r'^shorten$', views.shorten_url, name='shorten_url'),
    url(r'^unshort$', views.unshort_url, name='shorten_url'),
    url(r'^(?P<slug>\w{6})$', views.redirect_from_shortened_url, name='redirect_from_shortened_url'),
]
