from django.conf import settings

from .util import get_username
from .models import Tag

def quotedb_settings(request):
    d = {}
    for key in dir(settings):
        if key.startswith("QUOTEDB_"):
            d[key] = getattr(settings, key)
    if settings.QUOTEDB_DEBUG_USERNAME:
        d["QUOTEDB_USER"] = get_username(request)
    return d

def quotedb_tagcloud(request):
    return dict(tagcloud=Tag.get_tag_cloud())

