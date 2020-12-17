from django import forms
from .models import Tweet


MAX_TWEET_LENGTH = 240
class Tweetform(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']

    def clean_tweet(self):
        content = self.cleaned_data.get('content') 
        if len(content) > MAX_TWEET_LENGTH:
            raise forms.ValidationError('This tweet is too long') 
        return content