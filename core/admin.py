from django.contrib import admin

from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ``Video`` model.  Lists a few useful
    fields and allows searching by title and filename.  Ordering is
    descending by the upload timestamp to ensure that the most recently
    uploaded videos appear first in the list.
    """

    list_display = ("id", "titulo", "archivo", "fecha_subida", "usuario")
    search_fields = ("titulo", "archivo")
    ordering = ("-fecha_subida",)
