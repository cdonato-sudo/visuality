from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Video


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['titulo', 'archivo']

def clean_archivo(self):
    archivo = self.cleaned_data['archivo']

    import tempfile
    import os
    from moviepy.editor import VideoFileClip  

    temp = tempfile.NamedTemporaryFile(delete=False)
    for chunk in archivo.chunks():
        temp.write(chunk)
    temp.close()

    clip = VideoFileClip(temp.name)
    duracion = clip.duration
    clip.close()

    os.unlink(temp.name)

    if duracion > 15:
        raise forms.ValidationError("El video no puede durar más de 15 segundos.")

    return archivo
