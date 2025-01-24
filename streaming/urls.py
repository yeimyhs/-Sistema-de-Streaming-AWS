from rest_framework.routers import SimpleRouter
from streaming import views


router = SimpleRouter()

router.register(r'carrusel', views.CarruselViewSet, 'Carrusel')
router.register(r'comentario', views.ComentarioViewSet, 'Comentario')
router.register(r'configuracion', views.ConfiguracionViewSet, 'Configuracion')
router.register(r'evento', views.EventoViewSet, 'Evento')
router.register(r'gallos', views.GallosViewSet, 'Gallos')
router.register(r'streaming', views.StreamingViewSet, 'Streaming')
router.register(r'usuario', views.UsuarioViewSet, 'Usuario')
router.register(r'participaciongalllos', views.ParticipacionGalllosViewSet, 'ParticipacionGalllos')
router.register(r'registroevento', views.RegistroEventoViewSet, 'RegistroEvento')

urlpatterns = router.urls
