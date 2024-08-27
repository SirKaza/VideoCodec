import zipfile
import io
import numpy as np
from PIL import Image
import cv2  # OpenCV per a la comparació de tessel·les


def load_images_from_zip(zip_path):
    images = []
    with zipfile.ZipFile(zip_path, 'r') as z:
        for file_name in sorted(z.namelist()):
            with z.open(file_name) as file:
                img = Image.open(file).convert('RGB')
                images.append(np.array(img))
    return images


def save_images_to_zip(images, info, zip_path):
    with zipfile.ZipFile(zip_path, 'w') as z:
        for i, img in enumerate(images):
            img_pil = Image.fromarray(img)
            img_bytes = io.BytesIO()
            img_pil.save(img_bytes, format='JPEG')
            z.writestr(f'image_{i:04d}.jpg', img_bytes.getvalue())
        info_bytes = io.BytesIO()
        info_bytes.write(info.encode())
        z.writestr('info.txt', info_bytes.getvalue())


def divide_into_tiles(image, n_tiles):
    tile_height, tile_width = image.shape[0] // n_tiles[0], image.shape[1] // n_tiles[1]
    tiles = []
    for y in range(0, image.shape[0], tile_height):
        for x in range(0, image.shape[1], tile_width):
            tiles.append(image[y:y + tile_height, x:x + tile_width])
    return tiles, tile_height, tile_width


def motion_compensation(images, n_tiles, seek_range, gop, quality):
    reference_frame = images[0]
    info = "Frame, Tile X, Tile Y, Replaced\n"

    for i in range(1, len(images)):
        current_frame = images[i]
        tiles, tile_height, tile_width = divide_into_tiles(current_frame, n_tiles)
        reference_tiles, _, _ = divide_into_tiles(reference_frame, n_tiles)

        for y in range(n_tiles[0]):
            for x in range(n_tiles[1]):
                current_tile = tiles[y * n_tiles[1] + x]
                ref_tile = reference_tiles[y * n_tiles[1] + x]

                # Correlació per trobar coincidències
                correlation = cv2.matchTemplate(ref_tile, current_tile, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(correlation)

                if max_val > quality:
                    images[i][y * tile_height:(y + 1) * tile_height, x * tile_width:(x + 1) * tile_width] = ref_tile
                    info += f"{i}, {x}, {y}, Yes\n"
                else:
                    info += f"{i}, {x}, {y}, No\n"

        if (i + 1) % gop == 0:
            reference_frame = images[i]

    return images, info


def main():
    input_zip = './data/raw/Cubo.zip'
    output_zip = './data/processed/processed_images.zip'
    n_tiles = (4, 4)  # Exemple de divisió en tessel·les
    seek_range = 5
    gop = 10
    quality = 0.90

    images = load_images_from_zip(input_zip)
    processed_images, info = motion_compensation(images, n_tiles, seek_range, gop, quality)
    save_images_to_zip(processed_images, info, output_zip)
    print("Compressió i codificació completades.")


if __name__ == "__main__":
    main()
