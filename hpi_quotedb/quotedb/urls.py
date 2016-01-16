from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.quotes, {"order" : "newest"}, name="index"),

    url(r'^quote/submit$', views.submit_quote, name="submit_quote"),
    #url(r'^quote/report/(?P<pk>[0-9]+)$', views.report_quote),
    url(r'^quote/vote/(?P<pk>[0-9]+)/(?P<vote>-1|0|1)$', views.vote_quote, name="vote_quote"),

    url(r'^quotes/(?P<pk>[0-9]+)$', views.single_quote, name="single_quote"),
    url(r'^quotes/random$', views.random_quote, name="random_quote"),
    url(r'^quotes$', views.quotes),
    url(r'^quotes/(?P<order>newest|top)$', views.quotes, name="quotes"),
    url(r'^quotes/tag/(?P<tag>.*)$', views.quotes_by_tag, name="quotes_by_tag"),
]

