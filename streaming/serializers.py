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

class GalponGallosSerializer(ModelSerializer):

    class Meta:
        model = GalponGallos
        fields = '__all__'
        
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

    def get_galpondetalle(self, obj):
        gallos_ids = set(obj.gallo_galpondetalle.values_list('idgalpon', flat=True))
        fiesta_ids = set(self.context.get('galpon_ids_fiesta', []))
        interseccion_ids = gallos_ids & fiesta_ids

        galpon = Galpon.objects.filter(idgalpon__in=interseccion_ids).first()
        if galpon:
            return OnlyGalponSerializer(galpon).data
        return None

class EventoSerializer(ModelSerializer):
    gallosvs = serializers.SerializerMethodField()

    class Meta:
        model = Evento
        fields = '__all__'

    def get_gallosvs(self, obj):
        participaciones = ParticipacionGallos.objects.select_related('idgallo1', 'idgallo2').filter(idevento=obj)

        galpon_ids_fiesta = GalponFiesta.objects.filter(idfiesta=obj.idfiesta).values_list('idgalpon', flat=True)

        return [
            {
                "idparticipacion": p.idparticipacion,
                "idgallo1": p.idgallo1.idgallo,
                "gallo1": GallosidGalponSerializer(p.idgallo1, context={'galpon_ids_fiesta': galpon_ids_fiesta}).data,
                "idgallo2": p.idgallo2.idgallo,
                "gallo2": GallosidGalponSerializer(p.idgallo2, context={'galpon_ids_fiesta': galpon_ids_fiesta}).data,
            }
            for p in participaciones
        ]


class OnlyGalponSerializer(ModelSerializer):
    iddueniodetalle = DuenioSerializer(source='idduenio', read_only=True) 
    class Meta:
        model = Galpon
        fields = '__all__'

        
        
class GallosSerializer(ModelSerializer):
    galpondetalle = serializers.SerializerMethodField()
    
    class Meta:
        model = Gallos
        fields = '__all__'
        
    def get_galpondetalle(self, obj):
        return OnlyGalponSerializer(Galpon.objects.filter(idgalpon__in=obj.gallo_galpondetalle.values_list('idgalpon', flat=True)), many=True).data


class OnlyGallosSerializer(ModelSerializer):
    class Meta:
        model = Gallos
        fields = '__all__'


class GalponSerializer(ModelSerializer):
    iddueniodetalle = DuenioSerializer(source='idduenio', read_only=True) 
    #gallos = GallosSerializer(many=True, read_only=True, source='galpon_gallos.all')
    gallos = serializers.SerializerMethodField()
    class Meta:
        model = Galpon
        fields = '__all__'
    def get_gallos(self, obj):
        galpon_gallos = GalponGallos.objects.select_related('idgallo').filter(idgalpon=obj)
        return [
            {
                "idgalpongallos": gg.idgalpongallos,
                "idgallo": gg.idgallo.idgallo,
                "gallo": OnlyGallosSerializer(gg.idgallo).data
            }
            for gg in galpon_gallos
        ]
        #return GallosSerializer(obj.galpon_gallos.values_list('idgallo', flat=True), many=True).data
    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self.fields['gallos'] = GallosSerializer(many=True, read_only=True, source='galpon_gallos.all')


        
class FiestaSerializer(ModelSerializer):
    galpones = serializers.SerializerMethodField()
    class Meta:
        model = Fiesta
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['eventos'] = EventoSerializer(many=True, read_only=True) 
        
    def get_galpones(self, obj):
        galpon_fiesta = GalponFiesta.objects.select_related('idgalpon').filter(idfiesta=obj)
        return [
            {
                "idgalponfiesta": gf.idgalponfiesta,
                "idgalpon": gf.idgalpon.idgalpon,
                "galpon": GalponSerializer(gf.idgalpon).data
            }
            for gf in galpon_fiesta
        ]

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


class ParticipacionGallosSerializer(ModelSerializer):

    class Meta:
        model = ParticipacionGallos
        fields = '__all__'


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
