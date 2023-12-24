from .views import *
from django.urls import path, include

urlpatterns = [
    path('login/', UserView.as_view()),
]

