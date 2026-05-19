from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:thread_id>/", views.thread, name="thread")
]