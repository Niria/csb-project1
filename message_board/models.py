from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class Thread(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=4096)
    upvotes = models.IntegerField(default=0)

    def __str__(self):
        return f"Title: {self.title}\nUpvotes:{self.upvotes}\nContent: {self.content}"

class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    content = models.CharField(max_length=4096)
    upvotes = models.IntegerField(default=0)

    def __str__(self):
        return f"Thread: {self.thread.title}\nUpvotes:{self.upvotes}\nContent: {self.content}"
