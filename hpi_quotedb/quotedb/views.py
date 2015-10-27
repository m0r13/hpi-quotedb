from django.shortcuts import render

# Create your views here.

def index(request):
    context = {}
    return render(request, "general/index.html.tpl", context)
