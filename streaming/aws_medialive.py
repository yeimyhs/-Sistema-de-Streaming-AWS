
import boto3
from django.conf import settings
import logging

# 🔧 CONFIGURACIÓN PERSONALIZABLE 🔧
AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
AWS_REGION = settings.AWS_REGION
AWS_MEDIALIVE_ROLE_ARN = settings.AWS_MEDIALIVE_ROLE_ARN
BUCKET_NAME = "streaming-gallos-bucket"  # Reemplaza con tu bucket de S3
CLOUDFRONT_DOMAIN = "d17y4wxxn3lf6q.cloudfront.net"  # Tu dominio de CloudFront
AWS_MEDIALIVE_SECURITY_GROUP = settings.AWS_MEDIALIVE_SECURITY_GROUP
# Inicializar cliente de MediaLive
client = boto3.client(
    "medialive",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)
# Configurar logging
logger = logging.getLogger(__name__)

def crear_canal_medialive(nombre_canal):
    try:
        # 1️⃣ Crear entrada en MediaLive (para OBS)
        input_response = client.create_input(
            Name="MiEntradaLive",
            Type="RTMP_PUSH",
            InputSecurityGroups=[AWS_MEDIALIVE_SECURITY_GROUP],  # Reemplazar con el ID correcto
            Destinations=[
                {"StreamName": f"{nombre_canal}"},
                {"StreamName": f"{nombre_canal}"}
            ]
        )

        input_id = input_response["Input"]["Id"]

        # Obtener las URLs de entrada RTMP (para OBS)
        input_destinations = input_response["Input"]["Destinations"]
        stream_urls = [dest.get("Url") for dest in input_destinations]

        logger.info(f"URLs de entrada RTMP: {stream_urls}")

        # 2️⃣ Crear canal en MediaLive con salida en S3
        channel_response = client.create_channel(
            Name=nombre_canal,
            RoleArn=AWS_MEDIALIVE_ROLE_ARN,
            InputAttachments=[
                {
                    "InputId": input_id,
                    "InputAttachmentName": "attachment1"
                }
            ],
            Destinations=[
                {
                    "Id": "destination1",
                    "Settings": [
                        {
                            "Url": f"s3://{BUCKET_NAME}/live-stream/{nombre_canal}/playlist"
                        },
                        {
                            "Url": f"s3://{BUCKET_NAME}/live-stream/{nombre_canal}/backup/playlist"
                        }
                    ]
                }
            ],
            EncoderSettings={
                "AudioDescriptions": [
                    {
                        "AudioSelectorName": "Default",
                        "CodecSettings": {
                            "AacSettings": {
                                "InputType": "NORMAL",
                                "Profile": "LC",
                                "RateControlMode": "CBR",
                                "SampleRate": 48000
                            }
                        },
                        "Name": "audio_1"
                    }
                ],
                "VideoDescriptions": [
                    {
                        "Height": 720,
                        "Width": 1280,
                        "CodecSettings": {
                            "H264Settings": {
                                "AdaptiveQuantization": "HIGH",
                                "Bitrate": 3000000,
                                "FramerateControl": "INITIALIZE_FROM_SOURCE",
                                "GopSize": 60,
                                "GopSizeUnits": "FRAMES",
                                "Profile": "HIGH",
                                "RateControlMode": "CBR"
                            }
                        },
                        "Name": "video_1"
                    }
                ],
                "OutputGroups": [
                    {
                        "Name": "HLS",
                        "OutputGroupSettings": {
                            "HlsGroupSettings": {
                                "Destination": {
                                    "DestinationRefId": "destination1"
                                },
                                "HlsCdnSettings": {
                                    "HlsBasicPutSettings": {}
                                },
                                "SegmentLength": 6
                            }
                        },
                        "Outputs": [
                            {
                                "AudioDescriptionNames": ["audio_1"],
                                "OutputName": "output_1",
                                "VideoDescriptionName": "video_1",
                                "OutputSettings": {
                                    "HlsOutputSettings": {
                                        "HlsSettings": {
                                            "StandardHlsSettings": {
                                                "M3u8Settings": {}
                                            }
                                        }
                                    }
                                }
                            }
                        ]
                    }
                ],
                "TimecodeConfig": {
                    "Source": "EMBEDDED"
                }
            }
        )
        hls_bk_stream_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/live-stream/{nombre_canal}/playlist.m3u8"

        # 3️⃣ Generar la URL de salida HLS desde CloudFront
        hls_stream_url = f"https://{CLOUDFRONT_DOMAIN}/live-stream/{nombre_canal}/playlist.m3u8"


        # 4️⃣ Devolver las URLs
        result = {
            "channel_info": channel_response,
            "stream_url": stream_urls,
            "channel_id": channel_response["Channel"]["Id"],
            "rtmp_input_urls": stream_urls,  # Para OBS
            "hls_output_url": hls_stream_url,  # Para ver la transmisión a través de CloudFront
            "hls_bk_stream_url": hls_bk_stream_url,  # Para ver la transmisión a través de CloudFront
        }

        return result

    except Exception as e:
        logger.error(f"Error al crear canal MediaLive: {str(e)}")
        raise e


