import cv2
import numpy as np

# Función para aplicar el filtro de promedio (averaging) recorriendo manualmente la matriz
def filtro_averaging_manual(imagen, tamaño_kernel):
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

# Cargar la imagen
imagen = cv2.imread('tmp/Cubo05.png')

# Convertir la imagen a punto flotante para evitar desbordamientos
imagen = imagen.astype(np.float32)

# Aplicar el filtro de promedio con un tamaño de kernel de 3x3
imagen_filtrada = filtro_averaging_manual(imagen, 3)

# Convertir la imagen filtrada de nuevo a tipo de datos uint8 para mostrarla
imagen_filtrada = np.clip(imagen_filtrada, 0, 255).astype(np.uint8)

# Mostrar la imagen original y la imagen filtrada
cv2.imshow('Imagen original', imagen.astype(np.uint8))
cv2.imshow('Imagen filtrada', imagen_filtrada)
cv2.waitKey(0)
cv2.destroyAllWindows()
