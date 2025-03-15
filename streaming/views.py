from rest_framework.viewsets import ModelViewSet
from streaming.serializers import CarruselSerializer, ComentarioSerializer, ConfiguracionSerializer, EventoSerializer, GallosSerializer, StreamingSerializer, UsuarioSerializer, ParticipacionGalllosSerializer, RegistroEventoSerializer
from streaming.models import Carrusel, Comentario, Configuracion, Evento, Gallos, Streaming, ParticipacionGalllos, RegistroEvento
from streaming.serializers import *
from streaming.models import *


from .models import CustomUser

from rest_framework import generics
from rest_framework.response import Response
from knox.models import AuthToken

from knox.views import LoginView as KnoxLoginView
from rest_framework import status
from django.contrib.auth import login
from rest_framework import status, permissions
from django.http import JsonResponse

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": serializer.data,
            
            "token": AuthToken.objects.create(user)[1]
        })
        


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        # Inicializar el serializer con los datos enviados
        serializer = CustomAuthTokenSerializer(data=request.data)

        # Intentar validar el serializer
        if not serializer.is_valid():
            # Construir una respuesta de error uniforme en JSON
            errors = serializer.errors
            return JsonResponse(
                {
                    "success": False,
                    "error": {
                        "code": "invalid_data",
                        "message": "Se encontraron errores en los datos enviados.",
                        "details": errors,  # Esto incluye los errores del serializer
                    }
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Recuperar el usuario autenticado desde el serializer
        user = serializer.validated_data["user"]

        # Iniciar sesión
        login(request, user)

        # Obtener la respuesta estándar de Knox
        response = super(LoginView, self).post(request, format=None)
        expiry = response.data.get("expiry")
        # Serializar la información del usuario
        user_serializer = CustomUserSerializer(user)

        # Responder con un JSON que combine el token y la información del usuario
        return JsonResponse(
            {   
                "success": True,
                "expiry": expiry,
                "token": response.data["token"],
                "user": user_serializer.data,
            },
            status=status.HTTP_200_OK,
        )
        
        
        
        
class CarruselViewSet(ModelViewSet):
    queryset = Carrusel.objects.order_by('pk')
    serializer_class = CarruselSerializer


class ComentarioViewSet(ModelViewSet):
    queryset = Comentario.objects.order_by('pk')
    serializer_class = ComentarioSerializer


class ConfiguracionViewSet(ModelViewSet):
    queryset = Configuracion.objects.order_by('pk')
    serializer_class = ConfiguracionSerializer


class EventoViewSet(ModelViewSet):
    queryset = Evento.objects.order_by('pk')
    serializer_class = EventoSerializer


class GallosViewSet(ModelViewSet):
    queryset = Gallos.objects.order_by('pk')
    serializer_class = GallosSerializer


class StreamingViewSet(ModelViewSet):
    queryset = Streaming.objects.order_by('pk')
    serializer_class = StreamingSerializer


class UsuarioViewSet(ModelViewSet):
    queryset = CustomUser.objects.order_by('pk')
    serializer_class = UsuarioSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = [    'id', 'nombres', 'apellidos', 'telefono', 'activo', 'pais', 'ciudad', 'email', 'email_verified_at']
    
    search_fields = [
        'nombres', 'apellidos', 'telefono', 'pais', 'ciudad', 'email'
    ]


class ParticipacionGalllosViewSet(ModelViewSet):
    queryset = ParticipacionGalllos.objects.order_by('pk')
    serializer_class = ParticipacionGalllosSerializer


class RegistroEventoViewSet(ModelViewSet):
    queryset = RegistroEvento.objects.order_by('pk')
    serializer_class = RegistroEventoSerializer


class EstadoViewSet(ModelViewSet):
    queryset = Estado.objects.order_by('pk')
    serializer_class = EstadoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['valor', 'clave', 'descripcion', 'identificador_tabla', 'nombre_tabla']
    search_fields = ['valor', 'clave', 'descripcion', 'identificador_tabla', 'nombre_tabla']
    
    
    
    
from django.shortcuts import render

def chat_view(request):
    return render(request, "chat.html")
