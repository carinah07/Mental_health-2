# chatbot/urls.py
from django.urls import path
from .views import akili_chat

urlpatterns = [
    path("ask_akili/", akili_chat, name="akili_chat")
]
