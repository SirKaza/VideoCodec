from tqdm.auto import tqdm
from tmproject import encoder

def main(images, metadata):
    """
    Descodifica els grups d'imatges a partir de la informació de les metadades.

    Args:
        images (dict): Diccionari amb les imatges.
        metadata (dict): Metadades del encoder que contenen els paràmetres i la informació dels frames.
    """
    # Obtener los parámetros necesarios del metadata
    gop_size = metadata["encoder_parameters"]["gop"]
    ntiles = (metadata["encoder_parameters"]["n_tiles_x"], metadata["encoder_parameters"]["n_tiles_y"])
    frames = metadata["frames"]

    # Dividir las imágenes en grupos según el GOP
    image_groups = encoder.split_images_into_groups(images, gop_size)

    # Inicializar la barra de progreso para los grupos de imágenes
    for image_group in tqdm(image_groups, desc="Descodificant grups d'imatges"):
        reference_image = None
        for file_name, image in image_group.items():
            # Obtener la información del frame actual
            frame = get_frame_by_file_name(frames, file_name)
            height, width = image.shape[:2]
            tile_height = height // ntiles[1]
            tile_width = width // ntiles[0]

            if frame["reference_frame"]:
                reference_image = images[file_name]
                ref_tiles = encoder.subdivide_image_into_tiles(reference_image, tile_height, tile_width, ntiles)
            else:
                for tile_info in frame["tiles"]:
                    # Obtener información de la tesela
                    tb_id = tuple(tile_info["tb_id"])
                    td_position = tile_info["td_position"]
                    x, y = td_position

                    # Calcular el tamaño de la tesela de referencia
                    ref_tile_height = tile_height if y + tile_height <= height else height - y
                    ref_tile_width = tile_width if x + tile_width <= width else width - x

                    # Obtener la tesela de referencia
                    reference_tile = ref_tiles[tb_id][:ref_tile_height, :ref_tile_width]
                    images[file_name][y:y+ref_tile_height, x:x+ref_tile_width] = reference_tile

def get_frame_by_file_name(frames, file_name) -> dict or None:
    """
    Obté la informació del fotograma corresponent al nom del fitxer donat.

    Args:
        frames (list): Llista de diccionaris que contenen la informació dels fotogrames.
        file_name (str): Nom del fitxer per buscar el fotograma corresponent.

    Returns:
        dict: Diccionari amb la informació del fotograma corresponent al nom del fitxer donat.
    """
    for frame in frames:
        if frame["file_name"] == file_name:
            return frame
    return None  # Si no se encuentra ningún marco con el nombre de archivo dado

