from pathlib import Path
from zipfile import ZipFile
from PIL import Image
import io
import json

def create_zip(output_path, images, metadata, is_encoded):
    """
    Crea un fitxer ZIP a la ruta especificada, guardant les imatges del diccionari global convertides a JPEG.

    Args:
        output_path (str): Ruta al fitxer ZIP de sortida.
        images (dict): Diccionari on les claus són noms d'arxiu i els valors són dades d'imatge.
        metadata (dict): Metadades associades a les imatges.
        is_encoded (bool): Indica si els noms dels arxius en els metadades ja estan codificats.
    """
    with ZipFile(output_path, 'w') as zip_file:
        for file_name, image_data in images.items():
            # Convertir la imagen a formato JPEG
            jpeg_image = image_to_jpeg(image_data)
            # Obtener el nombre del archivo sin la extensión
            file_name_without_extension = Path(file_name).stem
            # Guardar la imagen en el zip
            zip_file.writestr(f'{file_name_without_extension}.jpeg', jpeg_image)

        if not is_encoded:
            # Actualizar los nombres de archivo en los metadatos (.jpeg)
            updated_metadata = update_metadata_file_names(metadata)
            # Convertir los metadatos del encoder a formato JSON
            metadata_json = json.dumps(updated_metadata, indent=4)
            # Guardar el JSON de los metadatos en el zip
            zip_file.writestr('encoder_metadata.json', metadata_json)


def update_metadata_file_names(metadata) -> dict:
    """
    Actualitza els noms dels fitxers als metadades per reflectir l'extensió .jpeg.

    Args:
        metadata (dict): Metadades de l'encoder.

    Returns:
        dict: Metadades actualitzades amb els noms de fitxer modificats.
    """
    for frame in metadata['frames']:    
        file_name_without_extension = Path(frame['file_name']).stem
        frame['file_name'] = f'{file_name_without_extension}.jpeg'
    return metadata


def image_to_jpeg(image_data) -> bytes:
    """
    Converteix dades d'imatge en format d'array a format JPEG.

    Args:
        image_data (ndarray): Dades de la imatge a convertir.

    Returns:
        bytes: Dades de la imatge en format JPEG.
    """
    # Convertir la matriz de la imagen a un objeto BytesIO
    with io.BytesIO() as output_bytes:
        # Convertir la matriz de imagen a objeto de imagen PIL
        image_pil = Image.fromarray(image_data)
        # Verificar si la imagen tiene un canal alfa (RGBA)
        if image_pil.mode == 'RGBA':
            # Si tiene un canal alfa, convertirla a RGB
            image_pil = image_pil.convert('RGB')
        # Guardar la imagen PIL en formato JPEG en BytesIO
        image_pil.save(output_bytes, format='JPEG')
        # Obtener los bytes de la imagen JPEG
        jpeg_bytes = output_bytes.getvalue()
    return jpeg_bytes

