# Informació i Instruccions

Projecte de pràctiques de Tecnologies Multimèdia per implementació i optimització d'un còdec de vídeo. 

Conté els següents fitxers:

```plaintext
tm-project-base/
├── .gitignore
├── README.md
├── tmproject/
│   ├── docs/
│   |   ├── index.md
│   |   ├── ...
│   |   └── reproduce.md
│   ├── site/
│   ├── __init__.py
│   ├── __main__.py
|   ├── cli.py
|   ├── create_output.py
|   ├── decoder.py
|   ├── encoder.py
|   ├── filters.py
|   ├── mkdocs.yml
|   ├── read_input.py
│   └── reproduce.py
├── scripts/
│   ├── script1.py
│   ├── ...
│   └── scriptN.py
├── requirements.txt
└── setup.py
```

## Creació d'un entorn de Python amb `pyenv`:

Per tal de treballar adecuadament amb aquest repositori, es recomana la creació d'un entorn de Python amb `pyenv`. Aquesta eina permet tenir diferents versions de Python instal·lades al sistema i crear entorns virtuals: 

```bash
# Crear un entorn de Python 3.8.5
pyenv install 3.9.14
pyenv virtualenv 3.9.14 tm
pyenv local tm
```

Comprobar que `pip` i `wheel` estan actualitzats, i instal·lem `ipython`:

```bash
pip install --upgrade pip wheel
pip install ipython
```

## Instal·lació del paquet local com editable: 

Per tal de poder importar el paquet `tmproject` com un mòdul de Python, es pot instal·lar com a paquet editable: 

```bash
pip install -e .
```

## Execució del codi

Per tal de poder executar el projecte desde consola, farem servir la següent comanda:

```bash
tmprojects --help
```

Si no tenim el paquet local instalat es pot fer servir la següent comanda:

```
python -m tmproject --help
```

## Exemples d'execució

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

## Visualitzar documentació

Per tal de visualitzar la documentació s'ha fet un build (mkdocs build) de la documentació prèviament, per accedir sense necessitat de seguir els passos 1-6:
- Obre el teu explorador d'arxius.
- Navega fins al directori del teu projecte MkDocs.
- Troba la carpeta anomenada site.
- Obre la carpeta site.
- Fes doble clic a l'arxiu index.html per obrir-lo al teu navegador web predeterminat.

Si es vol visualitzar la documentació fent servir mkdocs:

1. Assegura't de tenir Python instal·lat al teu sistema. Pots descarregar-lo des de [python.org](https://www.python.org/downloads/).
2. Descarrega els arxius proporcionats. Els arxius python, l'arxiu de configuració `mkdocs.yml` i la carpeta docs han d'estar a la mateixa carpeta .
3. Obre un terminal o línia de comandaments a la carpeta on es troben els arxius.
4. Executa els següents comandaments per instal·lar les dependències necessàries:
    - pip install mkdocs mkdocstrings mkdocstrings-python mkdocs-material
5. Pots obrir el lloc web localment amb el següent comandament:
    - mkdocs serve
6. Obre el teu navegador web i ves a l'adreça `http://localhost:8000` per veure la documentació generada.

## Versions Utilitzades

- IDE: 
  - VSCode: 1.88.1
- Llenguatge:
  - Python: 3.12.2
- Biblioteques:
  - matplotlib: 3.8.3
  - mkdocs: 1.5.3
  - mkdocstrings: 0.24.3
  - mkdocstrings-python: 1.9.2
  - mkdocs-material: 9.5.17
  - click: 8.1.7
  - tqdm: 4.66.4
  - imageio: 2.34.0
  - numpy: 1.26.4
  - pillow: 10.2.0
  - opencv-python: 4.9.0.80

## Utilització d'Eines d'Intel·ligència Artificial

Per al desenvolupament d'aquest projecte s'ha utilitzat l'eina GitHub Copilot, proporcionada per la Universitat. S'ha fet servir tant pels comentaris de les diferents funcions com pel desenvolupament i com a ajuda d'algunes funcions.
