from django.contrib import admin
from core.models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'industry']

