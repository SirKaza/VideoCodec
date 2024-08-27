import numpy as np
import multiprocessing
from numpy import ndarray
from tqdm.auto import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def main(images, ntiles, seekrange, gop, quality, metadata):
    """
    Processa les imatges per a la codificació, dividint-les en grups segons el GOP (Group of Pictures) 
    i aplicant els paràmetres especificats per a la codificació.

    Args:
        images (dict): Diccionari amb les imatges.
        ntiles (tuple): Nombre de teselles en els eixos vertical i horitzontal.
        seekrange (int): Desplaçament màxim en la cerca de teselles coincidents.
        gop (int): Mida del GOP.
        quality (float): Factor de qualitat per determinar la coincidència de teselles.
        metadata (dict): Diccionari per emmagatzemar la informació dels fotogrames i els paràmetres de codificació.
    """
    # Dividir las imágenes en grupos según el GOP
    image_groups = split_images_into_groups(images, gop)
    num_processors = multiprocessing.cpu_count()
    thread_limit = num_processors
    #thread_limit = num_processors // 2

    with tqdm(total=len(image_groups), desc="Processant grups d'imatges") as pbar:
        with ThreadPoolExecutor(max_workers=thread_limit) as executor:
            futures = []
            for index, image_group in enumerate(image_groups):
                future = executor.submit(process_image_group, image_group, ntiles, seekrange, quality, images, metadata, index)
                futures.append(future)
                
            for future in as_completed(futures):
                future.result()
                pbar.update(1)
    pbar.close()
    # Ordenar los metadatos por nombre de archivo
    metadata["frames"].sort(key=lambda x: x["file_name"])


def process_image_group(image_group, ntiles, seekrange, quality, images, metadata, group_index):
    """
    Processa un grup d'imatges, dividint-les en teselles i aplicant l'algorisme de correlació per a la codificació.

    Args:
        image_group (dict): Grup d'imatges a processar.
        ntiles (tuple): Nombre de teselles en els eixos vertical i horitzontal.
        seekrange (int): Desplaçament màxim en la cerca de teselles coincidents.
        quality (float): Factor de qualitat per determinar la coincidència de teselles.
        images (dict): Diccionari amb les imatges.
        metadata (dict): Diccionari per emmagatzemar la informació dels fotogrames i els paràmetres de codificació.
        group_index (int): Índex del grup d'imatges.
    """
    reference_image = None
    tiles_to_remove = {}

    for file_name, image in tqdm(image_group.items(), desc=f"Processant grup {group_index}", leave=False):
        height, width = image.shape[:2]
        tile_height = height // ntiles[1]
        tile_width = width // ntiles[0]
        tiles = subdivide_image_into_tiles(image, tile_height, tile_width, ntiles)

        if reference_image is not None:
            frame_info = {
                "file_name": file_name,
                "reference_frame": False,
                "tiles": []
            }

            for tile_index, current_tile in tqdm(tiles.items(), desc=f"Processant tessel·les del grup {group_index}", leave=False):
                for previous_index, previous_tile in reference_tiles.items():
                    # Aplicar el algoritmo de correlación
                    correlation_score, (dx, dy) = calculate_correlation(current_tile, previous_tile, seekrange)
                    # Comparar el resultado con el umbral de calidad
                    if correlation_score >= quality:
                        # Marcar la tesela para ser eliminada
                        mark_tile_for_removal(tiles_to_remove, tile_index, current_tile)
                        # Guardar la información de la tesela en el diccionario de metadatos
                        x = tile_index[1] * tile_width + dx
                        y = tile_index[0] * tile_height + dy
                        if x < 0:
                            x = 0
                        if y < 0:
                            y = 0
                        frame_info["tiles"].append({"tb_id": previous_index, "td_position": (x, y)})

            if tiles_to_remove:
                # Calcular el valor medio de la imagen
                average_value = calculate_average_value(image)
                # Procesar las teselas marcadas para eliminación
                tmp_tiles = tiles.copy()
                replace_tile_with_average(tmp_tiles, tiles_to_remove, average_value)
                tiles_to_remove.clear()
                # Reconstruir la imagen desde las teselas modificadas
                reconstructed_image = reconstruct_image_from_tiles(list(tmp_tiles.values()), ntiles, image.shape, tile_height, tile_width)
                # Actualizar la imagen original en el diccionario con la imagen reconstruida
                images[file_name] = reconstructed_image
        else:
            reference_image = image
            reference_tiles = tiles
            frame_info = {
                "file_name": file_name,
                "reference_frame": True
            }

        metadata["frames"].append(frame_info)


