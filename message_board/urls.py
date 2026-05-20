from django.urls import path, include
from . import views

app_name = "message_board"
urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("login", views.login_view, name="login_view"),
    path("logout", views.logout_view, name="logout_view"),
    path("threads/<int:thread_id>/", views.thread, name="thread"),
    path("threads/new/", views.new_thread, name="new_thread"),
    path("threads/<int:thread_id>/delete/", views.delete_thread, name="delete_thread"),
    path("threads/<int:thread_id>/reply/", views.new_reply, name="new_reply"),
    path("threads/<int:thread_id>/<int:reply_id>/delete", views.delete_reply, name="delete_reply"),
]