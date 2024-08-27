# Documentació de cli.py

## Introducció

El fitxer `cli.py` és un component essencial del projecte del còdec de vídeo, on s'implementa la interfície de línia de comandes (CLI) utilitzant la biblioteca Click. Aquest mòdul facilita la interacció amb l'usuari, permetent-li executar diverses operacions en fitxers d'imatge i vídeo mitjançant comandaments específics.

## Ús de Click

Click és una biblioteca de Python per a la creació d'interfícies de línia de comandes. Permet definir comandaments, opcions i arguments de forma fàcil i flexible. `cli.py` utilitza Click per proporcionar una CLI intuïtiva i fàcil d'utilitzar per al projecte del còdec de vídeo.

## Exemples d'Ús

- Codificar un vídeo i desar el resultat en un fitxer ZIP:

   ```
   tmproject -i video.avi -o video_comprimit.zip --fps 30 --filter "sepia;brillo=-50,1.5" --quality 0.8
   ```

- Mostrar informació sobre els filtres disponibles:

   ```
   tmproject -i video.avi --filter-help
   ```

- Reproduir un vídeo amb una taxa de fotogrames de 60 FPS:

   ```
   tmproject -i video.avi --fps 60
   ```

- Descodificar un video, aplicar filtres i reproduir-lo:

   ```
   tmproject -i video_comprimit.zip --filter "averaging;grey;edges;embossing;sharp;sepia;negative;blur=5;brillo=-50,1"
   ```

Aquest són exemples de com utilitzar la CLI proporcionada per `cli.py`. Pots ajustar els arguments segons les teves necessitats específiques.

## Funcions

::: cli