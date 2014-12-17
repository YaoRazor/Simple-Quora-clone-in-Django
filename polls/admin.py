from django.contrib import admin

from polls.models import Question, Answers, Tags
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from photologue.models import PhotoEffect, PhotoSize

# Register your models here.


class ChoiceInline(admin.TabularInline):
    model = Answers
    extra = 3


class QuestionAdmin(admin.ModelAdmin):

    # specify how to group the properties of each question and how to display them
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]

    # specify inline displayed items
    inlines = [ChoiceInline]

    # specify which fields will be displayed on admin page
    list_display = ('question_text', 'pub_date', 'was_published_recently', 'author')

    # specify the field that is used to filter Question
    list_filter = ['pub_date']

    # specify which fields will be used for search
    search_fields = ['question_text']



# specify which model will be displayed on the admin page
#admin.site.register(Question, QuestionAdmin)

#admin.site.register(Tags)

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(Site)
# admin.site.unregister(PhotoSize)
# admin.site.unregister(PhotoEffect)
