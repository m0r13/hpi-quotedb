from django.shortcuts import render
from .models import Quote

import random

# Create your views here.

def quotes_single(request, pk):
    context = {"quote" : Quote.objects.get(pk=pk)}
    return render(request, "quotes/quotes.html", context)

def quotes_random(request):
    count = Quote.objects.all().count()
    context = {"quote" : Quote.objects.all()[random.randint(0, count - 1)]}
    return render(request, "quotes/quotes.html", context)

def quotes(request, order, page=1):
    quotes = Quote.objects.all()
    if order == "newest":
        quotes = quotes.order_by("-date")
    context = {"quotes" : quotes}
    return render(request, "quotes/quotes.html", context)

def index(request):
    context = {"quotes" : Quote.objects.all()}
    return render(request, "general/index.html", context)
