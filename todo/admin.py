from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'user', 'created_at']
    list_filter = ['status', 'user']
    search_fields = ['title', 'user__username']
# Register your models here.
