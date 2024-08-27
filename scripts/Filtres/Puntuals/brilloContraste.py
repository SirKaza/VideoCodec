import cv2
import numpy as np

# Función para aplicar el filtro de brillo y contraste recorriendo manualmente la matriz
def filtro_brillo_contraste_manual(imagen, brillo, contraste):
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

# Cargar la imagen
imagen = cv2.imread('tmp/Cubo05.png')

# Ajustar el brillo y el contraste
brillo = 50  # Ajuste del brillo (positivo o negativo)
contraste = 1.5  # Ajuste del contraste (>1 para aumentar, <1 para disminuir)

# Aplicar el filtro de brillo y contraste
imagen_brillo_contraste = filtro_brillo_contraste_manual(imagen, brillo, contraste)

# Mostrar la imagen original y la imagen con brillo y contraste ajustados
cv2.imshow('Imagen original', imagen)
cv2.imshow('Imagen con brillo y contraste ajustados', imagen_brillo_contraste)
cv2.waitKey(0)
cv2.destroyAllWindows()
