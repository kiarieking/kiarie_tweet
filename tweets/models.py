from django.db import models
import random
from django.conf import settings

User = settings.AUTH_USER_MODEL

class TweetLike(models.Model):
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timeStamp = models.DateTimeField(auto_now_add=True)

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    likes = models.ManyToManyField(User, related_name="tweet_user",blank=True, through=TweetLike)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    timeStamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    def serialize(self):
        return{
            "id":self.id,
            "content":self.content,
            "likes":random.randint(0,300)
        }

    def __str__(self):
        return(self.content)