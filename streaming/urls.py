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
    
    
    path("chat/", views.chat_view, name="chat"),
    
]
router.register(r'duenio', views.DuenioViewSet, 'Duenio')
router.register(r'carrusel', views.CarruselViewSet, 'Carrusel')
router.register(r'comentario', views.ComentarioViewSet, 'Comentario')
router.register(r'configuracion', views.ConfiguracionViewSet, 'Configuracion')
router.register(r'evento', views.EventoViewSet, 'Evento')
router.register(r'gallos', views.GallosViewSet, 'Gallos')
router.register(r'streaming', views.StreamingViewSet, 'Streaming')
router.register(r'usuario', views.UsuarioViewSet, 'Usuario')
router.register(r'participaciongalllos', views.ParticipacionGalllosViewSet, 'ParticipacionGalllos')
router.register(r'registroevento', views.RegistroEventoViewSet, 'RegistroEvento')
router.register(r'estado', views.EstadoViewSet, 'Estado')

urlpatterns = urlpatterns +  router.urls


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

