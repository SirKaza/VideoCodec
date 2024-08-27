import cv2
import time
import numpy as np
from numpy import ndarray
from tqdm.auto import tqdm

def main(filters_split, images, metadata, click, is_encoded, is_grayscale):
    """
    Processa les imatges segons el filtres especificat i els paràmetres proporcionats.

    Args:
        filters_split (list): Llista de Strings que contenen el nom del filtre i els seus paràmetres, si n'hi ha.
        images (dict): Diccionari que conté les imatges a processar.
        metadata (dict): Metadades del programa.
        click (mòdul): Mòdul Click per a la interacció amb l'usuari.
        is_encoded (bool): Indica si les imatges han estat codificades prèviament.
        is_grayscale (bool): Indica si les imatges són en escala de grisos.
    """
    filters_applied = []
    filters_not_compatible = ["sepia", "grey"]

    if is_encoded: # Si se ha codificado previamente, cogemos la información de los filtros aplicados
        filters_applied = [filter['filter_name'] for filter in metadata['filters']]

    for filter_str in filters_split:
        if '=' in filter_str:
            filter_name, filter_value = filter_str.split('=')
            if ',' in filter_value:
                filter_value = filter_value.split(',')
                filter_value = float(filter_value[0]), float(filter_value[1])
                filter_value = tuple(filter_value)
            elif filter_value.isdigit():
                filter_value = int(filter_value)
        else:
            filter_name, filter_value = filter_str, None

        if filter_name in filters_applied:
            click.echo(f'El filtre {filter_name} ja ha estat aplicat anteriorment.')
            continue
        if filter_name in filters_not_compatible and any(item in filters_applied for item in filters_not_compatible):
            click.echo(f'El filtre {filter_name} no és compatible amb els filtres aplicats anteriorment.')
            continue
        if is_grayscale and filter_name in filters_not_compatible:
            click.echo(f'El filtre {filter_name} no és compatible amb imatges en escala de grisos.')
            continue
        filter_func = {
            'binarization': binaritzar,
            'brillo': brillo_contraste,
            'negative': negative,
            'sepia': sepia,
            'grey': lambda img: cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),
            'averaging': averaging,
            'blur': blur,
            'edges': bordes,
            'embossing': embossing,
            'sharp': sharp,
        }.get(filter_name)

        if filter_func:
            # valors per defecte
            if filter_name == 'averaging':
                filter_value = 3
            elif filter_name == 'blur':
                filter_value = 3
            elif filter_name == 'binarization':
                filter_value = 128
            elif filter_name == 'brillo':
                filter_value = (50.0, 1.5)

            start_time = time.time()
            if filter_value:
                apply_filter_to_images(filter_func, images, filter_value)
                end_time = time.time()
                total_time = end_time - start_time
                click.echo(f'Aplicat filtre {filter_name} amb els paràmetres: {filter_value}. Temps total: {str(round(total_time))} segons.')
            else:
                apply_filter_to_images(filter_func, images)
                end_time = time.time()
                total_time = end_time - start_time
                click.echo(f'Aplicat filtre {filter_name}. Temps total: {str(round(total_time))} segons.')
            
            filters_applied.append(filter_name)
            metadata["filters"].append({"filter_name": filter_name, "parameters": filter_value})


def apply_filter_to_images(filter_func, images, *args:int or float or tuple or None):
    """
    Aplica una funció de filtre específica a cada imatge d'un diccionari d'imatges.

    Args:
        filter_func (funció): La funció de filtre a aplicar a les imatges.
        images (dict): Diccionari que conté les imatges a les quals s'aplicarà el filtre.
        *args: Arguments addicionals que es passaran a la funció de filtre.
    """
    for file_name, image_data in tqdm(images.items(), desc="Aplicant filtre"):
        images[file_name] = filter_func(image_data, *args)


def binaritzar(image, threshold) -> ndarray:
    """
    Aplica una binarització a una imatge a partir d'un valor de llindar específic.

    Args:
        image (numpy.ndarray): La imatge a binaritzar.
        threshold (int): El valor de llindar per a la binarització. Si no es proporciona, s'utilitza el valor predeterminat de 128.

    Returns:
        numpy.ndarray: La imatge binària resultant després d'aplicar la binarització.
    """
    if threshold == None:
        threshold = 128
    _, binary_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    return binary_image


def brillo_contraste(image, brillo_contraste) -> ndarray:
    """
    Ajusta el brillo y el contrast per a una imatge.

    Args:
        image (numpy.ndarray): La imatge d'entrada.
        brillo_contraste (tuple): Tupla que conté l'ajust de brillantor i contrast.
            El primer valor de la tupla és l'ajust de brillantor, on un valor major que 1 augmentarà el brillantor i un valor menor que 1 el disminuirà.
            El segon valor de la tupla és l'ajust de contrast, on un valor major que 1 augmentarà el contrast i un valor menor que 1 el disminuirà.

    Returns:
        numpy.ndarray: La imatge resultant després d'aplicar els ajustos de brillantor i contrast.
    """
    return cv2.convertScaleAbs(image, alpha=brillo_contraste[1], beta=brillo_contraste[0])


