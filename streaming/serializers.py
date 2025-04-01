from rest_framework.serializers import ModelSerializer
from streaming.models import Carrusel, Comentario, Configuracion, Evento, Gallos, Streaming

from .models import *

from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
User = get_user_model()

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


class EventoSerializer(ModelSerializer):
    gallosvs = serializers.SerializerMethodField()

    class Meta:
        model = Evento
        fields = '__all__'
    def get_gallosvs(self, obj):
        return GallosSerializer(Gallos.objects.filter(idgallo__in=obj.evento_gallos_vs.values_list('idgallo', flat=True)), many=True).data


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


class GalponSerializer(ModelSerializer):
    iddueniodetalle = DuenioSerializer(source='idduenio', read_only=True) 
    #gallos = GallosSerializer(many=True, read_only=True, source='galpon_gallos.all')
    gallos = serializers.SerializerMethodField()
    class Meta:
        model = Galpon
        fields = '__all__'
    def get_gallos(self, obj):
        return GallosSerializer(Gallos.objects.filter(idgallo__in=obj.galpon_gallos.values_list('idgallo', flat=True)), many=True).data

        #return GallosSerializer(obj.galpon_gallos.values_list('idgallo', flat=True), many=True).data
    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self.fields['gallos'] = GallosSerializer(many=True, read_only=True, source='galpon_gallos.all')


        
class FiestaSerializer(ModelSerializer):
    class Meta:
        model = Fiesta
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['eventos'] = EventoSerializer(many=True, read_only=True) 

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
