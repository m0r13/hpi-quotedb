from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import ModelForm
from .models import Quote

import random

# Create your views here.

class QuoteForm(ModelForm):
    class Meta:
        model = Quote
        fields = ["text"]

def submit_quote(request):
    form = None
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Thanks for submitting a quote!")
            return redirect("quotedb:quotes", order="newest")
    else:
        form = QuoteForm()
    context = {"form" : form}
    return render(request, "quote/submit.html", context)

def single_quote(request, pk):
    context = {"quote" : Quote.objects.get(pk=pk)}
    return render(request, "quotes/quotes.html", context)

def random_quote(request):
    count = Quote.objects.all().count()
    context = {"quote" : Quote.objects.all()[random.randint(0, count - 1)]}
    return render(request, "quotes/quotes.html", context)

def quotes(request, order="newest"):
    quote_list = Quote.objects.all()
    if order == "newest":
        quote_list = quote_list.order_by("-date")
    
    paginator = Paginator(quote_list, 5)
    page = request.GET.get("page")
    quotes = None
    try:
        quotes = paginator.page(page)
    except PageNotAnInteger:
        response = redirect("quotedb:quotes", order=order)
        response["Location"] += "?page=1"
        return response
    except EmptyPage:
        response = redirect("quotedb:quotes", order=order)
        response["Location"] += "?page=%d" % paginator.num_pages
        return response
    context = {"quotes" : quotes}
    return render(request, "quotes/quotes.html", context)

def index(request):
    context = {"quotes" : Quote.objects.all()}
    return render(request, "general/index.html", context)
