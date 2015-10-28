from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.quotes, {"order" : "newest"}),

    url(r'^quotes/(?P<pk>[0-9]+)$', views.quotes_single),
    url(r'^quotes/random$', views.quotes_random),
    url(r'^quotes$', views.quotes, {"order" : "newest"}),
    url(r'^quotes/(?P<order>newest|top)$', views.quotes),
]

