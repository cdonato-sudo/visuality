from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Video

import os
import tempfile
import subprocess


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["titulo", "archivo"]

    def clean_archivo(self):
        archivo = self.cleaned_data.get("archivo")
        if not archivo:
            return archivo

        # 1) Validación simple por extensión (rápida)
        nombre = (archivo.name or "").lower()
        if not (nombre.endswith(".mp4") or nombre.endswith(".mov") or nombre.endswith(".webm")):
            raise forms.ValidationError("No es posible subir este video. Formato no soportado (usá MP4).")

        # 2) Validación por tamaño (fallback y también útil siempre)
        # Ajustá el límite a lo que quieras (ej: 30MB)
        max_mb = 30
        if archivo.size and archivo.size > max_mb * 1024 * 1024:
            raise forms.ValidationError(f"No es posible subir este video. El archivo supera {max_mb} MB.")

        # 3) Validación por duración con ffprobe (lo mejor para server)
        # Si ffprobe no está, no rompe: se queda con validación por tamaño.
        try:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(nombre)[1] or ".mp4")
            for chunk in archivo.chunks():
                tmp.write(chunk)
            tmp.close()

            # ffprobe: devuelve duración en segundos
            cmd = [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                tmp.name,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            dur_str = (result.stdout or "").strip()

            # Si ffprobe no pudo leerlo, lo tratamos como inválido
            if result.returncode != 0 or not dur_str:
                raise forms.ValidationError("No es posible subir este video. El archivo parece dañado o no es un video válido.")

            duracion = float(dur_str)

            if duracion > 15.0:
                raise forms.ValidationError("No es posible subir este video. Debe durar como máximo 15 segundos.")

        except FileNotFoundError:
            # ffprobe no está instalado (no rompemos el form)
            # Te queda la validación por tamaño + extensión.
            pass
        except subprocess.TimeoutExpired:
            raise forms.ValidationError("No es posible subir este video. No pudimos verificar su duración (probá con otro archivo).")
        finally:
            try:
                os.unlink(tmp.name)
            except Exception:
                pass

        return archivo