def split_images_into_groups(images, gop) -> list:
    """
    Divideix la llista d'imatges en conjunts consecutius segons el GOP (Grup de Fotogrames).

    Args:
        images (dict): Diccionari d'imatges.
        gop (int): Mida del GOP.

    Returns:
        list: Llista de diccionaris, on cada diccionari conté imatges consecutives de mida gop.
    """
    image_groups = []
    for i in range(0, len(images), gop):
        # Obtener el conjunto de claves (índices) de las imágenes consecutivas de tamaño gop
        group_keys = list(images.keys())[i:i+gop]
        
        # Crear un diccionario para almacenar las imágenes en este grupo
        group_images = {key: images[key] for key in group_keys}
        
        # Agregar este diccionario al grupo de imágenes
        image_groups.append(group_images)
    return image_groups


def subdivide_image_into_tiles(image, tile_height, tile_width, n_tiles) -> dict:
    """
    Subdivideix una imatge en el nombre especificat de teselles.

    Args:
        image (ndarray): Matriu de dades de la imatge.
        tile_height (int): Alçada de cada tesela.
        tile_width (int): Amplada de cada tesela.
        n_tiles (tuple): Nombre de teselas en els eixos vertical i horitzontal.

    Returns:
        dict: Diccionari on les claus són els índexos de les teselles i els valors són les subimatges (teselles).
    """
    tiles = {}
    for i in range(n_tiles[0]):
        for j in range(n_tiles[1]):
            tile = image[i*tile_height:(i+1)*tile_height, j*tile_width:(j+1)*tile_width]
            tiles[(i,j)] = tile
    return tiles


def calculate_correlation(current_tile, reference_tile, seekrange) -> tuple:
    """
    Calcula la correlació entre dues teselles d'imatges consecutives amb un desplaçament màxim especificat. Algoritme de correspondencia de tesela.

    Args:
        current_tile (ndarray): Tesela de la imatge actual.
        reference_tile (ndarray): Tesela de la imatge de referència.
        seekrange (int): Desplaçament màxim en la cerca de teselles coincidents.

    Returns:
        float: Valor de correlació màxima entre les dues teselles considerant el desplaçament.
        tuple: Posició de desplaçament de la tesela actual (dx, dy).
    """
    # Convertir las teselas a tipo de dato flotante
    current_tile = current_tile.astype(float)
    reference_tile = reference_tile.astype(float)

    max_correlation = -1  # Inicializar con un valor mínimo de correlación
    max_dx = 0  # Inicializar el desplazamiento horizontal máximo
    max_dy = 0  # Inicializar el desplazamiento vertical máximo

    # Recorrer todos los desplazamientos posibles dentro del rango especificado
    for dy in range(-seekrange, seekrange + 1):
        for dx in range(-seekrange, seekrange + 1):
            # Desplazar la tesela actual
            shifted_current_tile = np.roll(current_tile, shift=(dy, dx), axis=(0, 1))

            # Calcular la media de cada tesela
            mean_current = np.mean(shifted_current_tile)
            mean_reference = np.mean(reference_tile)

            # Calcular las diferencias respecto a la media para cada tesela
            diff_current = shifted_current_tile - mean_current
            diff_reference = reference_tile - mean_reference

            # Calcular la correlación entre las dos teselas
            numerator = np.sum(diff_current * diff_reference)
            denominator = np.sqrt(np.sum(diff_current ** 2) * np.sum(diff_reference ** 2))

            if denominator != 0 and not np.isnan(denominator):
                correlation = numerator / denominator
                if correlation > max_correlation:
                    max_correlation = correlation
                    max_dx = dx
                    max_dy = dy      

    return max_correlation, (max_dx, max_dy)


