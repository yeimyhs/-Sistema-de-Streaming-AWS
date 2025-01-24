# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remov` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Carrusel(models.Model):
    activo = models.SmallIntegerField(default = 1)
    titulo = models.CharField(max_length=128)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='carrusel/', blank=True, null=True)
    fechacreacion = models.DateField()
    fechapublicacion = models.DateField()
    estado = models.IntegerField()
    idcarrusel = models.BigIntegerField(primary_key=True)

    class Meta:
        db_table = 'Carrusel'


class Comentario(models.Model):
    activo = models.SmallIntegerField(default = 1)
    idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='idusuario')
    comentario = models.TextField()
    idcomentario = models.BigIntegerField(primary_key=True)
    estado = models.IntegerField()
    fechacreacion = models.DateField()
    idstreaming = models.ForeignKey('Streaming', models.DO_NOTHING, db_column='idstreaming')

    class Meta:
        db_table = 'Comentario'


class Configuracion(models.Model):
    activo = models.SmallIntegerField(default = 1)
    idconf = models.BigIntegerField(primary_key=True)
    nombreweb = models.CharField(max_length=128)
    correo = models.CharField(max_length=128)
    telefono = models.CharField(max_length=128, blank=True, null=True)
    estadostreaming = models.IntegerField(blank=True, null=True)
    urlinput = models.TextField( blank=True, null=True)
    urloutput = models.TextField( blank=True, null=True)
    nombrecanal = models.CharField(max_length=128)

    class Meta:
        db_table = 'Configuracion'


class Evento(models.Model):
    activo = models.SmallIntegerField(default = 1)
    idevento = models.BigIntegerField(primary_key=True)
    titulo = models.CharField(max_length=128)
    descripcion = models.TextField()
    fechaevento = models.DateField()
    fechacreacion = models.DateField()
    estado = models.IntegerField()
 

    class Meta:
        db_table = 'Evento'


class Gallos(models.Model):
    activo = models.SmallIntegerField(default = 1)
    nombre = models.BigIntegerField()
    duenio = models.BigIntegerField()
    peso = models.BigIntegerField(blank=True, null=True)
    color = models.BigIntegerField(blank=True, null=True)
    descripcion = models.BigIntegerField()
    experiencia = models.BigIntegerField(blank=True, null=True)
    fechacreacion = models.BigIntegerField()
    idgallo = models.BigIntegerField(primary_key=True)

    class Meta:
        db_table = 'Gallos'


class Streaming(models.Model):
    activo = models.SmallIntegerField(default = 1)
    idevento = models.ForeignKey(Evento, models.DO_NOTHING, db_column='idevento', blank=True, null=True)
    urlstreaming = models.TextField()
    nombrevideolife = models.TextField()
    idstreaming = models.BigIntegerField(primary_key=True)

    class Meta:
        db_table = 'Streaming'


class Usuario(models.Model):
    activo = models.SmallIntegerField(default = 1)
    idusuario = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=128)
    apellido = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    telefono = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'Usuario'


class ParticipacionGalllos(models.Model):
    activo = models.SmallIntegerField(default = 1)
    idgallo = models.OneToOneField(Gallos, models.DO_NOTHING, db_column='idgallo', primary_key=True)
    idevento = models.ForeignKey(Evento, models.DO_NOTHING, db_column='idevento')

    class Meta:
        db_table = 'participacion_galllos'
        unique_together = (('idgallo', 'idevento'),)


class RegistroEvento(models.Model):
    activo = models.SmallIntegerField(default = 1)
    voucher = models.BinaryField()
    estado = models.IntegerField()
    idevento = models.OneToOneField(Evento, models.DO_NOTHING, db_column='idevento', primary_key=True)
    idusuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='idusuario')

    class Meta:
        db_table = 'registro_evento'
        unique_together = (('idevento', 'idusuario'),)
