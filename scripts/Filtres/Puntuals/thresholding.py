import cv2
import numpy as np

# Función para aplicar el filtro de umbral (thresholding) recorriendo manualmente la matriz
def thresholding_manual(imagen, umbral):
    alto, ancho = imagen.shape
    imagen_umbralizada = np.zeros_like(imagen)

    # Recorrer la imagen
    for y in range(alto):
        for x in range(ancho):
            # Obtener el valor del píxel en la posición (x, y)
            valor_pixel = imagen[y, x]

            # Aplicar el umbral
            if valor_pixel > umbral:
                imagen_umbralizada[y, x] = 255  # Blanco
            else:
                imagen_umbralizada[y, x] = 0    # Negro

    return imagen_umbralizada

# Cargar la imagen en escala de grises
imagen = cv2.imread('tmp/Cubo05.png', cv2.IMREAD_GRAYSCALE)

# Definir el umbral de binarización
umbral = 127

# Aplicar el filtro de umbral
imagen_umbralizada = thresholding_manual(imagen, umbral)

# Mostrar la imagen original y la imagen umbralizada
cv2.imshow('Imagen original', imagen)
cv2.imshow('Imagen umbralizada', imagen_umbralizada)
cv2.waitKey(0)
cv2.destroyAllWindows()
