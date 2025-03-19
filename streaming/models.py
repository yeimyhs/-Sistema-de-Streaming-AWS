# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field BigAutoField primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remov` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models




from django.core.exceptions import ValidationError
from django.conf import settings

from django.contrib.auth.models import AbstractUser, BaseUserManager



class Estado(models.Model):
    nombre_tabla = models.CharField(max_length=255, help_text="Nombre de la tabla a la que pertenece este estado")
    identificador_tabla = models.CharField(max_length=255, help_text="Identificador único del registro dentro de la tabla")
    descripcion = models.CharField(max_length=255)
    clave = models.CharField(max_length=255, help_text="Clave del estado")
    valor = models.CharField(help_text="Valor del estado")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('nombre_tabla', 'identificador_tabla', 'clave')
        indexes = [
            models.Index(fields=['nombre_tabla', 'identificador_tabla']),
        ]

    def __str__(self):
        return f"{self.nombre_tabla} ({self.identificador_tabla}): {self.clave} = {self.valor}"

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        
        email = self.normalize_email(email)
        # Verifica que el campo nombreusuario esté presente
        #if not nombreusuario:
        #    raise ValueError('El campo nombreusuario debe ser declarado')
        
        # Crea el usuario con el nombre de usuario y otros campos extra
        user = self.model( email = email, **extra_fields)
        
        # Establece la contraseña
        if password:
            user.set_password(password)
        
        # Guarda el usuario en la base de datos
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Establece is_staff y is_superuser para el superusuario
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('nombres', "superuser")

        # Llama a create_user para crear el superusuario
        return self.create_user( email, password, **extra_fields)

class CustomUser(AbstractUser):
    # Eliminar el campo `username` heredado
    username = None
    
    # Campos adicionales
    nombres = models.CharField(max_length=128)
    fechacreacion = models.DateTimeField(auto_now_add=True)
    apellidos = models.CharField(max_length=128, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fotoperfil = models.ImageField(upload_to='perfilUsuarioimagen/', blank=True, null=True)
    eliminado = models.BooleanField(default = 0)
    
    pais = models.CharField(max_length=128, blank=True, null=True)
    ciudad = models.CharField(max_length=128, blank=True, null=True)
    
    email = models.EmailField(unique=True) 
    email_verified_at = models.DateTimeField(blank=True, null=True)
    remember_token = models.CharField(max_length=100, blank=True, null=True)

    # Especificar que el campo para autenticar es `nombreusuario`
    USERNAME_FIELD = 'email'
    
    # Campos requeridos adicionales (no necesitas username ya que lo has reemplazado con nombreusuario)
    REQUIRED_FIELDS = ['nombres']  # En Django, `email` es un campo por defecto si lo estás usando como required

    # Manager personalizado
    objects = CustomUserManager()
    
    def __str__(self):
        return self.nombres
    def get_full_name(self):
        return f"{self.nombres} {self.apellidos or ''}".strip()

#-------------------------------------------------------------------------------------------------------------user

class Duenio(models.Model):
    idduenio = models.BigAutoField(primary_key=True)
    eliminado = models.SmallIntegerField(default = 0)
    # Campos adicionales
    nombres = models.CharField(max_length=128)
    apellidos = models.CharField(max_length=128, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fotoperfil = models.ImageField(upload_to='perfilDuenioimagen/', blank=True, null=True)
    email = models.EmailField(unique=True) 
    
    fechacreacion = models.DateTimeField(auto_now_add=True)
    estado = models.IntegerField()

    class Meta:
        db_table = 'Duenio'
        
        
        
class Fiesta(models.Model):
    eliminado = models.SmallIntegerField(default = 0)
    idfiesta = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=128)
    descripcion = models.TextField()
    fechainicio = models.DateField()
    fechafin = models.DateField()
    fechacreacion = models.DateTimeField(auto_now_add=True)

    estado = models.IntegerField()
 

    class Meta:
        db_table = 'Fiesta'
        
class Galpon(models.Model):
    idgalpon = models.BigAutoField(primary_key=True)
    idduenio = models.ForeignKey(Duenio, models.DO_NOTHING, db_column='idduenio')
    eliminado = models.SmallIntegerField(default = 0)
    # Campos adicionales
    titulo = models.CharField(max_length=128)
    descripcion = models.TextField()
    
    fechacreacion = models.DateTimeField(auto_now_add=True)
    estado = models.IntegerField()

    class Meta:
        db_table = 'Galpon'
        

#-------------------------------------------------------------------------------------------------------------user



class Carrusel(models.Model):
    eliminado = models.SmallIntegerField(default = 0)
    titulo = models.CharField(max_length=128)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='carrusel/', blank=True, null=True)
    fechacreacion = models.DateTimeField(auto_now_add=True)

    fechapublicacion = models.DateField()
    estado = models.IntegerField()
    idcarrusel = models.BigAutoField(primary_key=True)

    class Meta:
        db_table = 'Carrusel'


