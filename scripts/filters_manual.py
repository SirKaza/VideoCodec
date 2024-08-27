import cv2
import numpy as np

def filtro_averaging_manual(imagen, tamaño_kernel):
    """
    Aplica un filtre de promig (averaging) a una imatge recorrent manualment la matriu.

    Args:
        imagen (numpy.ndarray): Imatge d'entrada com a un array de NumPy.
        tamaño_kernel (int): Mida del kernel (ha de ser un nombre senar).

    Returns:
        numpy.ndarray: Imatge resultant després d'aplicar el filtre de promig.
    """
    alto, ancho, canales = imagen.shape
    imagen_filtrada = np.zeros_like(imagen)

    # Definir el offset para la región del kernel
    offset = tamaño_kernel // 2

    # Recorrer la imagen
    for y in range(offset, alto - offset):
        for x in range(offset, ancho - offset):
            # Inicializar el valor promedio
            valor_promedio = np.zeros(canales, dtype=np.float32)

            # Recorrer la región del kernel
            for ky in range(-offset, offset + 1):
                for kx in range(-offset, offset + 1):
                    # Sumar los valores de los píxeles vecinos
                    valor_promedio += imagen[y + ky, x + kx]

            # Calcular el promedio dividiendo por el tamaño del kernel
            valor_promedio /= tamaño_kernel * tamaño_kernel

            # Asignar el valor promedio a la imagen filtrada
            imagen_filtrada[y, x] = valor_promedio

    return imagen_filtrada


def filtro_blur_manual(imagen, tamaño_kernel):
    """
    Aplica un filtre d'esborrament (blur) a una imatge recorrent manualment la matriu.

    Args:
        imagen (numpy.ndarray): Imatge d'entrada com a un array de NumPy.
        tamaño_kernel (int): Mida del kernel per a l'esborrament.

    Returns:
        numpy.ndarray: Imatge resultant després d'aplicar el filtre d'esborrament.
    """
    alto, ancho, _ = imagen.shape
    imagen_filtrada = np.zeros_like(imagen)

    # Definir el offset para la región del kernel
    offset = tamaño_kernel // 2

    # Recorrer la imagen
    for y in range(offset, alto - offset):
        for x in range(offset, ancho - offset):
            # Calcular el promedio de los valores de píxeles en la región del kernel
            promedio = np.mean(imagen[y-offset:y+offset+1, x-offset:x+offset+1], axis=(0, 1))
            imagen_filtrada[y, x] = promedio

    return imagen_filtrada


def filtro_bordes_manual(imagen):
    """
    Aplica un filtre de detecció de contorns utilitzant el mètode de Sobel.

    Args:
        imagen (numpy.ndarray): Imatge d'entrada en escala de grisos o en color.

    Returns:
        numpy.ndarray: Imatge resultant que mostra els contorns detectats.
    """
    # Convertir la imagen a escala de grises si es necesario
    if len(imagen.shape) > 2:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    alto, ancho = imagen.shape
    imagen_bordes = np.zeros_like(imagen, dtype=np.float32)

    # Definir el kernel de Sobel en las direcciones x e y
    kernel_x = np.array([[-1, 0, 1],
                         [-2, 0, 2],
                         [-1, 0, 1]])
    kernel_y = np.array([[-1, -2, -1],
                         [ 0,  0,  0],
                         [ 1,  2,  1]])

    # Recorrer la imagen
    for y in range(1, alto - 1):
        for x in range(1, ancho - 1):
            # Calcular el gradiente en las direcciones x e y utilizando el kernel de Sobel
            gradiente_x = np.sum(imagen[y-1:y+2, x-1:x+2] * kernel_x)
            gradiente_y = np.sum(imagen[y-1:y+2, x-1:x+2] * kernel_y)

            # Calcular la magnitud del gradiente
            magnitud_gradiente = np.sqrt(gradiente_x**2 + gradiente_y**2)

            # Asignar la magnitud del gradiente a la imagen de bordes
            imagen_bordes[y, x] = magnitud_gradiente

    return imagen_bordes


def filtro_embossing_manual(imagen):
    """
    Aplica un filtre d'embossat a una imatge recorrent manualment la matriu.

    Args:
        imagen (numpy.ndarray): Imatge d'entrada com a un array de NumPy.

    Returns:
        numpy.ndarray: Imatge resultant després d'aplicar el filtre d'embossat.
    """
    # Obtener las dimensiones de la imagen
    alto, ancho, _ = imagen.shape

    # Crear una imagen para almacenar el resultado
    imagen_embossing = np.zeros_like(imagen)

    # Definir el kernel de embossing
    kernel_embossing = np.array([[0, -1, -1],
                                  [1,  0, -1],
                                  [1,  1,  0]])

    # Recorrer la imagen y aplicar el filtro de embossing
    for y in range(1, alto - 1):
        for x in range(1, ancho - 1):
            for c in range(3):
                valor = 0
                for i in range(3):
                    for j in range(3):
                        valor += imagen[y+i-1, x+j-1, c] * kernel_embossing[i, j]
                imagen_embossing[y, x, c] = np.clip(valor, 0, 255)

    return imagen_embossing.astype(np.uint8)


