from pathlib import Path
from zipfile import ZipFile
import imageio.v2 as imageio  
import cv2
import json
from numpy import ndarray

is_grayscale = False

def open_zip(zip_path, images, metadata) -> tuple[bool, bool]:
    """
    Obre un fitxer ZIP especificat i carrega les imatges vàlides en un diccionari global.

    Args:
        zip_path (str): Ruta al fitxer ZIP que s'obrirà.
        images (dict): Diccionari on s'emmagatzemaran les imatges.
        metadata (dict): Diccionari on s'emmagatzemaran els metadades.

    Returns:
        tuple[bool, bool]: Tupla que indica si el fitxer ZIP conté imatges codificades i si conté imatges en escala de grisos.

    Raises:
        ValueError: Si el fitxer ZIP no conté arxius d'imatge vàlids o si no es pot obrir.
    """
    is_encoded = False  # El input es un archivo codificadoç
    is_grayscale = False  # El input es una imagen en escala de grises
    with ZipFile(zip_path, 'r') as zip_file:
        # Obtener la lista de nombres de archivos en el zip ordenada
        file_list = sorted(zip_file.namelist())

        # Iterar sobre cada archivo en el zip
        for file_name in file_list:
            # Verificar si el archivo es un JSON de metadatos del encoder
            if file_name == 'encoder_metadata.json':
                # Leer los metadatos del encoder
                with zip_file.open(file_name) as metadata_file:
                    metadata.update(json.load(metadata_file))
                is_encoded = True
                continue
            # Verificar si el archivo es una imagen (puedes agregar más extensiones si es necesario)
            if file_name.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                images[file_name] = read_image(file_name, zip_file)
                # Verificar si la imagen es en escala de grises
                if len(images[file_name].shape) == 2:
                    is_grayscale = True
            else:  # error?
                print(f'Error: {file_name} no es una imagen válida.')
    return is_encoded, is_grayscale


def read_image(file_name, zip_file) -> ndarray:
    """
    Llegeix una imatge des d'un fitxer dins d'un objecte ZipFile i la retorna com un array de dades.

    Args:
        file_name (str): Nom del fitxer dins del ZIP.
        zip_file (ZipFile): Objecte ZipFile ja obert des d'on es llegeix el fitxer.

    Returns:
        ndarray: Array de dades de la imatge llegida.

    Raises:
        IOError: Si el fitxer d'imatge no es pot llegir.
    """
    # Leer la imagen desde el archivo en el zip
    with zip_file.open(file_name) as image_file:
        # Utilizar imageio para leer la imagen
        image_data = imageio.imread(image_file)
        return image_data


def read_gif(file_name, images) -> bool:
    """
    Llegeix un fitxer GIF, guardant cada fotograma com una entrada separada en el diccionari global.

    Args:
        file_name (str): Nom del fitxer GIF.
        images (dict): Diccionari on s'emmagatzemaran les imatges.

    Returns:
        bool: True si el GIF és en escala de grisos, False altrament.
    """
    # Leer el archivo GIF utilizando imageio
    gif_images = imageio.mimread(file_name)
    # Ver si es formato de escala de grises
    is_grayscale = True if len(gif_images[0].shape) == 2 else False
    # Iterar sobre cada frame del GIF
    for i, image_data in enumerate(gif_images):
        file_name_without_extension = Path(file_name).stem
        # Agregar cada frame a la lista de imágenes
        images[f'{file_name_without_extension}_{i}.gif'] = image_data
    return is_grayscale


def read_video(file_path, images) -> bool:
    """
    Llegeix un fitxer de vídeo (AVI, MPEG o MP4) i guarda cada fotograma com una entrada separada en el diccionari global.

    Args:
        file_path (str): Ruta del fitxer de vídeo.
        images (dict): Diccionari on s'emmagatzemaran les imatges.
    
    Returns:
        bool: True si el vídeo és en escala de grisos, False altrament.
    """
    video_capture = cv2.VideoCapture(file_path)
    if not video_capture.isOpened():
        raise ValueError(f"Unable to open video file: {file_path}")

    is_grayscale = False
    frame_index = 0

    try:
        success, frame = video_capture.read()

        # Verify if the video is in grayscale
        if success and frame is not None:
            if len(frame.shape) == 2:
                is_grayscale = True

        while success and frame is not None:
            # If the video is in grayscale, save the frame without color conversion
            if is_grayscale:
                images[f'frame_{frame_index}.jpeg'] = frame
            else:
                # If the video is not in grayscale, convert to RGB before saving
                images[f'frame_{frame_index}.jpeg'] = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_index += 1
            success, frame = video_capture.read()

    finally:
        video_capture.release()

    return is_grayscale

    