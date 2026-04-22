from django.contrib import admin
from .models import Risco
# Register your models here.

@admin.register(Risco)
class RiscoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'departamento', 'nivel_de_risco', 'nivel_residual')
    search_fields = ('nome', 'descricao', 'departamento')
    list_filter = ('tipo', 'departamento', 'nivel_de_risco')