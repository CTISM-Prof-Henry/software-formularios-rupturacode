from django.urls import path

from .views import criar_risco

urlpatterns = [
    path('risco/criar/', criar_risco, name='criar_risco'),
]