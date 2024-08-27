import cv2

# Cargar la imagen
imagen = cv2.imread('tmp/Cubo05.png')

# Obtener las dimensiones de la imagen
alto, ancho, canales = imagen.shape

# Recorrer todos los píxeles de la imagen
for y in range(alto):
    for x in range(ancho):
        # Obtener el valor del píxel en la posición (x, y)
        pixel = imagen[y, x]

        # Aplicar alguna operación al valor del píxel
        # Por ejemplo, invertir el valor para obtener el negativo
        imagen[y, x] = 255 - pixel

# Mostrar la imagen resultante
cv2.imshow('Imagen con filtro negativo', imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()