def filtro_afilado_manual(imagen):
    """
    Aplica un filtre d'afinat a una imatge utilitzant un kernel específic.

    Args:
        imagen (numpy.ndarray): Imatge d'entrada com a un array de NumPy.

    Returns:
        numpy.ndarray: Imatge resultant després d'aplicar el filtre d'afinat.
    """
    # Obtener las dimensiones de la imagen
    alto, ancho, _ = imagen.shape

    # Crear una imagen para almacenar el resultado
    imagen_afilada = np.zeros_like(imagen)

    # Definir el kernel de afilado
    kernel = np.array([[-1, -1, -1],
                       [-1, 9, -1],
                       [-1, -1, -1]])

    # Recorrer la imagen y aplicar el filtro de afilado
    for y in range(1, alto - 1):
        for x in range(1, ancho - 1):
            # Aplicar la convolución con el kernel en el vecindario del píxel
            valor = np.sum(imagen[y - 1:y + 2, x - 1:x + 2] * kernel)

            # Asegurarse de que el valor esté dentro del rango [0, 255]
            valor = np.clip(valor, 0, 255)

            # Asignar el valor resultante al píxel correspondiente en la imagen de salida
            imagen_afilada[y, x] = valor

    return imagen_afilada.astype(np.uint8)


def binarizar_manual(imagen, umbral):
    """
    Aplica una binarització manual a una imatge basada en un llindar.

    Args:
        imagen (numpy.ndarray): Imatge d'entrada en escala de grisos.
        umbral (int): Valor del llindar per a la binarització.

    Returns:
        numpy.ndarray: Imatge binaritzada resultant.
    """
    alto, ancho = imagen.shape
    imagen_binarizada = np.zeros_like(imagen)

    # Recorrer la imagen
    for y in range(alto):
        for x in range(ancho):
            # Obtener el valor del píxel en la posición (x, y)
            valor_pixel = imagen[y, x]

            # Aplicar la binarización
            if valor_pixel > umbral:
                imagen_binarizada[y, x] = 255  # Blanco
            else:
                imagen_binarizada[y, x] = 0    # Negro

    return imagen_binarizada


def filtro_brillo_contraste_manual(imagen, brillo, contraste):
    """
    Ajusta el brillantor i el contrast d'una imatge de forma manual.

    Args:
        imagen (numpy.ndarray): Imatge d'entrada en escala de grisos o en color.
        brillo (int): Valor per ajustar el brillantor.
        contraste (float): Factor d'ajust del contrast.

    Returns:
        numpy.ndarray: Imatge resultant amb el brillantor i contrast ajustats.
    """
    # Convertir la imagen a escala de grises si es a color
    if len(imagen.shape) > 2:
        imagen_grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    else:
        imagen_grises = imagen.copy()

    # Obtener las dimensiones de la imagen
    alto, ancho = imagen_grises.shape

    # Crear una imagen para almacenar el resultado
    imagen_resultado = np.zeros_like(imagen_grises)

    # Recorrer la imagen y aplicar el ajuste de brillo y contraste
    for y in range(alto):
        for x in range(ancho):
            # Aplicar el ajuste de contraste
            pixel = imagen_grises[y, x]
            pixel_con_contraste = np.clip(contraste * (pixel - 128) + 128, 0, 255)

            # Aplicar el ajuste de brillo
            pixel_con_brillo = np.clip(pixel_con_contraste + brillo, 0, 255)

            # Asignar el valor del píxel al resultado
            imagen_resultado[y, x] = pixel_con_brillo

    # Convertir la imagen de nuevo a color si es necesario
    if len(imagen.shape) > 2:
        imagen_resultado = cv2.cvtColor(imagen_resultado, cv2.COLOR_GRAY2BGR)

    return imagen_resultado


def filtro_sepia_manual(imagen):
    """
    Aplica un filtre sepia a una imatge recorrent manualment la matriu.

    Args:
        imagen (numpy.ndarray): Imatge d'entrada com a un array de NumPy.

    Returns:
        numpy.ndarray: Imatge resultant després d'aplicar el filtre sepia.
    """
    # Obtener las dimensiones de la imagen
    alto, ancho, canales = imagen.shape

    # Crear una imagen para almacenar el resultado
    imagen_sepia = np.zeros_like(imagen, dtype=np.float32)

    # Definir los valores de la matriz de transformación
    matriz_transformacion = np.array([[0.393, 0.769, 0.189],
                                      [0.349, 0.686, 0.168],
                                      [0.272, 0.534, 0.131]])

    # Recorrer la imagen y aplicar el filtro sepia
    for y in range(alto):
        for x in range(ancho):
            pixel = imagen[y, x]

            # Aplicar la matriz de transformación al pixel
            pixel_sepia = matriz_transformacion.dot(pixel)

            # Asegurarse de que los valores estén dentro del rango [0, 255]
            pixel_sepia = np.clip(pixel_sepia, 0, 255)

            # Asignar el pixel transformado a la imagen de salida
            imagen_sepia[y, x] = pixel_sepia

    return imagen_sepia.astype(np.uint8)