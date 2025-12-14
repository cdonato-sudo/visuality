from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.templatetags.static import static
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import Video
from .forms import RegistroForm, VideoForm


def home(request):
    return render(request, "core/home.html")


def live_view(request):
    """
    Muestra siempre el video base (autopublicidad).
    Si hay un video de usuario pendiente (reproducido=False),
    se reproduce una sola vez y luego vuelve al base.
    """

    # Video fijo de autopublicidad
    base_video_url = static("videos/base.mp4")

    # Buscar el próximo video subido por usuarios (ignora videos viejos/admin)
    next_video = (
        Video.objects
        .filter(reproducido=False, usuario__isnull=False)
        .order_by("id")
        .first()
    )

    return render(request, "core/live.html", {
        "base_video_url": base_video_url,
        "next_video": next_video,
    })


def upload_view(request):
    # Si NO está logueado, lo mando a login con mensaje
    if not request.user.is_authenticated:
        messages.error(request, "Primero tenés que iniciar sesión para subir tu video.")
        return redirect("login")

    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)

        if form.is_valid():
            video = form.save(commit=False)
            video.usuario = request.user
            video.reproducido = False  # 👈 queda pendiente para mostrarse
            video.save()

            messages.success(
                request,
                "Video subido correctamente. Se mostrará una vez en la pantalla."
            )
            return redirect("live")
        else:
            messages.error(request, "Revisá el formulario. Hay errores.")
    else:
        form = VideoForm()

    return render(request, "core/upload.html", {"form": form})


@require_POST
@csrf_exempt
def mark_played(request, video_id):
    """
    Marca un video como reproducido para que no vuelva a mostrarse
    y la pantalla regrese al video base.
    """
    video = Video.objects.filter(
        id=video_id,
        usuario__isnull=False
    ).first()

    if video:
        video.reproducido = True
        video.save(update_fields=["reproducido"])

    return JsonResponse({"ok": True})


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
