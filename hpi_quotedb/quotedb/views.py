from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import ModelForm
from .models import Quote, Vote

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
            # TODO inform admin about new quote and review
            return redirect("quotedb:quotes", order="newest")
    else:
        form = QuoteForm()
    context = {"form" : form}
    return render(request, "quote/submit.html", context)

def vote_quote(request, pk, vote):
    quote = get_object_or_404(Quote, visible=True, pk=pk)

    hash = Vote.generate_vote_hash(quote, request.META.get("REMOTE_USER", "dummy"))
    votes = Vote.objects.all().filter(quote=quote, hash=hash)
    if votes.count() == 0:
        Vote.objects.create(quote=quote, value=vote, hash=hash)
    else:
        Vote.objects.all().filter(quote=quote, hash=hash).update(value=vote)
    quote.update_votes()
    return redirect(request.GET.get("return"))

def single_quote(request, pk):
    context = {"quote" : get_object_or_404(Quote, visible=True, pk=pk).process_voted(request)}
    return render(request, "quotes/quotes.html", context)

def random_quote(request):
    count = Quote.objects.all().filter(visible=True).count()
    context = {"quote" : Quote.objects.filter(visible=True).all()[random.randint(0, count - 1)].process_voted(request)}
    return render(request, "quotes/quotes.html", context)

def quotes(request, order="newest"):
    quote_list = Quote.objects.all().filter(visible=True)
    if order == "newest":
        quote_list = quote_list.order_by("-date")
    elif order == "top":
        quote_list = quote_list.order_by("-voting")
    for quote in quote_list:
        quote.process_voted(request)
    
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