def mark_tile_for_removal(tiles_to_remove, tile_index, current_tile):
    """
    Marca una tesela per ser eliminada emmagatzemant el seu índex en un diccionari.

    Args:
        tiles_to_remove (dict): Diccionari que emmagatzema els índexs de les teselles a eliminar, indexats per la seva posició.
        tile_index (tuple): L'índex de la tesela dins de la seva imatge.
        current_tile (ndarray): La tesela actual.
    """
    if tile_index not in tiles_to_remove:
        tiles_to_remove[tile_index] = current_tile



def calculate_average_value(image) -> float:
    """
    Calcula el valor mitjà d'una imatge en escala de grisos o color.

    Args:
        image (ndarray): Una imatge com un array de numpy.

    Returns:
        float: El valor mitjà de la imatge.
    """
    # Convertir la imagen a un array de numpy
    img_array = np.array(image)

    # Si la imagen es en color (tres canales)
    if len(img_array.shape) == 3:
        # Calcular el valor medio para cada canal y luego el promedio de esos valores
        mean_value = img_array.mean(axis=(0, 1))
        return mean_value
    else:
        # Calcular el valor medio directamente para una imagen en escala de grises
        mean_value = img_array.mean()
        return mean_value


def replace_tile_with_average(tiles, tiles_to_remove, average_value):
    """
    Reemplaça les teselles marcades per eliminació pel seu valor mitjà.

    Args:
        tiles (dict): Diccionari de teselles.
        tiles_to_remove (dict): Diccionari que emmagatzema els índexs de les teselles a eliminar.
        average_value (float): El valor mitjà que s'utilitzarà per reemplaçar les teselles marcades.
    """
    for tile_index in tiles_to_remove.keys():
        if tile_index in tiles:
            tiles[tile_index] = np.full_like(tiles[tile_index], average_value)


def reconstruct_image_from_tiles(tiles, n_tiles, original_shape, tile_height, tile_width) -> ndarray:
    """
    Reconstrueix la imatge original a partir de les teselles.

    Args:
        tiles (dict): Diccionari de teselles.
        n_tiles (tuple): Nombre de teselles en els eixos vertical i horitzontal (n_tiles_y, n_tiles_x).
        original_shape (tuple): La forma original de la imatge (altura, amplada, canals).
        tile_height (int): Alçada de cada tesela.
        tile_width (int): Amplada de cada tesela.

    Returns:
        ndarray: La imatge reconstruïda com una matriu de numpy.
    """
    reconstructed_image = np.zeros(original_shape, dtype=tiles[0].dtype)
    
    count = 0
    for i in range(n_tiles[0]):
        for j in range(n_tiles[1]):
            reconstructed_image[i*tile_height:(i+1)*tile_height, j*tile_width:(j+1)*tile_width] = tiles[count]
            count += 1
    
    return reconstructed_image


def calculate_psnr(original_images, compressed_images) -> float:
    """
    Calcula el PSNR (Peak Signal-to-Noise Ratio) entre imatges originals i comprimides.

    Args:
        original_images (dict): Diccionari d'imatges originals.
        compressed_images (dict): Diccionari d'imatges comprimides.

    Returns:
        float: El valor mitjà de PSNR entre totes les imatges, o None si no es va poder calcular.
    """
    psnr_values = []
    for title, original_image in original_images.items():
        compressed_image = compressed_images[title]

        # Verificar si las imágenes tienen el mismo tamaño
        if original_image.shape != compressed_image.shape:
            print(f"Les dimensions de les imatges {title} són diferents.")
            continue

        # Calcular PSNR
        mse = np.mean((original_image - compressed_image) ** 2)
        if mse != 0:
            psnr = 10 * np.log10((255 ** 2) / mse)
            psnr_values.append(psnr)

    # Calcular PSNR promedio
    if psnr_values:
        avg_psnr = np.mean(psnr_values)
        return avg_psnr
    else:
        return None
    
    