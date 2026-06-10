from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import UserCreationFormWithEmail
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from django.db import connection

from .models import Thread, Reply
User = get_user_model()

def index(request):
    thread_list = Thread.objects.all()
    return render(request, "message_board/index.html", {"thread_list": thread_list})

def register_view(request):
    if request.method == "GET" and request.user.is_authenticated:
        return redirect("message_board:index")
    
    if request.method == "POST":
        form = UserCreationFormWithEmail(request.POST)
        if form.is_valid():
            user = form.save()
            # user.email = request.POST.get("email")
            # user.save()
            return redirect("message_board:login_view")

    else:
        form = UserCreationFormWithEmail()

    return render(request, "message_board/register.html", {"form": form})

def login_view(request):
    if request.method == "GET" and request.user.is_authenticated:
        return redirect("message_board:index")
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
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
@login_required(redirect_field_name=None)
def profile_view(request, username):
    # Uncomment the two lines below to apply the fix for flaw 2
    # if request.user.username != username:
    #     raise PermissionDenied
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
@login_required(redirect_field_name=None)
def new_thread(request):
    thread_title = request.POST.get("new-thread-title")
    thread_content = request.POST.get("new-thread-content")
    thread = Thread(user=request.user, title=thread_title, content=thread_content)
    thread.save()
    return redirect("message_board:thread", thread_id=thread.id)

@login_required(redirect_field_name=None)
def delete_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id, user=request.user)
    thread.delete()
    return redirect("message_board:index")

@login_required(redirect_field_name=None)
def new_reply(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    reply_content = request.POST.get("new-reply-content")
    reply = Reply(user=request.user, thread=thread, content=reply_content)
    reply.save()
    return HttpResponseRedirect(reverse("message_board:thread", args=(thread_id,)))

@login_required(redirect_field_name=None)
def delete_reply(request, thread_id):
    reply_id = request.POST.get("reply-id")
    reply = get_object_or_404(Reply, pk=reply_id, user=request.user)
    reply.delete()
    return redirect("message_board:thread", thread_id=thread_id)

# Flaw 3
def search(request):
    search_term = request.POST.get("search-term")
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, title FROM message_board_thread WHERE title LIKE '%" + search_term + "%'")
        threads = cursor.fetchall()
    return render(request, "message_board/search.html", {"threads": threads})

# Flaw 3 fix version 1 (parametrized query)
# def search(request):
#     search_term = f"%{request.POST.get("search-term")}%"
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT id, title FROM message_board_thread WHERE title LIKE %s", [search_term])
#         threads = cursor.fetchall()
#     return render(request, "message_board/search.html", {"threads": threads})

# Flaw 3 fix version 2 (ORM)
# def search(request):
#     search_term = request.POST.get("search-term")
#     threads = Thread.objects.filter(title__contains=search_term)
#     return render(request, "message_board/search.html", {"threads": [(t.id, t.title) for t in threads]})

# Flaw 1 test endpoint
def csrf_exploit(request):
    return render(request, "message_board/csrf_exploit.html")
