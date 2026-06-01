"""
URL configuration for atlas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path

from core.api_views import dashboard_summary
from core.views import frontend_index
from riscos.api_views import riscos_collection

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/dashboard/", dashboard_summary, name="api_dashboard_summary"),
    path("api/riscos/", riscos_collection, name="api_riscos_collection"),
    path("", frontend_index, name="frontend_index"),
    re_path(r"^(?!admin/|api/).*$", frontend_index),
]
