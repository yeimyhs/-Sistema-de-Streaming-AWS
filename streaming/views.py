from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from streaming.serializers import CarruselSerializer, ComentarioSerializer, ConfiguracionSerializer, EventoSerializer, GallosSerializer, StreamingSerializer, UsuarioSerializer, ParticipacionGalllosSerializer, RegistroEventoSerializer
from streaming.models import Carrusel, Comentario, Configuracion, Evento, Gallos, Streaming, Usuario, ParticipacionGalllos, RegistroEvento


class CarruselViewSet(ViewSet):

    def list(self, request):
        queryset = Carrusel.objects.order_by('pk')
        serializer = CarruselSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CarruselSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Carrusel.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = CarruselSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Carrusel.objects.get(pk=pk)
        except Carrusel.DoesNotExist:
            return Response(status=404)
        serializer = CarruselSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Carrusel.objects.get(pk=pk)
        except Carrusel.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class ComentarioViewSet(ViewSet):

    def list(self, request):
        queryset = Comentario.objects.order_by('pk')
        serializer = ComentarioSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ComentarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Comentario.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = ComentarioSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Comentario.objects.get(pk=pk)
        except Comentario.DoesNotExist:
            return Response(status=404)
        serializer = ComentarioSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Comentario.objects.get(pk=pk)
        except Comentario.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class ConfiguracionViewSet(ViewSet):

    def list(self, request):
        queryset = Configuracion.objects.order_by('pk')
        serializer = ConfiguracionSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ConfiguracionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Configuracion.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = ConfiguracionSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Configuracion.objects.get(pk=pk)
        except Configuracion.DoesNotExist:
            return Response(status=404)
        serializer = ConfiguracionSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Configuracion.objects.get(pk=pk)
        except Configuracion.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class EventoViewSet(ViewSet):

    def list(self, request):
        queryset = Evento.objects.order_by('pk')
        serializer = EventoSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = EventoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Evento.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = EventoSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Evento.objects.get(pk=pk)
        except Evento.DoesNotExist:
            return Response(status=404)
        serializer = EventoSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Evento.objects.get(pk=pk)
        except Evento.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class GallosViewSet(ViewSet):

    def list(self, request):
        queryset = Gallos.objects.order_by('pk')
        serializer = GallosSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = GallosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Gallos.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = GallosSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Gallos.objects.get(pk=pk)
        except Gallos.DoesNotExist:
            return Response(status=404)
        serializer = GallosSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Gallos.objects.get(pk=pk)
        except Gallos.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class StreamingViewSet(ViewSet):

    def list(self, request):
        queryset = Streaming.objects.order_by('pk')
        serializer = StreamingSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = StreamingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Streaming.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = StreamingSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Streaming.objects.get(pk=pk)
        except Streaming.DoesNotExist:
            return Response(status=404)
        serializer = StreamingSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Streaming.objects.get(pk=pk)
        except Streaming.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class UsuarioViewSet(ViewSet):

    def list(self, request):
        queryset = Usuario.objects.order_by('pk')
        serializer = UsuarioSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Usuario.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = UsuarioSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = Usuario.objects.get(pk=pk)
        except Usuario.DoesNotExist:
            return Response(status=404)
        serializer = UsuarioSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = Usuario.objects.get(pk=pk)
        except Usuario.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class ParticipacionGalllosViewSet(ViewSet):

    def list(self, request):
        queryset = ParticipacionGalllos.objects.order_by('pk')
        serializer = ParticipacionGalllosSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ParticipacionGalllosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = ParticipacionGalllos.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = ParticipacionGalllosSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = ParticipacionGalllos.objects.get(pk=pk)
        except ParticipacionGalllos.DoesNotExist:
            return Response(status=404)
        serializer = ParticipacionGalllosSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = ParticipacionGalllos.objects.get(pk=pk)
        except ParticipacionGalllos.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class RegistroEventoViewSet(ViewSet):

    def list(self, request):
        queryset = RegistroEvento.objects.order_by('pk')
        serializer = RegistroEventoSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = RegistroEventoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = RegistroEvento.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = RegistroEventoSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            item = RegistroEvento.objects.get(pk=pk)
        except RegistroEvento.DoesNotExist:
            return Response(status=404)
        serializer = RegistroEventoSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            item = RegistroEvento.objects.get(pk=pk)
        except RegistroEvento.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)
