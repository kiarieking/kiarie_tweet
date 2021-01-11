from django.test import TestCase
from .models import Tweet
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
# Create your tests here.

User = get_user_model()
class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='king', password="password")
        tweet = Tweet.objects.create(content="Test tweet", user=self.user )
        tweet2 = Tweet.objects.create(content="Tweet 2 test", user = self.user)

    
    def get_client(self):
        client = APIClient()
        client.login(username = self.user.username, password = 'password')
        return client

    def test_api_tweetList(self):
        client = self.get_client()
        response = client.get('/tweets')
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.json()),2)
        print (len(response.json()))