class Comentario(models.Model):
    eliminado = models.SmallIntegerField(default = 0)
    idusuario = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='idusuario')
    comentario = models.TextField()
    idcomentario = models.BigAutoField(primary_key=True)
    estado = models.IntegerField()
    fechacreacion = models.DateTimeField(auto_now_add=True)

    idstreaming = models.ForeignKey('Streaming', models.DO_NOTHING, db_column='idstreaming')

    class Meta:
        db_table = 'Comentario'


class Configuracion(models.Model):
    eliminado = models.SmallIntegerField(default = 0)
    idconf = models.BigAutoField(primary_key=True)
    nombreweb = models.CharField(max_length=128)
    correo = models.CharField(max_length=128)
    telefono = models.CharField(max_length=128, blank=True, null=True)
    estadostreaming = models.IntegerField(blank=True, null=True)
    urlinput = models.TextField( blank=True, null=True)
    urloutput = models.TextField( blank=True, null=True)
    fechacreacion = models.DateTimeField(auto_now_add=True)
    nombrecanal = models.CharField(max_length=128)

    class Meta:
        db_table = 'Configuracion'


class Evento(models.Model):
    eliminado = models.SmallIntegerField(default = 0)
    idevento = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=128)
    descripcion = models.TextField()
    fechaevento = models.DateField()
    fechacreacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='eventoflayer/', blank=True, null=True)
    idfiesta = models.ForeignKey(Fiesta, models.DO_NOTHING, db_column='idfiesta', related_name="eventos")

    estado = models.IntegerField()
 

    class Meta:
        db_table = 'Evento'


class Gallos(models.Model):
    eliminado = models.SmallIntegerField(default = 0)
    nombre = models.CharField(max_length=128)
    peso = models.FloatField(blank=True, null=True)
    color = models.CharField(max_length=128,blank=True, null=True)
    descripcion = models.TextField()
    experiencia = models.FloatField(default = 0)
    fechacreacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='gallofoto/', blank=True, null=True)
    idgallo = models.BigAutoField(primary_key=True)
    

    class Meta:
        db_table = 'Gallos'


class Streaming(models.Model):
    eliminado = models.SmallIntegerField(default = 0)
    idevento = models.ForeignKey(Evento, models.DO_NOTHING, db_column='idevento', blank=True, null=True)
    urlstreaming = models.TextField()
    nombrevideolife = models.TextField()
    idstreaming = models.BigAutoField(primary_key=True)

    class Meta:
        db_table = 'Streaming'



class ParticipacionGallos(models.Model):
    idparticipacion = models.BigAutoField(primary_key=True)
    eliminado = models.SmallIntegerField(default = 0)
    idgallo = models.ForeignKey(Gallos, models.DO_NOTHING, db_column='idgallo')
    idevento = models.ForeignKey(Evento, models.DO_NOTHING, db_column='idevento', related_name='evento_gallos_vs')

    class Meta:
        db_table = 'participacion_gallos'


class RegistroFiesta(models.Model):
    idregistro = models.BigAutoField(primary_key=True)
    eliminado = models.SmallIntegerField(default = 0)
    voucher = models.ImageField(upload_to='pagos/', blank=True, null=True)
    estado = models.IntegerField()
    idfiesta = models.ForeignKey(Fiesta, models.DO_NOTHING, db_column='idfiesta')
    idusuario = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='idusuario')

    class Meta:
        db_table = 'registro_fiesta'
        unique_together = (('idfiesta', 'idusuario'),)


class GalponGallos(models.Model):
    idparticipacion = models.BigAutoField(primary_key=True)
    eliminado = models.SmallIntegerField(default = 0)
    idgallo = models.ForeignKey(Gallos, models.DO_NOTHING, db_column='idgallo', related_name = 'gallo_galpondetalle')
    idgalpon = models.ForeignKey(Galpon, models.DO_NOTHING, db_column='idgalpon', related_name='galpon_gallos')

    class Meta:
        db_table = 'galpon_gallos'
        
class GalponFiesta(models.Model):
    idparticipacion = models.BigAutoField(primary_key=True)
    eliminado = models.SmallIntegerField(default = 0)
    idfiesta = models.ForeignKey(Fiesta, models.DO_NOTHING, db_column='idfiesta')
    idgalpon = models.ForeignKey(Galpon, models.DO_NOTHING, db_column='idgalpon')

    class Meta:
        db_table = 'galpon_fiesta'