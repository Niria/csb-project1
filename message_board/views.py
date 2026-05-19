from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world")

def thread(request, thread_id):
    return HttpResponse("Thread id: %s" % thread_id)
