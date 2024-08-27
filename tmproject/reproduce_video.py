from threading import Thread
import cv2
from tqdm.auto import tqdm

stop_video = False # Bandera para detener la reproducción del video
def show_video(fps, images):
    """
    Inicia un fil per reproduir les imatges emmagatzemades com a vídeo a una velocitat de fps especificada.

    Args:
        fps (int): Fotogrames per segon als quals es reproduirà el vídeo.
        images (dict): Diccionari que conté les imatges del vídeo.
    """
    pbar = tqdm(total=len(images), desc="Reproduciendo video", unit="frames")
    thread = Thread(target=play_video, args=(fps, images, pbar))
    thread.start()


def play_video(fps, images, pbar):
    """
    Reprodueix les imatges emmagatzemades en el diccionari global com a vídeo, en una finestra de OpenCV.

    Args:
        fps (int): Fotogrames per segon als quals es reproduirà el vídeo.
        images (dict): Diccionari que conté les imatges del vídeo.
        pbar (tqdm): Barra de progrés per mostrar el progrés de la reproducció.
    """
    global stop_video
    window_name = 'Video'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    #cv2.resizeWindow(window_name, 800, 600)

    while not stop_video:
        for file_name, image_data in images.items():
            image_cv2_rgb = cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)  # Convertir de BGR a RGB
            cv2.imshow(window_name, image_cv2_rgb)
            key = cv2.waitKey(int(1000 / fps))  # Convertir fps a milisegundos
            if key == ord('q'):
                stop_video = True
                break
            pbar.update() 
        pbar.reset()
    pbar.close()
    cv2.destroyWindow(window_name)

