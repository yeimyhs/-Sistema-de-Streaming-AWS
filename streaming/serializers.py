from rest_framework.serializers import ModelSerializer
from streaming.models import Carrusel, Comentario, Configuracion, Evento, Gallos, Streaming

from .models import *

from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
User = get_user_model()

class RankingSerializer(serializers.Serializer):
    nro = serializers.IntegerField()
    galpon = serializers.CharField()
    propietario = serializers.CharField()
    pais = serializers.CharField()
    pg = serializers.IntegerField()
    pe = serializers.IntegerField()
    pp = serializers.IntegerField()
    puntaje = serializers.IntegerField()
    tiempo = serializers.DurationField()
    
class CustomUserSerializer(ModelSerializer):
    class Meta:
        #depth = 1
        model = CustomUser
        fields = ['eliminado',
            'id',
            "nombres",
            "apellidos",
            "fechacreacion",
            "telefono",
            "fotoperfil",
            "pais",
            "ciudad",
            "email",
            "estado",
            
            'email_verified_at',
            'remember_token',
            'is_staff',
        ]

class RegisterSerializer(ModelSerializer):
    class Meta:
        #depth = 1
        model = CustomUser
        fields = [
            'password',
             
            "nombres",
            "apellidos",
            "fechacreacion",
            "telefono",
            "fotoperfil",
            "eliminado",
            "pais",
            "estado",
            "ciudad",
            "email",
        ]
        extra_kwargs = {'password': {'write_only': True}}

class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label="Email del usuario")
    password = serializers.CharField(label="Contraseña", style={"input_type": "password"})

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # Validar si faltan campos
        if not email and not password:
            raise serializers.ValidationError(
                {
                    "error": {
                        "code": "missing_fields",
                        "message": "El nombre de usuario y la contraseña son obligatorios."
                    }
                },
                code="authorization",
            )
        elif not email:
            raise serializers.ValidationError(
                {
                    "error": {
                        "code": "missing_username",
                        "message": "El nombre de usuario es obligatorio."
                    }
                },
                code="authorization",
            )
        elif not password:
            raise serializers.ValidationError(
                {
                    "error": {
                        "code": "missing_password",
                        "message": "La contraseña es obligatoria."
                    }
                },
                code="authorization",
            )

        # Autenticar al usuario
        #user = authenticate(email=email, password=password)
       
        user = CustomUser.objects.get(email=email)  # Buscar usuario por email
        print(user)

        if check_password(password, user.password):  # Comparar contraseñas
            print("---")
    
        # Validar credenciales inválidas
        if not user:
            raise serializers.ValidationError(
                {
                    "error": {
                        "code": "invalid_credentials",
                        "message": "Las credenciales proporcionadas no son válidas. Por favor, intente de nuevo."
                    }
                },
                code="authorization",
            )

        # Verificar si la cuenta está deshabilitada
        if  user.eliminado:
            raise serializers.ValidationError(
                {
                    "error": {
                        "code": "account_disabled",
                        "message": "Esta cuenta está deshabilitada. Contacte con el administrador."
                    }
                },
                code="authorization",
            )

        # Validar si el usuario está inactivo
        if not user.is_active:
            raise serializers.ValidationError(
                {
                    "error": {
                        "code": "account_inactive",
                        "message": "Esta cuenta está inactiva. Por favor, contacte con el administrador."
                    }
                },
                code="authorization",
            )

        # Si todo es válido, se retorna el usuario
        attrs["user"] = user
        return attrs
    
    

    
class GalponFiestaSerializer(ModelSerializer):

    class Meta:
        model = GalponFiesta
        fields = '__all__'

#class GalponGallosSerializer(ModelSerializer):

#    class Meta:
#        model = GalponGallos
#        fields = '__all__'
        
class DuenioSerializer(ModelSerializer):

    class Meta:
        model = Duenio
        fields = '__all__'
   
   
    
    
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

class GallosidGalponSerializer(ModelSerializer):
    galpondetalle = serializers.SerializerMethodField()

    class Meta:
        model = Gallos
        fields = '__all__'



class EventoSerializer(ModelSerializer):
    gallosvs = serializers.SerializerMethodField()

    class Meta:
        model = Evento
        fields = '__all__'

    def get_gallosvs(self, obj):
        participaciones = obj.evento_gallos_vs.filter(eliminado=0)
        serializer = ParticipacionGallosSerializer(participaciones, many=True)
        return serializer.data


class OnlyGalponSerializer(ModelSerializer):
    iddueniodetalle = DuenioSerializer(source='idduenio', read_only=True) 
    class Meta:
        model = Galpon
        fields = '__all__'

class OnlyGalponGallosDuenioSerializer(ModelSerializer):
    iddueniodetalle = DuenioSerializer(source='idduenio', read_only=True) 
    class Meta:
        model = Galpon
        fields = '__all__'
              
        
class GallosSerializer(ModelSerializer):
    galpondetalle = OnlyGalponSerializer(source='idgalpon', read_only=True)
    
    class Meta:
        model = Gallos
        fields = '__all__'
        

class OnlyGallosSerializer(ModelSerializer):
    class Meta:
        model = Gallos
        fields = '__all__'


