from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from django.db import connection

from .models import Thread, Reply
User = get_user_model()

def index(request):
    thread_list = Thread.objects.all()
    context = {"thread_list": thread_list}
    return render(request, "message_board/index.html", context)

def register_view(request):
    if request.method == "GET" and request.user.is_authenticated:
        return redirect("message_board:index")
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = request.POST["email"]
            user.save()
            return redirect("message_board:login_view")
        else:
            messages.error(request, "Registration failed")
        
    return render(request, "message_board/register.html")

def login_view(request):
    if request.method == "GET" and request.user.is_authenticated:
        return redirect("message_board:index")
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("message_board:index")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "message_board/login.html")
        
def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("message_board:index")

# Flaw 2
def profile_view(request, username):
    # Uncomment the two lines below to apply fix for flaw 2
    if request.user.username != username:
        raise PermissionDenied
    user = get_object_or_404(User, username=username)
    return render(request, "message_board/profile.html", {"user": user})

def thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    replies = Reply.objects.filter(thread=thread_id)
    return render(request, "message_board/thread.html", 
                  {"thread": thread, "replies": replies})

# Flaw 1
# Comment or delete the @csrf_exempt decorator from the row below
@csrf_exempt
def new_thread(request):
    thread_title = request.POST["new-thread-title"]
    thread_content = request.POST["new-thread-content"]
    thread = Thread(user=request.user, title=thread_title, content=thread_content)
    thread.save()
    return redirect("message_board:thread", thread_id=thread.id)

def delete_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    thread.delete()
    return redirect("message_board:index")

def new_reply(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    reply_content = request.POST["new-reply-content"]
    reply = Reply(user=request.user, thread=thread, content=reply_content)
    reply.save()
    return HttpResponseRedirect(reverse("message_board:thread", args=(thread_id,)))

# FLAW 3
# Flawed endpoint:
def delete_reply(request, thread_id):
    reply_id = request.POST["reply-id"]
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM message_board_reply WHERE id =" + reply_id)
    return redirect("message_board:thread", thread_id=thread_id)

# Fixed endpoint:
# def delete_reply(request, thread_id):
#     reply = get_object_or_404(Reply, pk=reply_id)
#     reply.delete()
#     return redirect("message_board:thread", thread_id=thread_id)
