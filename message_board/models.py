from django.db import models


class Thread(models.Model):
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=4096)
    upvotes = models.IntegerField(default=0)

    def __str__(self):
        return f"Title: {self.title}\nUpvotes:{self.upvotes}\nContent: {self.content}"

class Reply(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    content = models.CharField(max_length=4096)
    upvotes = models.IntegerField(default=0)

    def __str__(self):
        return f"Thread: {self.thread.title}\nUpvotes:{self.upvotes}\nContent: {self.content}"
