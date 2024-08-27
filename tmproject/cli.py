import os
import time
import click
from tmproject import read_input
from tmproject import filters
from tmproject import reproduce_video
from tmproject import create_output
from tmproject import encoder
from tmproject import decoder

FILTER_HELP = """
Filtres disponibles i els seus paràmetres:
  binarization=<umbral>: Aplica una binarització amb el valor llindar especificat.
  brillo=<valor1>,<valor2>: Aplica un ajust de brillantor i contrast, on <valor1> és la brillantor i <valor2> el contrast.
  negative: Aplica un filtre negatiu a la imatge.
  sepia: Aplica un filtre de sepia a la imatge.
  grey: Converteix la imatge a escala de grisos.
  averaging<mida_kernel>: Aplica un filtre convolucional de mitjana amb tamany <mida_kernel> x <mida_kernel>.
  blur<mida_kernel>: Aplica un filtre convolucional de desenfocament amb tamany <mida_kernel> x <mida_kernel>.
  edges: Aplica un filtre convolucional de detecció de vores.
  embossing: Aplica un filtre convolucional d'estampació.
  sharp: Aplica un filtre convolucional d'afinat.
"""


@click.command()
@click.option('-i', '--input', required=True, help='Fitxer d’entrada.')
@click.option('-o', '--output', help='Fitxer de sortida.')
@click.option('--fps', type=int, default=25, help='Nombre d’imatges per segon amb les quals és reproduirà el vídeo.')
@click.option('--filter', help='Aplica filtres acumulatius amb sintaxi "filtre=valor".')
@click.option('--filter-help', is_flag=True, help='Mostra informació sobre els filtres disponibles.')
@click.option('--nTiles', type=(int, int), default=(4, 4), help='Nombre de tessel·les en els eixos vertical i horitzontal en les quals dividir la imatge.')
@click.option('--seekRange', type=int, default=0, help='Desplaçament màxim en la cerca de tessel·les coincidents.')
@click.option('--GOP', type=int, default=10, help='Nombre d’imatges entre dos frames de referència.')
@click.option('--quality', type=float, default=0.9, help='Factor de qualitat que determinarà quan dues tessel·les es consideren coincidents.')
@click.option('--reproduce', is_flag=True, help='Reprodueix el vídeo de sortida. Encara que hi hagi un fitxer de sortida.')
@click.help_option('--help', '-h')
def main(input, output, fps, filter, filter_help, ntiles, seekrange, gop, quality, reproduce):
    """
    Processa un fitxer de vídeo, aplicant codificació/descodificació i filtres especificats, i genera un fitxer ZIP amb el resultat.

    Args:
        input (str): Ruta al fitxer d'entrada. 
        output (str): Ruta al fitxer de sortida. 
        fps (int): Nombre d'imatges per segon per a la reproducció del vídeo.
        filter (str): Filtres a aplicar amb la sintaxi "filtre=valor".
        filter_help (bool): Indica si es mostra informació sobre els filtres disponibles.
        ntiles (tuple): Nombre de tessel·les en els eixos vertical i horitzontal.
        seekrange (int): Desplaçament màxim en la cerca de tessel·les coincidents.
        gop (int): Nombre d'imatges entre dos frames de referència.
        quality (float): Factor de qualitat per determinar quan dues tessel·les es consideren coincidents.
        reproduce (bool): Indica si es reprodueix el vídeo de sortida. Encara que hi hagi un fitxer de sortida.
    """
    if filter_help:
        click.echo(FILTER_HELP)
        return
    
    images = {}  # Diccionari per emmagatzemar les imatges
    metadata = {}  # Metadades de l'encoder
    is_encoded = False
    is_grayscale = False

    metadata = {
        "encoder_parameters": {
            "n_tiles_x": ntiles[0],
            "n_tiles_y": ntiles[1],
            "gop": gop,
            "quality": quality,
            "seek_range": seekrange
        },
        "frames": [],
        "filters": []
    }
    
    if input.endswith('.zip'):
        click.echo('Obrint fitxer zip...')
        is_encoded, is_grayscale = read_input.open_zip(input, images, metadata)
    elif input.endswith('.gif'):
        click.echo('Obrint fitxer GIF...')
        is_grayscale = read_input.read_gif(input, images)
    elif input.endswith(('.avi', '.mpeg', '.mp4')):
        click.echo('Obrint fitxer de vídeo...')
        is_grayscale = read_input.read_video(input, images)
    else:
        click.echo('Format d’entrada no vàlid. Només s’accepten fitxers de vídeo (AVI, MPEG o MP4) o fitxers ZIP.')
        return

    if is_encoded:
        start_time = time.time() 
        click.echo('Executant descodificació...')
        decoder.main(images, metadata)
        end_time = time.time()
        total_time = end_time - start_time
        click.echo("Temps total de descodificació: "+ str(round(total_time,2)) + " segons.")

    if filter:
        filters_split = filter.split(';')
        filters.main(filters_split, images, metadata, click, is_encoded, is_grayscale)

    if output:
        if not is_encoded:
            start_time = time.time()
            original_images = images.copy()  # for psnr calculation
            click.echo(f'Executant codificació: nTiles[{ntiles}], seekRange[{seekrange}], GOP[{gop}], quality[{quality}]...')
            encoder.main(images, ntiles, seekrange, gop, quality, metadata)
            end_time = time.time()
            total_time = end_time - start_time
            
            click.echo('Guardant video en zip...')
            create_output.create_zip(output, images, metadata, is_encoded)

            encode_info(input, output, total_time, original_images, images)
        else:
            click.echo('Guardant video en zip...')
            create_output.create_zip(output, images, metadata, is_encoded)

        if reproduce:
            reproduce_video.show_video(fps, images)
    else:
        reproduce_video.show_video(fps, images)


def encode_info(input, output, total_time, original_images, images):
    """
    Calcula i mostra informació sobre la compressió després de l'operació de codificació.

    Args:
        input (str): Ruta al fitxer d'entrada.
        output (str): Ruta al fitxer de sortida.
        total_time (float): Temps total de processament en segons.
    """
    original_zip_size = os.path.getsize(input)
    compressed_zip_size = os.path.getsize(output)
    compression_ratio = original_zip_size / compressed_zip_size
    improvement = (original_zip_size - compressed_zip_size) / original_zip_size * 100
    click.echo("Informe sobre la compressió:")
    if total_time > 60:
        minutes = total_time // 60
        seconds = total_time % 60
        click.echo(f"Temps total de processament: {int(minutes)} minuts {str(round(seconds))} segons.")
    else:
        click.echo(f"Temps total de processament: {str(round(total_time,2))} segons.")
    click.echo(f"Ratio de compressió: {str(round(compression_ratio,2))}.")
    click.echo(f"Millora en l'espai ocupat per l'arxiu ZIP final: {str(round(improvement,2))}%")
    psnr = encoder.calculate_psnr(original_images, images)
    if psnr is not None:
        click.echo(f"PSNR del vídeo comprimit: {str(round(psnr,2))} dB.")
    else:
        click.echo("No s'ha pogut calcular el PSNR ja que les imatges són iguals.")

