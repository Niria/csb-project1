from django.db import models


class Thread(models.Model):
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=4096)
    upvotes = models.IntegerField(default=0)

class Reply(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    content = models.CharField(max_length=4096)
    upvotes = models.IntegerField(default=0)
