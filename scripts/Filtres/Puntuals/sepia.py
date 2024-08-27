import cv2
import numpy as np


# Función para aplicar el filtro sepia recorriendo manualmente la matriz
def filtro_sepia_manual(imagen):
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


# Cargar la imagen
imagen = cv2.imread('tmp/Cubo05.png')

# Aplicar el filtro sepia
imagen_sepia = filtro_sepia_manual(imagen)

# Mostrar la imagen original y la imagen con filtro sepia
cv2.imshow('Imagen original', imagen)
cv2.imshow('Imagen con filtro sepia', imagen_sepia)
cv2.waitKey(0)
cv2.destroyAllWindows()
