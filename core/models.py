from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Video(models.Model):
    titulo = models.CharField(max_length=255, blank=True)

    
    archivo = CloudinaryField(resource_type="video")

    fecha_subida = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    reproducido = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo or "(sin título)"
