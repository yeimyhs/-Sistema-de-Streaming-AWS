from rest_framework.viewsets import ModelViewSet
from streaming.serializers import CarruselSerializer, ComentarioSerializer, ConfiguracionSerializer, EventoSerializer, GallosSerializer, StreamingSerializer, UsuarioSerializer
from streaming.models import Carrusel, Comentario, Configuracion, Evento, Gallos, Streaming
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
        
        
class DuenioViewSet(ModelViewSet):
    queryset = Duenio.objects.order_by('pk')
    serializer_class = DuenioSerializer
    filterset_fields = ['nombres', 'apellidos', 'telefono', 'email', 'estado']
    search_fields = ['nombres', 'apellidos', 'email']
        
        
class GalponViewSet(ModelViewSet):
    queryset = Galpon.objects.order_by('pk')
    serializer_class = GalponSerializer
    filterset_fields = ['titulo', 'idduenio', 'estado']
    search_fields = ['titulo', 'descripcion']
    
class FiestaViewSet(ModelViewSet):
    queryset = Fiesta.objects.order_by('pk')
    serializer_class = FiestaSerializer
    filterset_fields = ['titulo', 'fechainicio', 'fechafin', 'estado', 'precio']
    search_fields = ['titulo', 'descripcion']
    
class CarruselViewSet(ModelViewSet):
    queryset = Carrusel.objects.order_by('pk')
    serializer_class = CarruselSerializer
    filterset_fields = ['titulo', 'fechapublicacion', 'estado']
    search_fields = ['titulo', 'descripcion']


class ComentarioViewSet(ModelViewSet):
    queryset = Comentario.objects.order_by('pk')
    serializer_class = ComentarioSerializer
    filterset_fields = ['idusuario', 'idstreaming', 'estado']
    search_fields = ['comentario']


class ConfiguracionViewSet(ModelViewSet):
    queryset = Configuracion.objects.order_by('pk')
    serializer_class = ConfiguracionSerializer
    filterset_fields = ['nombreweb', 'correo', 'telefono', 'estadostreaming']
    search_fields = ['nombreweb', 'correo']


class EventoViewSet(ModelViewSet):
    queryset = Evento.objects.order_by('pk')
    serializer_class = EventoSerializer
    filterset_fields = ['titulo', 'fechaevento', 'idfiesta', 'estado']
    search_fields = ['titulo', 'descripcion']


class GallosViewSet(ModelViewSet):
    queryset = Gallos.objects.order_by('pk')
    serializer_class = GallosSerializer
    filterset_fields = ['nombre', 'peso', 'color', 'placa', 'anillo', 'experiencia']
    search_fields = ['nombre', 'color', 'placa', 'anillo', 'descripcion']


class StreamingViewSet(ModelViewSet):
    queryset = Streaming.objects.order_by('pk')
    serializer_class = StreamingSerializer
    filterset_fields = ['idevento']
    search_fields = ['nombrevideolife', 'urlstreaming']


class UsuarioViewSet(ModelViewSet):
    queryset = CustomUser.objects.order_by('pk')
    serializer_class = UsuarioSerializer# CustomUserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
            
    filterset_fields = [    'id', 'nombres', 'apellidos', 'telefono', 'eliminado', 'pais', 'ciudad', 'email', 'email_verified_at','is_staff',"estado"]
    
    search_fields = [
        'nombres', 'apellidos', 'telefono', 'pais', 'ciudad', 'email'
    ]


class ParticipacionGallosViewSet(ModelViewSet):
    queryset = ParticipacionGallos.objects.order_by('pk')
    serializer_class = ParticipacionGallosSerializer
    filterset_fields = ['idgallo', 'idevento']
    search_fields = []


class RegistroFiestaViewSet(ModelViewSet):
    queryset = RegistroFiesta.objects.order_by('pk')
    serializer_class = RegistroFiestaSerializer
    filterset_fields = ['idfiesta', 'idusuario', 'estado']
    search_fields = []

class EstadoViewSet(ModelViewSet):
    queryset = Estado.objects.order_by('pk')
    serializer_class = EstadoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['valor', 'clave', 'descripcion', 'identificador_tabla', 'nombre_tabla']
    search_fields = ['valor', 'clave', 'descripcion', 'identificador_tabla', 'nombre_tabla']
    
    

class GalponGallosViewSet(ModelViewSet):
    queryset = GalponGallos.objects.order_by('pk')
    serializer_class = GalponGallosSerializer
    filterset_fields = ['idgallo', 'idgalpon']
    search_fields = []

class GalponFiestaViewSet(ModelViewSet):
    queryset = GalponFiesta.objects.order_by('pk')
    serializer_class = GalponFiestaSerializer
    filterset_fields = ['idfiesta', 'idgalpon']
    search_fields = []


    
from django.shortcuts import render

def chat_view(request):
    return render(request, "chat.html")


import boto3
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class CreateMediaLiveChannel(APIView):
    def post(self, request):
        client = boto3.client(
            'medialive',
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

        try:
            response = client.create_channel(
                Name=request.data.get("name", "DefaultChannel"),
                RoleArn=settings.AWS_MEDIALIVE_ROLE_ARN,
                InputAttachments=[],
                Destinations=[],
                EncoderSettings={},
                Tags={'Project': 'Streaming'}
            )
            return Response(response, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



from django.http import JsonResponse
from .aws_medialive import crear_canal_medialive, listar_canales_medialive
import sys

def generar_stream(request):
    try:
        resultado = crear_canal_medialive()
        
        return JsonResponse({"stream_url": resultado})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def listar_stream(request):
    try:
        resultado = listar_canales_medialive()
        
        return JsonResponse({"canales": resultado})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from . import aws_medialive


@csrf_exempt
def iniciar_canal_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body)
        canal_id = data.get('canal_id')
        if not canal_id:
            return JsonResponse({'error': 'Falta canal_id'}, status=400)

        canal = aws_medialive.iniciar_canal(canal_id)
        return JsonResponse({'mensaje': 'Canal iniciado', 'canal': canal})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def detener_canal_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body)
        canal_id = data.get('canal_id')
        if not canal_id:
            return JsonResponse({'error': 'Falta canal_id'}, status=400)

        canal = aws_medialive.detener_canal(canal_id)
        return JsonResponse({'mensaje': 'Canal detenido', 'canal': canal})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
