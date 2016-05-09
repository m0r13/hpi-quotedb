from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import ModelForm, CharField, ValidationError
from django.utils.translation import ugettext as _
from .models import Tag, Quote, Vote
from .util import get_username

import random

# Create your views here.

class QuoteForm(ModelForm):
    class Meta:
        model = Quote
        fields = ["text"]

    tags = CharField(max_length=255)

    def clean_tags(self):
        tags = self.cleaned_data.get("tags", "")
        parsed_tags = set()
        for tag in tags.split(" "):
            tag = tag.strip().replace("#", "")
            if not tag:
                continue
            if not tag.isalnum():
                raise ValidationError(_("Invalid tag value (must be alphanumeric): %(value)s"), code="invalid", params={"value" : tag})
            parsed_tags.add(tag)
        return parsed_tags

    def save(self, commit=True):
        instance = super(QuoteForm, self).save(commit=commit)
        for tag in self.cleaned_data.get("tags", set()):
            instance.tags.add(Tag.objects.get_or_create(name=tag)[0])
        if commit:
            instance.save()
        return instance

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
    context = {"form" : form, "tag_cloud" : Tag.get_tag_cloud()}
    return render(request, "quote/submit.html", context)

def vote_quote(request, pk, vote):
    quote = get_object_or_404(Quote, visible=True, pk=pk)

    hash = Vote.generate_vote_hash(quote, get_username(request))
    votes = Vote.objects.all().filter(quote=quote, hash=hash)
    if votes.count() == 0:
        Vote.objects.create(quote=quote, value=vote, hash=hash)
    else:
        Vote.objects.all().filter(quote=quote, hash=hash).update(value=vote)
    quote.update_votes()
    return redirect(request.GET.get("return"))

def single_quote(request, pk):
    context = {"quote" : get_object_or_404(Quote, visible=True, pk=pk).process_voted(request), "tag_cloud" : Tag.get_tag_cloud()}
    return render(request, "quotes/quotes.html", context)

def random_quote(request):
    count = Quote.objects.all().filter(visible=True).count()
    quote = Quote.objects.filter(visible=True).all()[random.randint(0, count - 1)].process_voted(request)
    context = {"title" : "Random quote", "quote" : quote, "tag_cloud" : Tag.get_tag_cloud()}
    return render(request, "quotes/quotes.html", context)

def show_quotes(request, redirect_if_invalid, title, quote_list):
    paginator = Paginator(quote_list, settings.QUOTEDB_QUOTES_PER_PAGE)
    page = request.GET.get("page")
    quotes = None
    try:
        quotes = paginator.page(page)
    except PageNotAnInteger:
        response = redirect_if_invalid
        response["Location"] += "?page=1"
        return response
    except EmptyPage:
        response = redirect_if_invalid
        response["Location"] += "?page=%d" % paginator.num_pages
        return response
    context = {"title" : title, "quotes" : quotes, "tag_cloud" : Tag.get_tag_cloud()}
    return render(request, "quotes/quotes.html", context)

def quotes(request, order="newest"):
    title = ""
    quote_list = Quote.objects.all().filter(visible=True)
    if order == "newest":
        title = "Newest quotes"
        quote_list = quote_list.order_by("-date")
    elif order == "top":
        title = "Top quotes"
        quote_list = quote_list.order_by("-voting")
    for quote in quote_list:
        quote.process_voted(request)
    return show_quotes(request, redirect("quotedb:quotes", order=order), title, quote_list)

def quotes_by_tag(request, tag):
    tag = get_object_or_404(Tag, name=tag)
    title = "Quotes with tag #%s" % tag.name
    quotes = Quote.objects.filter(tags=tag)
    for quote in quotes:
        quote.process_voted(request)
    return show_quotes(request, redirect("quotedb:quotes_by_tag", tag=tag.name), title, quotes)
