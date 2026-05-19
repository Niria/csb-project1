from django.urls import path
from . import views

app_name = "message_board"
urlpatterns = [
    path("", views.index, name="index"),
    path("threads/<int:thread_id>/", views.thread, name="thread"),
    path("threads/new/", views.new_thread, name="new_thread"),
    path("threads/<int:thread_id>/edit/", views.edit_thread, name="edit_thread"),
    path("threads/<int:thread_id>/reply/", views.new_reply, name="new_reply"),
    path("threads/<int:thread_id>/<int:reply_id>/edit", views.edit_reply, name="edit_reply"),
]