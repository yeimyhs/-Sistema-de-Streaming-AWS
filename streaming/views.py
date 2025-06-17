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
    filterset_fields = ['titulo', 'idduenio', 'estado', 'pais']
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
    queryset = Evento.objects.prefetch_related(
    'evento_gallos_vs__idgallo1',
    'evento_gallos_vs__idgallo2',
    'evento_gallos_vs__idgalpon1',
    'evento_gallos_vs__idgalpon2',
).order_by('pk')
    serializer_class = EventoSerializer
    filterset_fields = ['titulo', 'fechaevento', 'idfiesta', 'estado', 'isstreaming']
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
    filterset_fields = ['idgallo1', 'idgallo2','idevento', 'culminacion1', 'culminacion2', 'idgalpon1','idgalpon2','idgalponganador' ]
    search_fields = []

from django.db.models import Prefetch
class RegistroFiestaViewSet(ModelViewSet):
    queryset = RegistroFiesta.objects.prefetch_related(
        Prefetch(
            'idfiesta__eventos__streaming_set',
            queryset=Streaming.objects.all()
        ),
        'idfiesta__eventos'
    ).select_related('idfiesta', 'idusuario')
    serializer_class = RegistroFiestaSerializer
    filterset_fields = ['idfiesta', 'idusuario', 'estado']
    search_fields = []

class EstadoViewSet(ModelViewSet):
    queryset = Estado.objects.order_by('pk')
    serializer_class = EstadoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['valor', 'clave', 'descripcion', 'identificador_tabla', 'nombre_tabla']
    search_fields = ['valor', 'clave', 'descripcion', 'identificador_tabla', 'nombre_tabla']
    
    

#class GalponGallosViewSet(ModelViewSet):
 #   queryset = GalponGallos.objects.order_by('pk')
  #  serializer_class = GalponGallosSerializer
   # filterset_fields = ['idgallo', 'idgalpon']
    #search_fields = []

class GalponFiestaViewSet(ModelViewSet):
    queryset = GalponFiesta.objects.order_by('pk')
    serializer_class = GalponFiestaSerializer
    filterset_fields = ['idfiesta', 'idgalpon']
    search_fields = []
    
    def perform_create(self, serializer):
        galpon_fiesta = serializer.save()
        gallos = Gallos.objects.filter(idgalpon=galpon_fiesta.idgalpon, eliminado=0)
        for gallo in gallos:
            GalponGalloFiesta.objects.create(
                idgalponfiesta=galpon_fiesta,
                idgallo=gallo
            )
class GalponGalloFiestaViewSet(ModelViewSet):
    queryset = GalponGalloFiesta.objects.order_by('pk')
    serializer_class = GalponGalloFiestaSerializer
    filterset_fields = ['idgalponfiesta', 'idgallo']
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


@csrf_exempt
def generar_stream(request):
    try:
        data = json.loads(request.body)
        nombrecanal = data.get("nombrecanal")
        
        if not nombrecanal:
            return JsonResponse({"error": "Falta el nombre del canal"}, status=400)

        
        resultado = crear_canal_medialive(nombrecanal)
        configuracion, creada = Configuracion.objects.get_or_create(
        idconf=1,  # O usa otro campo único si prefieres
        defaults={
            'nombreweb': 'Mi Web',
            'correo': 'correo@ejemplo.com',
            'telefono': '123456789',
            'estadostreaming': 0,
            
            'channel_id':'',
            'urlinput1': '',
            'urlinput2': '',
            'urloutput': '',
            'nombrecanal': ''
        }
        )
        primer_rtmp = resultado.get("rtmp_input_urls", [None])[0]
        seg_rtmp = resultado.get("rtmp_input_urls", [None])[1]
        primer_hls = resultado.get("hls_output_url")
        channel_id = resultado.get("channel_id")

        configuracion.urlinput1 = primer_rtmp
        configuracion.urlinput2 = seg_rtmp
        configuracion.urloutput = primer_hls
        configuracion.channel_id = channel_id
        configuracion.nombrecanal = nombrecanal

        configuracion.estadostreaming = 0  # Marcar como activo
        configuracion.save()

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
        configuracion = Configuracion.objects.get(idconf = 1)
        
        canal_id = configuracion.channel_id
        if not canal_id:
            return JsonResponse({'error': 'Falta canal_id en la configuracion'}, status=400)

        
        canal = aws_medialive.iniciar_canal(canal_id)
        data = json.loads(request.body)
        idevento = data.get("idevento")
        evento = Evento.objects.get(idevento = idevento)
        evento.isstreaming = 1
        evento.save()
        
        return JsonResponse({'mensaje': 'Canal iniciado', 'canal': canal})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


