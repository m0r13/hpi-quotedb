def get_username(request):
    return request.META.get("REMOTE_USER", "dummy")
