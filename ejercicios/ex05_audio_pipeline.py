"""
=============================================================================
Ejercicio 5: Pipeline de Audio - Polly + Transcribe (Python boto3)
Nivel: AUTONOMO
Duracion: ~20 minutos
=============================================================================

Objetivo: Construir un pipeline de audio completo que:

  1. Lea el titulo y texto de la primera noticia de data/noticias.json
  2. Use Amazon Polly (synthesize_speech) para generar un archivo MP3
     con la lectura del titulo
  3. Guarde el audio en data/output/noticia_audio.mp3
  4. (Bonus) Sube el MP3 a un bucket S3 y usa Amazon Transcribe
     (start_transcription_job) para transcribirlo de vuelta a texto

Servicios AWS:
  - Amazon Polly: Texto → Voz (TTS - Text to Speech)
  - Amazon Transcribe: Voz → Texto (STT - Speech to Text)

Parametros utiles de Polly:
  - VoiceId: 'Mia' (espanol mexicano), 'Lupe' (espanol US), 'Conchita' (espanol ES)
  - OutputFormat: 'mp3', 'ogg_vorbis', 'pcm'
  - Engine: 'neural' (mejor calidad) o 'standard'

Relacion con AIF-C01:
  - Task 1.2: Servicios de AI para procesamiento de voz
  - Polly y Transcribe son servicios complementarios (texto↔audio)
  - Concepto: pipeline de servicios AI encadenados

=============================================================================
"""
import boto3
import json
import os

# ============================================================
# 1. CARGA DE DATOS
# ============================================================
# Se abre el archivo JSON que contiene las noticias
# y se carga en memoria como una lista de diccionarios
with open('data/noticias.json', 'r', encoding='utf-8') as f:
    noticias = json.load(f)

# Se selecciona la primera noticia del arreglo
# y se extraen sus campos principales
titulo = noticias[0]['titulo']
texto = noticias[0]['texto']

# Se concatena el título y el cuerpo de la noticia
# para que Polly lea el contenido completo
contenido = f"{titulo}. {texto}"

# Se imprime el título como referencia en consola
print(f"Título: {titulo}")


# ============================================================
# 2. CONFIGURACIÓN DEL CLIENTE DE AMAZON POLLY
# ============================================================
# Se crea el cliente de Amazon Polly mediante boto3
# La región 'us-east-1' permite usar voces neuronales en español
polly = boto3.client('polly', region_name='us-east-1')


# ============================================================
# 3. GENERACIÓN DE AUDIO (TEXT TO SPEECH)
# ============================================================
# Se envía el texto a Polly para convertirlo en voz
# Parámetros clave:
# - Text: contenido a sintetizar
# - OutputFormat: formato de salida (mp3 en este caso)
# - VoiceId: voz seleccionada (Mia = español mexicano)
# - Engine: 'neural' mejora la naturalidad del audio
response = polly.synthesize_speech(
    Text=contenido,
    OutputFormat='mp3',
    VoiceId='Mia',
    Engine='neural'
)


# ============================================================
# 4. ALMACENAMIENTO DEL ARCHIVO DE AUDIO
# ============================================================
# Se define la ruta de salida del archivo MP3
output_path = 'data/output/noticia_audio.mp3'

# Se escribe el audio en modo binario ('wb')
# usando el stream devuelto por Polly
with open(output_path, 'wb') as f:
    f.write(response['AudioStream'].read())

# Confirmación en consola
print(f"Audio guardado en: {output_path}")

# BONUS
# ============================================================
# 5. CREAR BUCKET S3 (SI NO EXISTE)
# ============================================================
region = 'us-east-1'
bucket_name = 'bucket-lab-aif-c01-2026mx'  
file_name = 'noticia_audio.mp3'

s3 = boto3.client('s3', region_name=region)

try:
    s3.create_bucket(Bucket=bucket_name)
    print(f"Bucket creado: {bucket_name}")

except s3.exceptions.BucketAlreadyOwnedByYou:
    print("El bucket ya existe y es tuyo")

except s3.exceptions.BucketAlreadyExists:
    raise Exception("Ese nombre de bucket ya existe globalmente. Usa otro nombre.")


# ============================================================
# 6. SUBIR AUDIO A S3
# ============================================================

s3.upload_file(output_path, bucket_name, file_name)

print("Archivo subido a S3")


# ============================================================
# 7. INICIAR TRANSCRIPCIÓN
# ============================================================
transcribe = boto3.client('transcribe', region_name=region)

import time  # solo este import extra es necesario aquí

job_name = f"transcripcion-{int(time.time())}"
file_uri = f"s3://{bucket_name}/{file_name}"

transcribe.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={'MediaFileUri': file_uri},
    MediaFormat='mp3',
    LanguageCode='es-ES'
)

print(f"Transcripción iniciada: {job_name}")


# ============================================================
# 8. ESPERAR RESULTADO
# ============================================================
while True:
    status = transcribe.get_transcription_job(
        TranscriptionJobName=job_name
    )

    estado = status['TranscriptionJob']['TranscriptionJobStatus']

    if estado in ['COMPLETED', 'FAILED']:
        break

    print("Esperando transcripción...")
    time.sleep(5)


# ============================================================
# 9. GUARDAR TRANSCRIPCIÓN EN JSON
# ============================================================
if estado == 'COMPLETED':
    transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']

    import urllib.request  # import local para mantener tu estilo
    response = urllib.request.urlopen(transcript_uri)
    data = json.loads(response.read())

    os.makedirs('outputs', exist_ok=True)

    with open('outputs/transcripcion_audio.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("Transcripción guardada en outputs/transcripcion_audio.json")

else:
    print("La transcripción falló")

