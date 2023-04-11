from django.urls import path

from rest_framework.authtoken import views
from .views import CompoundQueryAPI


urlpatterns = [
    # reactions
    path("compound-query", CompoundQueryAPI.as_view()),
]
