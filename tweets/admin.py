from django.contrib import admin
from .models import Tweet

class TweetAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user']
    search_fields = ['user__username','content']
    class Meta:
        model = Tweet

# Register your models here.
admin.site.register(Tweet, TweetAdmin)