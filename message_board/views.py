from django.http import HttpResponse, Http404
from django.shortcuts import render
from .models import Thread, Reply


def index(request):
    thread_list = Thread.objects.all()
    context = {"thread_list": thread_list}
    return render(request, "message_board/index.html", context)

def thread(request, thread_id):
    try:
        thread = Thread.objects.get(pk=thread_id)
    except:
        raise Http404("Thread does not exist")
    replies = Reply.objects.get(thread=thread_id)
    return render(request, "message_board/thread.html", 
                  {"thread": thread, "replies": replies})

def new_thread(request):
    pass

def edit_thread(request, thread_id):
    pass

def new_reply(request, thread_id):
    pass

def edit_reply(request, thread_id, reply_id):
    pass