def listar_canales_medialive():
    try:
        client = boto3.client(
            'medialive',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )

        response = client.list_channels()
        canales = response.get('Channels', [])

        resultado = []
        for canal in canales:
            resultado.append({
                'id': canal['Id'],
                'name': canal['Name'],
                'state': canal['State'],
                'inputAttachments': canal['InputAttachments'],
                'type': canal['ChannelClass']
            })

        return  resultado

    except Exception as e:
        logger.error(f"Error al listar canales MediaLive: {str(e)}")
        raise e
    
    



def iniciar_canal(canal_id):
    response = client.start_channel(ChannelId=canal_id)
    return client.describe_channel(ChannelId=canal_id)


def detener_canal(canal_id):
    response = client.stop_channel(ChannelId=canal_id)
    return client.describe_channel(ChannelId=canal_id)


def obtener_detalle_canal(canal_id):
    return client.describe_channel(ChannelId=canal_id)


def listar_canales():
    response = client.list_channels()
    return response.get('Channels', [])



# El nombre del bucket de S3
BUCKET_NAME = "streaming-gallos-bucket"  # Reemplaza con tu bucket de S3

# Función para obtener los detalles del canal
def obtener_detalle_canal(canal_id):
    return client.describe_channel(ChannelId=canal_id)

# Función para mover los archivos a una nueva ubicación en S3
def mover_grabacion_a_nueva_ubicacion(canal_id, nombre_canal, nombrestreming):
    # Fecha y hora actual para crear una carpeta única
    from datetime import datetime
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Definir la nueva ruta de grabación en S3
    nueva_ubicacion = f"live-recordings/{nombrestreming}_{current_time}/"

    # Obtener los objetos de grabación en el bucket
    # (Asumimos que los archivos están en la carpeta original 'live-stream')
    grabaciones_ruta_original = f"live-stream/{nombre_canal}/"
    try:
        # Listar objetos en la carpeta de grabaciones
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=grabaciones_ruta_original)
        archivos = response.get('Contents', [])

        # Mover cada archivo a la nueva ubicación
        for archivo in archivos:
            # Obtener el nombre del archivo
            archivo_key = archivo['Key']
            nueva_ruta = archivo_key.replace(grabaciones_ruta_original, nueva_ubicacion)

            # Copiar el archivo a la nueva ubicación
            s3_client.copy_object(
                Bucket=BUCKET_NAME,
                CopySource={'Bucket': BUCKET_NAME, 'Key': archivo_key},
                Key=nueva_ruta
            )

            # Eliminar el archivo original
            s3_client.delete_object(Bucket=BUCKET_NAME, Key=archivo_key)

        logger.info(f"Grabación movida a la nueva ubicación: {nueva_ubicacion}")
        return nueva_ubicacion
    except Exception as e:
        logger.error(f"Error al mover la grabación: {str(e)}")
        raise e

import time
def eliminar_todos_canales_y_entradas():
    try:
        # 1️⃣ Detener todos los canales
        canales = client.list_channels().get('Channels', [])
        for canal in canales:
            canal_id = canal['Id']
            estado = canal.get('State')
            if estado == 'RUNNING':
                client.stop_channel(ChannelId=canal_id)
                waiter = client.get_waiter('channel_stopped')
                waiter.wait(ChannelId=canal_id)

        # 2️⃣ Eliminar todos los canales
        for canal in canales:
            client.delete_channel(ChannelId=canal['Id'])

        # 🕒 Esperar unos segundos a que AWS libere las entradas
        time.sleep(10)

        # 3️⃣ Eliminar todas las entradas
        entradas = client.list_inputs().get('Inputs', [])
        for entrada in entradas:
            input_id = entrada['Id']
            try:
                client.delete_input(InputId=input_id)
                logger.info(f"Entrada {input_id} eliminada correctamente")
            except Exception as e:
                logger.warning(f"No se pudo eliminar entrada {input_id} (primer intento): {str(e)}")

        # 4️⃣ Reintentar después de esperar un poco más
        time.sleep(5)
        entradas_restantes = client.list_inputs().get('Inputs', [])
        for entrada in entradas_restantes:
            input_id = entrada['Id']
            try:
                client.delete_input(InputId=input_id)
                logger.info(f"Entrada {input_id} eliminada en segundo intento")
            except Exception as e:
                logger.error(f"No se pudo eliminar entrada {input_id} ni en segundo intento: {str(e)}")

        return True, "Todos los canales y entradas fueron eliminados (incluidos reintentos)"

    except Exception as e:
        logger.error(f"Error al eliminar recursos: {str(e)}")
        return False, str(e)