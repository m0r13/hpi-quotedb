from django.contrib import admin
from .models import Tag, Quote

# Register your models here.

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", )

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("date", "text", "show_tags", "visible")

    def show_tags(self, quote):
        return " ".join([ str(tag) for tag in quote.tags.all()])
    show_tags.short_description = "tags"

