from django.conf import settings

from hpi_quotedb.quotedb.util import get_username

def quotedb_settings(request):
    d = {}
    for key in dir(settings):
        if key.startswith("QUOTEDB_"):
            d[key] = getattr(settings, key)
    if settings.QUOTEDB_DEBUG_USERNAME:
        d["QUOTEDB_USER"] = get_username(request)
    return d