CLOUDFRONT_DOMAIN = "d17y4wxxn3lf6q.cloudfront.net"  # Tu dominio de CloudFront

@csrf_exempt
def detener_canal_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body)
        idstreaming = data.get("idstreaming")
        idevento = data.get("idevento")
        evento = Evento.objects.get(idevento = idevento)
        evento.isstreaming = 2
        evento.save()
        configuracion = Configuracion.objects.get(idconf = 1)
        canal_id = configuracion.channel_id
        nombre_canal = configuracion.nombrecanal

        if not canal_id or not nombre_canal:
            return JsonResponse({'error': 'Faltan datos en configuracion'}, status=400)

        canal = aws_medialive.detener_canal(canal_id)
        
        streaming = Streaming.objects.get(idstreaming = idstreaming)
        nombrestreming = streaming.nombrevideolife
        
        # 🧠 Mover grabación y obtener nueva ubicación
        nueva_ubicacion = aws_medialive.mover_grabacion_a_nueva_ubicacion(canal_id, nombre_canal, nombrestreming)

        # 🛰️ Construir enlace a CloudFront
        url_playlist = f"https://{CLOUDFRONT_DOMAIN}/{nueva_ubicacion}playlist.m3u8"

        streaming = Streaming.objects.get(idstreaming = idstreaming)
        streaming.urlgrabacion = url_playlist
        streaming.save()
        return JsonResponse({
            'mensaje': 'Canal detenido y grabación archivada',
            'canal': canal,
            'url_grabacion': url_playlist
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
from django.views.decorators.http import require_http_methods


@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_recursos_medialive(request):
    success, mensaje = aws_medialive.eliminar_todos_canales_y_entradas()
    if success:
        try:
            configuracion = Configuracion.objects.first()
            if configuracion:
                configuracion.estadostreaming = None
                configuracion.channel_id = None
                configuracion.urlinput1 = None
                configuracion.urlinput2 = None
                configuracion.urloutput = None
                configuracion.nombrecanal = None
                configuracion.save()

            return JsonResponse({"message": "Canales eliminados y configuración actualizada."}, status=200)
        except Exception as e:
            return JsonResponse({"error": f"Error al limpiar configuración: {str(e)}"}, status=500)
    else:
        return JsonResponse({"error": mensaje}, status=500)
from django.http import JsonResponse
from django.shortcuts import render
from .consumers import encrypt_channel_name

def chat_page(request, room_name):
    # Generamos el token encriptado para el canal
    token = encrypt_channel_name(room_name)
    return render(request, 'chat.html', {
        'room_name': room_name,
        'token': token
    })
    
    
    
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def chat_view_comment(request, streaming_id):
    return render(request, 'comentario/chat.html', {
        'streaming_id': streaming_id,
        'user_id': request.user.id if request.user.is_authenticated else 1  # usuario demo
    })
    
def sschat_view_comment(request):
    return render(request, 'comentario/chat.html')



from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import ParticipacionGallos, Galpon
from datetime import timedelta


class RankingView(APIView):
    def get(self, request):
        participaciones = ParticipacionGallos.objects.select_related(
            'idgalpon1', 'idgalpon2', 'idgalponganador'
        ).all()

        galpon_stats = {}

        for p in participaciones:
            g1 = p.idgalpon1
            g2 = p.idgalpon2
            ganador = p.idgalponganador

            # Inicializar datos
            for g in [g1, g2]:
                if g and g.pk not in galpon_stats:
                    galpon_stats[g.pk] = {
                        'galpon': g,
                        'pg': 0,
                        'pe': 0,
                        'pp': 0,
                        'puntaje': 0,
                        'tiempo': timedelta(0),
                    }

            # Acumular tiempo de pelea
            if p.duracion:
                if g1:
                    galpon_stats[g1.pk]['tiempo'] += p.duracion
                if g2:
                    galpon_stats[g2.pk]['tiempo'] += p.duracion

            # Procesar resultado
            if ganador:
                galpon_stats[ganador.pk]['pg'] += 1
                perdedor = g1 if ganador == g2 else g2
                if perdedor:
                    galpon_stats[perdedor.pk]['pp'] += 1
            elif (p.culminacion1 == '2' or p.culminacion2 == '2'):
                # Empate declarado
                if g1:
                    galpon_stats[g1.pk]['pe'] += 1
                if g2:
                    galpon_stats[g2.pk]['pe'] += 1
            else:
                # Resultado no claro, se omite
                continue

        # Calcular puntaje (3 por victoria, 1 por empate)
        for stats in galpon_stats.values():
            stats['puntaje'] = stats['pg'] * 3 + stats['pe']

        # Ordenar
        ranking = sorted(
            galpon_stats.values(),
            key=lambda x: (-x['puntaje'], x['tiempo'])
        )

        # Formatear respuesta
        response_data = []
        for idx, item in enumerate(ranking, start=1):
            galpon = item['galpon']
            response_data.append({
                'nro': idx,
                'galpon': galpon.titulo,
                'propietario': f"{galpon.idduenio.nombres} {galpon.idduenio.apellidos}" if galpon.idduenio else "Sin dueño",
                'pais': galpon.pais if galpon.pais else "Desconocido",
                'pg': item['pg'],
                'pe': item['pe'],
                'pp': item['pp'],
                'puntaje': item['puntaje'],
                'tiempo': item['tiempo'],
            })

        return Response(response_data)

from rest_framework.decorators import api_view
@api_view(['POST'])
def asignar_gallos_a_galpon(request):
    ids_gallos = request.data.get('ids_gallos')
    id_galpon = request.data.get('id_galpon')

    if not ids_gallos or not id_galpon:
        return Response({'error': 'Faltan parámetros'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        galpon = Galpon.objects.get(pk=id_galpon)
    except Galpon.DoesNotExist:
        return Response({'error': 'Galpón no existe'}, status=status.HTTP_404_NOT_FOUND)

    gallos_actualizados = Gallos.objects.filter(idgallo__in=ids_gallos, eliminado=0)
    updated_count = gallos_actualizados.update(idgalpon=galpon)

    return Response({
        'mensaje': f'Se actualizaron {updated_count} gallos al galpón {galpon.idgalpon}.'
    }, status=status.HTTP_200_OK)
    


import random
import itertools
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Evento, GalponFiesta, GalponGalloFiesta, Gallos, ParticipacionGallos

@api_view(['POST'])
def asignar_vs_por_experiencia_aleatoria(request):
    idevento = request.data.get('idevento')
    id_galpones = request.data.get('id_galpones')

    if not idevento or not id_galpones:
        return Response({'error': 'Faltan parámetros.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        evento = Evento.objects.get(pk=idevento)
    except Evento.DoesNotExist:
        return Response({'error': 'Evento no existe.'}, status=status.HTTP_404_NOT_FOUND)

    idfiesta = evento.idfiesta_id

    galpones_inscritos = GalponFiesta.objects.filter(idfiesta=idfiesta, idgalpon__in=id_galpones)
    if galpones_inscritos.count() != len(id_galpones):
        return Response({'error': 'Uno o más galpones no están inscritos en la fiesta.'}, status=status.HTTP_400_BAD_REQUEST)

    gallos_data = []
    for gf in galpones_inscritos:
        gallos_fiesta = GalponGalloFiesta.objects.filter(idgalponfiesta=gf).select_related('idgallo')
        for g in gallos_fiesta:
            gallos_data.append({
                'idgallo': g.idgallo.idgallo,
                'experiencia': g.idgallo.experiencia,
                'idgalpon': gf.idgalpon_id
            })

    if len(gallos_data) % 2 != 0:
        return Response({'error': 'Número impar de gallos. No se puede asignar VS.'}, status=status.HTTP_400_BAD_REQUEST)

    # Randomizar gallos dentro del margen de experiencia
    gallos_data.sort(key=lambda g: g['experiencia'])

    # Randomizar dentro del margen de ±1
    gallos_aleatorios = []
    for galpon in set(g['idgalpon'] for g in gallos_data):
        gallos_del_galpon = [g for g in gallos_data if g['idgalpon'] == galpon]
        random.shuffle(gallos_del_galpon)  # Aleatorizamos dentro del galpón
        gallos_aleatorios.extend(gallos_del_galpon)

    # Buscar pares de gallos con experiencia similar (±1)
    vs_generados = []
    usados = set()

    for i, g1 in enumerate(gallos_aleatorios):
        if g1['idgallo'] in usados:
            continue
        for j in range(i + 1, len(gallos_aleatorios)):
            g2 = gallos_aleatorios[j]
            if g2['idgallo'] in usados:
                continue
            # Diferente galpón y experiencia similar (por ejemplo, ±1)
            if g1['idgalpon'] != g2['idgalpon'] and abs(g1['experiencia'] - g2['experiencia']) <= 1:
                vs_generados.append({
                    'idgallo1': g1['idgallo'],
                    'idgallo2': g2['idgallo'],
                    'idevento': idevento,
                    'idgalpon1': g1['idgalpon'],
                    'idgalpon2': g2['idgalpon'],
                })
                usados.add(g1['idgallo'])
                usados.add(g2['idgallo'])
                break

    # Si hay gallos no emparejados, intentar asignarles la experiencia más cercana
    gallos_no_emparejados = [g for g in gallos_aleatorios if g['idgallo'] not in usados]
    if gallos_no_emparejados:
        for g in gallos_no_emparejados:
            # Buscar el gallo con la experiencia más cercana para emparejarlo
            gallo_con_menor_diferencia = None
            menor_diferencia = float('inf')
            for g2 in gallos_no_emparejados:
                if g != g2 and abs(g['experiencia'] - g2['experiencia']) < menor_diferencia:
                    menor_diferencia = abs(g['experiencia'] - g2['experiencia'])
                    gallo_con_menor_diferencia = g2

            if gallo_con_menor_diferencia:
                vs_generados.append({
                    'idgallo1': g['idgallo'],
                    'idgallo2': gallo_con_menor_diferencia['idgallo'],
                    'idevento': idevento,
                    'idgalpon1': g['idgalpon'],
                    'idgalpon2': gallo_con_menor_diferencia['idgalpon'],
                })
                usados.add(g['idgallo'])
                usados.add(gallo_con_menor_diferencia['idgallo'])
                gallos_no_emparejados.remove(gallo_con_menor_diferencia)

    # Si no se pudieron emparejar todos, mostrar mensaje de los gallos que no fueron emparejados
    if len(usados) != len(gallos_data):
        gallos_restantes = [g['idgallo'] for g in gallos_no_emparejados]
        return Response({
            'error': 'No se pudo emparejar a todos los gallos. Algunos fueron emparejados con la experiencia más cercana.',
            'gallos_no_emparejados': gallos_restantes
        }, status=status.HTTP_400_BAD_REQUEST)

    # Guardar en la base de datos
    for vs in vs_generados:
        # Obtener las instancias de los gallos usando el ID
        idgallo1_instance = Gallos.objects.get(idgallo=vs['idgallo1'])
        idgallo2_instance = Gallos.objects.get(idgallo=vs['idgallo2'])
        idgalpon1_instance = Galpon.objects.get(idgalpon=vs['idgalpon1'])
        idgalpon2_instance = Galpon.objects.get(idgalpon=vs['idgalpon2'])

        # Crear la participación
        ParticipacionGallos.objects.create(
            idgallo1=idgallo1_instance,
            idgallo2=idgallo2_instance,
            idevento=evento,
            idgalpon1=idgalpon1_instance,
            idgalpon2=idgalpon2_instance,
        )

    return Response({
        'mensaje': f'{len(vs_generados)} enfrentamientos generados con éxito.',
        'gallos_emparejados': vs_generados
    }, status=status.HTTP_201_CREATED)




from django.db import transaction
from .models import (
    Fiesta, Evento, Gallos, GalponFiesta,
    GalponGalloFiesta, ParticipacionGallos
)
import random
from collections import defaultdict

@transaction.atomic
def asignar_versus_por_fiesta(idfiesta):
    # 1. Obtener eventos de la fiesta
    eventos = list(Evento.objects.filter(idfiesta_id=idfiesta, eliminado=0))
    if not eventos:
        raise Exception("La fiesta no tiene eventos activos")

    # 2. Obtener gallos de la fiesta y su galpón
    inscripciones = GalponGalloFiesta.objects.filter(
        idgalponfiesta__idfiesta_id=idfiesta,
        eliminado=0
    ).select_related('idgallo', 'idgalponfiesta__idgalpon')

    gallos_info = []
    for ins in inscripciones:
        gallos_info.append({
            'gallo': ins.idgallo,
            'galpon_id': ins.idgalponfiesta.idgalpon.idgalpon,
            'experiencia': ins.idgallo.experiencia
        })

    # 3. Agrupar por nivel de experiencia
    experiencia_niveles = defaultdict(list)
    for info in gallos_info:
        exp = info['experiencia']
        if exp >= 10:
            experiencia_niveles['alta'].append(info)
        elif exp >= 4:
            experiencia_niveles['media'].append(info)
        else:
            experiencia_niveles['baja'].append(info)

    # 4. Emparejar por niveles, evitando gallos del mismo galpón
    emparejamientos = []

    def emparejar_grupo(gallos_grupo):
        random.shuffle(gallos_grupo)
        emparejados = []
        usados = set()
        for i, g1 in enumerate(gallos_grupo):
            if i in usados:
                continue
            for j in range(i+1, len(gallos_grupo)):
                g2 = gallos_grupo[j]
                if j in usados:
                    continue
                if g1['galpon_id'] != g2['galpon_id']:
                    emparejados.append((g1, g2))
                    usados.update([i, j])
                    break
        no_emparejados = [g for idx, g in enumerate(gallos_grupo) if idx not in usados]
        return emparejados, no_emparejados

    niveles = ['alta', 'media', 'baja']
    pendientes = []
    for i, nivel in enumerate(niveles):
        grupo = experiencia_niveles[nivel] + pendientes
        parejas, pendientes = emparejar_grupo(grupo)
        emparejamientos.extend(parejas)

    # 5. Repartir emparejamientos entre eventos
    eventos_cycle = eventos * ((len(emparejamientos) // len(eventos)) + 1)
    eventos_cycle = eventos_cycle[:len(emparejamientos)]

    lista_parejas = []  # <-- Aquí se almacenarán los resultados para retornar

    for (g1, g2), evento in zip(emparejamientos, eventos_cycle):
        ParticipacionGallos.objects.create(
            idgallo1=g1['gallo'],
            idgallo2=g2['gallo'],
            idevento=evento,
            idgalpon1_id=g1['galpon_id'],
            idgalpon2_id=g2['galpon_id'],
        )
        lista_parejas.append({
            'evento': evento.titulo,
            'gallo1': g1['gallo'].nombre,
            'galpon1': g1['galpon_id'],
            'gallo2': g2['gallo'].nombre,
            'galpon2': g2['galpon_id'],
        })

    return {
        'mensaje': f"Se asignaron {len(emparejamientos)} peleas a {len(eventos)} eventos.",
        'parejas': lista_parejas
    }

@api_view(['POST'])
def generar_emparejamientos(request, pk):
    try:
        resultado = asignar_versus_por_fiesta(pk)
        return Response({'mensaje': resultado}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)