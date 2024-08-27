import cv2
import numpy as np

# Función para aplicar el filtro de embossing recorriendo manualmente la matriz
def filtro_embossing_manual(imagen):
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

# Cargar la imagen
imagen = cv2.imread('tmp/Cubo05.png')

# Aplicar el filtro de embossing
imagen_embossing_manual = filtro_embossing_manual(imagen)

# Mostrar la imagen original y la imagen con el filtro de embossing aplicado manualmente
cv2.imshow('Imagen original', imagen)
cv2.imshow('Imagen con filtro de embossing manual', imagen_embossing_manual)
cv2.waitKey(0)
cv2.destroyAllWindows()
