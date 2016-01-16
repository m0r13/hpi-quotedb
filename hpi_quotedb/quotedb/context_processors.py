from django.conf import settings

def quotedb_settings(request):
    d = {}
    for key in dir(settings):
        if key.startswith("QUOTEDB_"):
            d[key] = getattr(settings, key)
    return d

