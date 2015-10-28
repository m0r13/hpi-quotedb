from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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

def quotes(request, order):
    quote_list = Quote.objects.all()
    if order == "newest":
        quote_list = quote_list.order_by("-date")
    
    paginator = Paginator(quote_list, 5)
    page = request.GET.get("page")
    quotes = None
    try:
        quotes = paginator.page(page)
    except PageNotAnInteger:
        response = redirect("quotedb.views.quotes", order=order)
        response["Location"] = "?page=1"
        return response
    except EmptyPage:
        response = redirect("quotedb.views.quotes", order=order)
        response["Location"] = "?page=%d" % paginator.num_pages
        return response
    context = {"quotes" : quotes}
    return render(request, "quotes/quotes.html", context)

def index(request):
    context = {"quotes" : Quote.objects.all()}
    return render(request, "general/index.html", context)
