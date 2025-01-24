from rest_framework.serializers import ModelSerializer
from streaming.models import Carrusel, Comentario, Configuracion, Evento, Gallos, Streaming, Usuario, ParticipacionGalllos, RegistroEvento


class CarruselSerializer(ModelSerializer):

    class Meta:
        model = Carrusel
        fields = '__all__'


class ComentarioSerializer(ModelSerializer):

    class Meta:
        model = Comentario
        fields = '__all__'


class ConfiguracionSerializer(ModelSerializer):

    class Meta:
        model = Configuracion
        fields = '__all__'


class EventoSerializer(ModelSerializer):

    class Meta:
        model = Evento
        fields = '__all__'


class GallosSerializer(ModelSerializer):

    class Meta:
        model = Gallos
        fields = '__all__'


class StreamingSerializer(ModelSerializer):

    class Meta:
        model = Streaming
        fields = '__all__'


class UsuarioSerializer(ModelSerializer):

    class Meta:
        model = Usuario
        fields = '__all__'


class ParticipacionGalllosSerializer(ModelSerializer):

    class Meta:
        model = ParticipacionGalllos
        fields = '__all__'


class RegistroEventoSerializer(ModelSerializer):

    class Meta:
        model = RegistroEvento
        fields = '__all__'
