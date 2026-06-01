from django.urls import path
from .views import frontend_index

urlpatterns = [
    path("", frontend_index, name="frontend_index"),
]
