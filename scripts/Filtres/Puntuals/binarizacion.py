import cv2
import numpy as np

# Función para aplicar la binarización recorriendo manualmente la matriz
def binarizar_manual(imagen, umbral):
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

# Cargar la imagen en escala de grises
imagen_grises = cv2.imread('tmp/Cubo05.png', cv2.IMREAD_GRAYSCALE)

# Definir el umbral de binarización
umbral = 127

# Aplicar la binarización
imagen_binarizada = binarizar_manual(imagen_grises, umbral)

# Mostrar la imagen original y la imagen binarizada
cv2.imshow('Imagen original', imagen_grises)
cv2.imshow('Imagen binarizada', imagen_binarizada)
cv2.waitKey(0)
cv2.destroyAllWindows()