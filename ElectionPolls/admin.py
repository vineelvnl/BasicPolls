from django.contrib import admin

# Register your models here.
from .models import Question, choice

class choiceInline(admin.TabularInline):
    model = choice
    extra = 3
class Questionadmin(admin.ModelAdmin):
    list_filter = ["published_date"]
    search_fields = ["question_text"]
    fieldsets = [
        (None, {'fields':['question_text']}),
        ('Date information',{'fields':['published_date']}),
    ]
    inlines = [choiceInline]
    list_display = ("question_text", "published_date", "was_published_recently")
admin.site.register(Question, Questionadmin)
