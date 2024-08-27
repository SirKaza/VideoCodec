# Documentació del Codi

Benvinguts a la documentació del codi del còdec de vídeo per al Projecte de Pràctiques de Tecnologies Multimèdia. Aquest codi implementa les diferents funcionalitats demanades.


## Contingut

Aquest projecte es divideix en diferents parts, cadascun d'ells compleix una funcionalitat diferent i junts composen el còdec de vídeo.

- [cli.py](cli.md): Aquest fitxer conté la implementació de la interfície de línia de comandes (CLI) per al projecte. Defineix els comandaments i opcions que els usuaris poden utilitzar per interactuar amb el programa des de la línia de comandes. A més, en el nostre projecte funciona com una clase Controller, i actua com a intermediari entre les diferents funcionalitats del còdec.

- [create_output.py](output.md): Aquest fitxer conté funcions per crear la sortida del projecte, creant un fitxer zip amb les diferents imatges en format JPEG. Aquestes imatges poden estar modificades o no gracies a altres mòduls. En cas que es comprimeixi les imatges, s'afegira un arxiu JSON amb la informació per descodificar-les.

- [decoder.py](decoder.md): En aquest fitxer es troba la implementació del descodificador, que pren imatges codificades i les converteix de nou en el seu format original.

- [encoder.py](encoder.md): Aquest fitxer conté  la implementació del codificador. Aquest codificador fa la compressió d'un vídeo sense audio. Per fer la compressió s'ha fet servir un algoritme de correspondencia de tesela.

- [filters.py](filters.md): Aquí es troben les implementacions dels diferents filtres que es poden aplicar al vídeo processats pel projecte. Aquests filtres poden incloure funcions per ajustar la brillantor, el contrast, aplicar efectes de color, etc.

- [read_input.py](input.md): Aquest fitxer conté funcions per llegir les dades d'entrada del projecte, com arxius d'imatge, zips o vídeo.

- [reproduce_video.py](reproduce.md): Aquí es troba la lògica per reproduir vídeos processats pel projecte.

Hi ha altres parts del projecte que no tenen gaire rellevància i s'expliquen breument a continuació:

- `__init__.py`: Aquest fitxer indica que el directori `tmproject` és un paquet de Python, permetent la importació de mòduls dins d'ell.

- `__main__.py`: Aquest fitxer conté el punt d'entrada principal del paquet. S'executa quan es crida al paquet com a script (`python -m tmproject` o `tmproject` en cas que tinguis el paquet local). Aquest arxiu serveix únicament per cridar la funció main de `cli.py`.