class GalponSerializer(ModelSerializer):
    iddueniodetalle = DuenioSerializer(source='idduenio', read_only=True) 
    #gallos = serializers.SerializerMethodField()
    gallos = OnlyGallosSerializer(many=True, read_only=True, source='idgalpon_actualmente.all')
    #gallos = GallosSerializer(many=True, read_only=True, source='galpon_gallos.all')
    #!!!
    #gallos = serializers.SerializerMethodField()
    class Meta:
        model = Galpon
        fields = '__all__'
        
   
    #def get_gallos(self, obj):
    #    galpon_gallos = GalponGallos.objects.select_related('idgallo').filter(idgalpon=obj)
    #    return [
    #        {
    #            "idgalpongallos": gg.idgalpongallos,
    #            "idgallo": gg.idgallo.idgallo,
    #            "gallo": OnlyGallosSerializer(gg.idgallo).data
    #        }
    #        for gg in galpon_gallos
    #    ]
        
    #!!
        #return GallosSerializer(obj.galpon_gallos.values_list('idgallo', flat=True), many=True).data
    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self.fields['gallos'] = GallosSerializer(many=True, read_only=True, source='galpon_gallos.all')


class OnlyGalloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallos
        fields = ['idgallo', 'nombre']


class GalponSerializerConGallos(serializers.ModelSerializer):
    gallos = serializers.SerializerMethodField()
    iddueniodetalle = DuenioSerializer(source='idduenio', read_only=True) 

    class Meta:
        model = Galpon
        fields = ['idgalpon', 'titulo', 'fechacreacion', 'descripcion', 'pais', 'gallos', 'iddueniodetalle']

    def get_gallos(self, obj):
        fiesta = self.context.get('fiesta')
        if not fiesta:
            return []
        inscritos = GalponGalloFiesta.objects.filter(
            idgalponfiesta__idgalpon=obj,
            idgalponfiesta__idfiesta=fiesta
        ).select_related('idgallo')
        return OnlyGalloSerializer([i.idgallo for i in inscritos], many=True).data
       
class FiestaSerializer(ModelSerializer):
    galpones = serializers.SerializerMethodField()    
    eventos = serializers.SerializerMethodField()

    class Meta:
        model = Fiesta
        fields = '__all__'

    def get_eventos(self, obj):
        eventos = Evento.objects.filter(idfiesta=obj).prefetch_related(
            'evento_gallos_vs__idgallo1',
            'evento_gallos_vs__idgallo2',
            'evento_gallos_vs__idgalpon1',
            'evento_gallos_vs__idgalpon2',
        )
        return EventoSerializer(eventos, many=True).data

    def get_galpones(self, obj):
        galpon_fiesta_qs = GalponFiesta.objects.filter(idfiesta=obj).select_related('idgalpon')
        galpones = [gf.idgalpon for gf in galpon_fiesta_qs]
        serializer = GalponSerializerConGallos(galpones, many=True, context={'fiesta': obj})
        return serializer.data

class OnlyFiestaSerializer(ModelSerializer):
    class Meta:
        model = Fiesta
        fields = '__all__'
        
class StreamingSerializer(ModelSerializer):
    class Meta:
        model = Streaming
        fields = '__all__'


class UsuarioSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = '__all__'
#-----------------------------------------
class GalloSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallos
        fields = '__all__' # ajusta según tu modelo

class GalponConGallosSerializer(serializers.ModelSerializer):
    gallos = serializers.SerializerMethodField()
    iddueniodetalle = DuenioSerializer(source='idduenio', read_only=True) 

    class Meta:
        model = Galpon
        fields = ['idgalpon', 'titulo', 'gallos','iddueniodetalle']

    def get_gallos(self, galpon):
        fiesta_id = self.context.get("fiesta_id")
        if not fiesta_id:
            return []

        galpon_fiesta = GalponFiesta.objects.filter(
            idgalpon=galpon,
            idfiesta=fiesta_id
        ).first()

        if not galpon_fiesta:
            return []

        gallo_qs = Gallos.objects.filter(
            idgallo_galpon_fiesta_inscripcion__idgalponfiesta=galpon_fiesta
        ).distinct()

        return GalloSimpleSerializer(gallo_qs, many=True).data


class ParticipacionGallosSerializer(serializers.ModelSerializer):
    galpon1_detalle_completo = serializers.SerializerMethodField()
    galpon2_detalle_completo = serializers.SerializerMethodField()
    gallodetalle = OnlyGalloSerializer(source='idgallo1', read_only=True)
    gallodetalle = OnlyGalloSerializer(source='idgallo2', read_only=True)

    class Meta:
        model = ParticipacionGallos
        fields = '__all__'

    def get_fiesta_id(self, obj):
        return obj.idevento.idfiesta_id if obj.idevento and obj.idevento.idfiesta_id else None

    def get_galpon_detalle(self, galpon, fiesta_id):
        context = {'fiesta_id': fiesta_id}
        return GalponConGallosSerializer(galpon, context=context).data if galpon and fiesta_id else None

    def get_galpon1_detalle_completo(self, obj):
        fiesta_id = self.get_fiesta_id(obj)
        return self.get_galpon_detalle(obj.idgalpon1, fiesta_id)

    def get_galpon2_detalle_completo(self, obj):
        fiesta_id = self.get_fiesta_id(obj)
        return self.get_galpon_detalle(obj.idgalpon2, fiesta_id)


class RegistroFiestaSerializer(ModelSerializer):
    fiestadetalle = OnlyFiestaSerializer(source='idfiesta', read_only=True) 
    userdetalle = CustomUserSerializer(source='idusuario', read_only=True) 

    class Meta:
        model = RegistroFiesta
        fields = '__all__'

class EstadoSerializer(ModelSerializer):

    class Meta:
        model = Estado
        fields = '__all__'

class GalponGalloFiestaSerializer(ModelSerializer):

    class Meta:
        model = GalponGalloFiesta
        fields = '__all__'
