from django.contrib import admin
from .models import MainContent


@admin.register(MainContent)
class MainContentAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'value')
    search_fields = ('name', 'key', 'value')
