from rest_framework.routers import SimpleRouter
from streaming import views

from django.conf import settings
from django.conf.urls.static import static

from django.urls import path,include, re_path
from knox import views as knox_views


router = SimpleRouter()
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='knox_login'),
    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    
    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('channel/', views.CreateMediaLiveChannel.as_view(), name='create-medialive-channel'),
    path("chat/", views.chat_view, name="chat"),
    path("streamcomentarios/", views.chat_view_comment, name="chats"),
    path("crear-stream/", views.generar_stream, name="crear-stream"),
    path("listar-stream/", views.listar_stream, name="listar-stream"),
    path("iniciar-stream/", views.iniciar_canal_view, name="iniciar-stream"),
    path("detener-stream/", views.detener_canal_view, name="detener-stream"),
    
]
router.register(r'duenio', views.DuenioViewSet, 'Duenio')
router.register(r'carrusel', views.CarruselViewSet, 'Carrusel')
router.register(r'comentario', views.ComentarioViewSet, 'Comentario')
router.register(r'configuracion', views.ConfiguracionViewSet, 'Configuracion')
router.register(r'evento', views.EventoViewSet, 'Evento')
router.register(r'gallos', views.GallosViewSet, 'Gallos')
router.register(r'streaming', views.StreamingViewSet, 'Streaming')
router.register(r'usuario', views.UsuarioViewSet, 'Usuario')
router.register(r'participaciongallos', views.ParticipacionGallosViewSet, 'ParticipacionGallos')
router.register(r'registrofiesta', views.RegistroFiestaViewSet, 'RegistroFiesta')
router.register(r'estado', views.EstadoViewSet, 'Estado')
router.register(r'galpon', views.GalponViewSet, 'Galpon')
router.register(r'fiesta', views.FiestaViewSet, 'Fiesta')
router.register(r'galponfiesta', views.GalponFiestaViewSet, 'GalponFiesta')
router.register(r'galpongallos', views.GalponGallosViewSet, 'GalponGallos')

urlpatterns = urlpatterns +  router.urls


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

