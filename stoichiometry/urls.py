from django.urls import path

from .views import CompoundInformationAPI


urlpatterns = [
    path("compound-information", CompoundInformationAPI.as_view()),
]
