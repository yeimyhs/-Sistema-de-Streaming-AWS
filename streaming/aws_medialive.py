import boto3
from django.conf import settings
import logging

# 🔧 CONFIGURACIÓN PERSONALIZABLE 🔧
AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
AWS_REGION = settings.AWS_REGION
AWS_MEDIALIVE_ROLE_ARN = settings.AWS_MEDIALIVE_ROLE_ARN
BUCKET_NAME = "streaming-gallos-bucket"  # Reemplaza con tu bucket de S3

# Inicializar cliente de MediaLive
client = boto3.client(
    "medialive",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

# Configurar logging
logger = logging.getLogger(__name__)

def crear_canal_medialive():
    try:
        # 1️⃣ Crear entrada en MediaLive (para OBS)
        input_response = client.create_input(
            Name="MiEntradaLive",
            Type="RTMP_PUSH",
            InputSecurityGroups=["3471356"],  # Reemplazar con el ID correcto
            Destinations=[
                {"StreamName": "stream1"},
                {"StreamName": "stream2"}
            ]
        )

        input_id = input_response["Input"]["Id"]

        # Obtener las URLs de entrada RTMP (para OBS)
        input_destinations = input_response["Input"]["Destinations"]
        stream_urls = [dest.get("Url") for dest in input_destinations]

        logger.info(f"URLs de entrada RTMP: {stream_urls}")

        # 2️⃣ Crear canal en MediaLive con salida en S3
        channel_response = client.create_channel(
            Name="MiCanalLive",
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
                            "Url": f"s3://{BUCKET_NAME}/live-stream/primary/playlist"
                        },
                        {
                            "Url": f"s3://{BUCKET_NAME}/live-stream/backup/playlist"
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

        # 3️⃣ Generar la URL de salida HLS directamente desde S3
        hls_stream_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/live-stream/primary/playlist.m3u8"

        # 4️⃣ Devolver las URLs
        result = {
            "channel_info": channel_response,
            "stream_url": stream_urls,
            "channel_id": channel_response["Channel"]["Id"],
            "rtmp_input_urls": stream_urls,  # Para OBS
            "hls_output_url": hls_stream_url  # Para ver la transmisión en S3
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
    
    


def get_medialive_client():
    return boto3.client(
        'medialive',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )
    
    

def iniciar_canal(canal_id):
    client = get_medialive_client()
    response = client.start_channel(ChannelId=canal_id)
    return client.describe_channel(ChannelId=canal_id)


def detener_canal(canal_id):
    client = get_medialive_client()
    response = client.stop_channel(ChannelId=canal_id)
    return client.describe_channel(ChannelId=canal_id)


def obtener_detalle_canal(canal_id):
    client = get_medialive_client()
    return client.describe_channel(ChannelId=canal_id)


def listar_canales():
    client = get_medialive_client()
    response = client.list_channels()
    return response.get('Channels', [])