def negative(image) -> ndarray:
    """
    Crea una imatge negativa d'una imatge donada.

    Args:
        image (numpy.ndarray): La imatge d'entrada.

    Returns:
        numpy.ndarray: La imatge resultant que és la negativa de la imatge d'entrada.
    """
    return 255 - image


def sepia(image) -> ndarray:
    """
    Aplica un efecte sèpia a una imatge.

    Args:
        image (numpy.ndarray): La imatge d'entrada.

    Returns:
        numpy.ndarray: La imatge resultant amb l'efecte sèpia aplicat.
    """
    sepia_filter = np.array([[0.272, 0.534, 0.131],
                             [0.349, 0.686, 0.168],
                             [0.393, 0.769, 0.189]])
    return cv2.transform(image, sepia_filter)


def generate_averaging_kernel(size) -> ndarray:
    """
    Genera un kernel per al filtre de promig.

    Args:
        size (int): La mida del kernel.

    Returns:
        numpy.ndarray: El kernel generat per al filtre de promig.
    """
    kernel = np.ones((size, size), dtype=np.float32) / (size * size)
    return kernel


def generate_blur_kernel(size) -> ndarray:
    """
    Genera un kernel per al filtre de desenfocament gaussià.

    Args:
        size (int): La mida del kernel.

    Returns:
        numpy.ndarray: El kernel generat per al filtre de desenfocament gaussià.
    """
    if size % 2 == 0:
        raise ValueError("El tamaño del kernel debe ser impar.")
    sigma = 0.3 * ((size - 1) * 0.5 - 1) + 0.8
    kernel = cv2.getGaussianKernel(size, sigma)
    kernel = np.outer(kernel, kernel)
    return kernel


def averaging(image, kernel_size) -> ndarray:
    """
    Aplica un filtre de promig a una imatge.

    Args:
        image (numpy.ndarray): La imatge d'entrada.
        kernel_size (int): La mida del kernel per al filtre de promig. Si no es proporciona, s'utilitza un valor predeterminat de 3.

    Returns:
        numpy.ndarray: La imatge resultante després d'aplicar el filtre de promig.
    """
    if kernel_size is None:
        kernel_size = 3
    kernel = generate_averaging_kernel(kernel_size)
    channels = cv2.split(image)
    averaged_channels = [cv2.filter2D(channel, -1, kernel) for channel in channels]
    averaged_image = cv2.merge(averaged_channels)
    return averaged_image



def blur(image, kernel_size) -> ndarray:
    """
    Aplica un filtre de desenfocament gaussià a una imatge.

    Args:
        image (numpy.ndarray): La imatge d'entrada.
        kernel_size (int): La mida del kernel per al filtre de desenfocament. Si no es proporciona, s'utilitza un valor predeterminat de 3.

    Returns:
        numpy.ndarray: La imatge resultante després d'aplicar el filtre de desenfocament gaussià.
    """
    if kernel_size is None:
        kernel_size = 3
    kernel = generate_blur_kernel(kernel_size)
    channels = cv2.split(image)
    blurred_channels = [cv2.filter2D(channel, -1, kernel) for channel in channels]
    blurred_image = cv2.merge(blurred_channels)
    return blurred_image



def sharp(image) -> ndarray:
    """
    Aplica un filtre de millora a una imatge.

    Args:
        image (numpy.ndarray): La imatge d'entrada.

    Returns:
        numpy.ndarray: La imatge resultante després d'aplicar el filtre de millora.
    """
    kernel = np.array([[0, -1, 0],
                       [-1,  5, -1],
                       [0, -1, 0]], dtype=np.float32)
    return cv2.filter2D(image, -1, kernel)



def embossing(image) -> ndarray:
    """
    Aplica un filtre de relleu a una imatge.

    Args:
        image (numpy.ndarray): La imatge d'entrada.

    Returns:
        numpy.ndarray: La imatge resultant després d'aplicar el filtre de relleu.
    """
    kernel = np.array([[-1, -1, 0],
                       [-1,  0,  1],
                       [0,   1,  1]], dtype=np.float32)
    return cv2.filter2D(image, -1, kernel)



def bordes(image) -> ndarray:
    """
    Detecta contorns en una imatge utilitzant l'operador de Sobel.

    Args:
        image (numpy.ndarray): La imatge d'entrada.

    Returns:
        numpy.ndarray: La imatge resultant que mostra els contorns detectats.
    """
    sobel_kernel_x = np.array([[-1, 0, 1],
                               [-2, 0, 2],
                               [-1, 0, 1]], dtype=np.float32)
    sobel_kernel_y = np.array([[1,  2,  1],
                               [0,  0,  0],
                               [-1, -2, -1]], dtype=np.float32)
    sobelx = cv2.filter2D(image, cv2.CV_64F, sobel_kernel_x)
    sobely = cv2.filter2D(image, cv2.CV_64F, sobel_kernel_y)
    edges = cv2.magnitude(sobelx, sobely)
    edges = np.uint8(edges)
    return edges

