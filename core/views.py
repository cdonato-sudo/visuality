from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Video
from .forms import RegistroForm, VideoForm


def home(request):
    return render(request, "core/home.html")


def live_view(request):
    videos = Video.objects.order_by("-id")
    current = videos.first()
    return render(request, "core/live.html", {"current": current, "videos": videos})


def upload_view(request):
    # Si NO está logueado, lo mando a login con mensaje de error
    if not request.user.is_authenticated:
        messages.error(request, "Primero tenés que iniciar sesión para subir tu video.")
        return redirect("login")

    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)

        if form.is_valid():
            video = form.save(commit=False)
            video.usuario = request.user
            video.save()
            messages.success(request, "Video subido correctamente.")
            return redirect("live")
        else:
            messages.error(request, "Revisá el formulario. Hay errores.")
    else:
        form = VideoForm()

    return render(request, "core/upload.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "core/login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegistroForm()
    return render(request, "core/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")
