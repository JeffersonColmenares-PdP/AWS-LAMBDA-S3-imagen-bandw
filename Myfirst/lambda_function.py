import json
import boto3#libreria para acceso a S3
import os
from PIL import Image#libreria para manipular la imagen
import io

s3 = boto3.client('s3')#para comunicarse con S3

def lambda_handler(event, context):
    print(event)
    # Obtener detalles del evento
    bucket_name = event['Records'][0]['s3']['bucket']['name']#nombre del bucket
    object_key = event['Records'][0]['s3']['object']['key']#ruta completa del archivo

    #Descargar la imagen desde S3
    image_object = s3.get_object(Bucket=bucket_name, Key=object_key)#busca imagen en bucket
    print(image_object)
    image_content = image_object['Body'].read()#lee la imagen

    # Convertir la imagen a blanco y negro
    image = Image.open(io.BytesIO(image_content)).convert('L')

    # Guardar la imagen convertida en un buffer
    buffer = io.BytesIO()# crea el buffer
    image.save(buffer, 'JPEG') # guarda la imagen en el buffer
    buffer.seek(0)#situa el cursor de R W al inicio del buffer

    # Definir un nuevo nombre para el archivo
    new_object_key = f"bandw{os.path.basename(object_key)}"#bandw + nombre original del archivo

    # Subir la nueva imagen a S3
    s3.put_object(Bucket=bucket_name, Key=new_object_key, Body=buffer, ContentType='image/jpeg')

    return {
        'statusCode': 200,
        'body': f"imagen {object_key} convertida a bandw guardado como {new_object_key}"
    }