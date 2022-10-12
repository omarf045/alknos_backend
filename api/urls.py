from django.urls import path

from rest_framework.authtoken import views
from .views import UserDetailAPI, RegisterUserAPIView, InorganicReactionAPI

urlpatterns = [
    # reactions
    path("inorganic-reaction", InorganicReactionAPI.as_view()),

    path("get-details", UserDetailAPI.as_view()),
    path('register', RegisterUserAPIView.as_view()),
    path('login', views.obtain_auth_token)
]
