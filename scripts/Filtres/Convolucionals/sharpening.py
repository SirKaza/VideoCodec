import cv2
import numpy as np


# Función para aplicar el filtro de afilado (sharpening) recorriendo manualmente la matriz
def filtro_afilado_manual(imagen):
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


# Cargar la imagen
imagen = cv2.imread('tmp/Cubo05.png')

# Aplicar el filtro de afilado
imagen_afilada = filtro_afilado_manual(imagen)

# Mostrar la imagen original y la imagen con filtro de afilado
cv2.imshow('Imagen original', imagen)
cv2.imshow('Imagen con filtro de afilado', imagen_afilada)
cv2.waitKey(0)
cv2.destroyAllWindows()
