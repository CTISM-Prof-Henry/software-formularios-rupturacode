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
