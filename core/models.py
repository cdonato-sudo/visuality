from django.db import models
from django.contrib.auth.models import User

class Video(models.Model):
    titulo = models.CharField(max_length=255, blank=True)
    archivo = models.FileField(upload_to='videos/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    # puede ser null (admin puede cargar videos)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # NUEVO: marca si ya se reprodujo (para volver al video base)
    reproducido = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.titulo or (self.archivo.name if self.archivo else "(sin título)")
