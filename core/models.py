from django.db import models
from django.contrib.auth.models import User

class Video(models.Model):
    """
    Represents a video uploaded to the platform.  Each video has a title,
    a file stored under ``media/videos/``, the timestamp when it was
    uploaded, and optionally the user who uploaded it.  Making the
    ``usuario`` field optional allows videos to be uploaded without
    associating them to a specific user account (for example, when the
    site operator loads initial content via the admin interface).  If
    you want to force attribution, remove ``null=True, blank=True`` and
    update ``upload_view`` in ``views.py`` accordingly.
    """

    titulo = models.CharField(max_length=255, blank=True)
    archivo = models.FileField(upload_to='videos/')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    # ``usuario`` no longer required; allows NULL and blank values.
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        # Fallback to the filename if no title is provided
        return self.titulo or (self.archivo.name if self.archivo else "(sin título)")