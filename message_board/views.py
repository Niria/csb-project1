from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from .models import Thread, Reply


def index(request):
    thread_list = Thread.objects.all()
    context = {"thread_list": thread_list}
    return render(request, "message_board/index.html", context)

def login_view(request):
    if request.method == "GET":
        return render(request, "message_board/login.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("message_board:index")
        else:
            return redirect("message_board:login_view", {"error": "Invalid username or password"})
        
def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("message_board:index")

def thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    replies = Reply.objects.all().filter(thread=thread_id)
    return render(request, "message_board/thread.html", 
                  {"thread": thread, "replies": replies})

def new_thread(request):
    thread_title = request.POST["new-thread-title"]
    thread_content = request.POST["new-thread-content"]
    thread = Thread(title=thread_title, content=thread_content)
    thread.save()
    return redirect("message_board:thread", thread_id=thread.id)

def delete_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    thread.delete()
    return redirect("message_board:index")

def new_reply(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    reply_content = request.POST["new-reply-content"]
    reply = Reply(thread=thread, content=reply_content)
    reply.save()
    return HttpResponseRedirect(reverse("message_board:thread", args=(thread_id,)))

def delete_reply(request, thread_id, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    reply.delete()
    return redirect("message_board:thread", thread_id=thread_id)
