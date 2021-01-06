from django.contrib import admin
from .models import Tweet, TweetLike

class TweetLikeAdmin(admin.TabularInline):
    model = TweetLike

class TweetAdmin(admin.ModelAdmin):
    inlines = [TweetLikeAdmin]
    list_display = ['__str__', 'user']
    search_fields = ['user__username','content']
    class Meta:
        model = Tweet

# Register your models here.
admin.site.register(Tweet, TweetAdmin)
# admin.site.register(TweetLike)