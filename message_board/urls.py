from django.urls import path, include
from . import views

app_name = "message_board"
urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("register", views.register_view, name="register_view"),
    path("login", views.login_view, name="login_view"),
    path("logout", views.logout_view, name="logout_view"),
    path("profile/<str:username>", views.profile_view, name="profile_view"),
    path("threads/<int:thread_id>/", views.thread, name="thread"),
    path("threads/new_thread/", views.new_thread, name="new_thread"),
    path("threads/<int:thread_id>/delete_thread/", views.delete_thread, name="delete_thread"),
    path("threads/<int:thread_id>/new_reply/", views.new_reply, name="new_reply"),
    path("threads/<int:thread_id>/delete_reply", views.delete_reply, name="delete_reply"),
    path("search", views.search, name="search"),
    path("csrf_exploit", views.csrf_exploit, name="csrf_exploit"),
]