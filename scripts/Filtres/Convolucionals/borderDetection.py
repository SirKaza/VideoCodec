import cv2
import numpy as np

# Función para aplicar el filtro de detección de bordes recorriendo manualmente la matriz
def filtro_bordes_manual(imagen):
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

# Cargar la imagen
imagen = cv2.imread('tmp/Cubo05.png')

# Aplicar el filtro de detección de bordes
imagen_bordes = filtro_bordes_manual(imagen)

# Normalizar la imagen resultante para mostrarla correctamente
imagen_bordes_normalizada = cv2.normalize(imagen_bordes, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

# Mostrar la imagen original y la imagen con bordes resaltados
cv2.imshow('Imagen original', imagen)
cv2.imshow('Imagen con bordes resaltados', imagen_bordes_normalizada)
cv2.waitKey(0)
cv2.destroyAllWindows()