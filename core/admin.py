from django.contrib import admin
from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "usuario", "reproducido", "fecha_subida")
    list_filter = ("reproducido", "fecha_subida")
    search_fields = ("titulo", "usuario__username")
    ordering = ("-id",)
