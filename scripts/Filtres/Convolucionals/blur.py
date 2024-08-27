import cv2
import numpy as np

# Función para aplicar el filtro de desenfoque (blur) recorriendo manualmente la matriz
def filtro_blur_manual(imagen, tamaño_kernel):
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

# Cargar la imagen
imagen = cv2.imread('tmp/Cubo05.png')

# Aplicar el filtro de desenfoque con un tamaño de kernel de 3x3
imagen_desenfocada = filtro_blur_manual(imagen, 3)

# Mostrar la imagen original y la imagen desenfocada
cv2.imshow('Imagen original', imagen)
cv2.imshow('Imagen desenfocada', imagen_desenfocada)
cv2.waitKey(0)
cv2.destroyAllWindows()
