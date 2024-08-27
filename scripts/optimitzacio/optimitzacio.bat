@echo off
setlocal enabledelayedexpansion

REM Definir el rango de valores GOP, seekrange, calidad y ntiles que deseas probar
set GOP_MIN=2
set GOP_MAX=10
set NTILES_MIN=2
set NTILES_MAX=4
set QUALITY_MIN=80
set QUALITY_MAX=95
set SEEKRANGE_MIN=0
set SEEKRANGE_MAX=2

REM Definir la ruta del directorio de trabajo
set "working_dir=E:\ProjecteMultimedia"

REM Limpiar la carpeta tmp
del /Q "%working_dir%\data\tmp\*"

REM Crear un archivo de texto para almacenar los resultados
echo GOP NTiles SeekRange Quality Frames_I Frames_P Ratio_Compression PSNR > resultados.txt

REM Bucle para generar videos con diferentes valores GOP y recopilar información
for /L %%g in (%GOP_MIN%, 2, %GOP_MAX%) do (
    echo Procesando GOP = %%g
    tmproject -i "%working_dir%\data\raw\Cubo.zip" --GOP %%g -o "%working_dir%\data\processed\cubo_encoded.zip" > temp.txt 2>&1
    type temp.txt
    for /F "tokens=6,8,10,12" %%a in ('type temp.txt') do (
        echo %%g N/A N/A N/A %%a %%b %%c %%d >> resultados.txt
    )
)

REM Bucle para generar videos con diferentes valores NTiles y recopilar información
for /L %%n in (%NTILES_MIN%, 1, %NTILES_MAX%) do (
    echo Procesando NTiles = %%n
    tmproject -i "%working_dir%\data\raw\Cubo.zip" --nTiles %%n %%n -o "%working_dir%\data\processed\cubo_encoded.zip" 2>&1 
    type temp.txt
    for /F "tokens=7,9,12,15,16,18,19" %%a in ('type temp.txt') do (
        echo N/A %%n N/A N/A %%a %%b %%c %%d >> resultados.txt
    )
)

REM Bucle para generar videos con diferentes valores Quality y recopilar información
for /L %%q in (%QUALITY_MIN%, 5, %QUALITY_MAX%) do (
    set /a "quality=%%q * 10 / 10"
    echo Procesando Quality = !quality!
    tmproject -i "%working_dir%\data\raw\Cubo.zip" --quality !quality! -o "%working_dir%\data\processed\cubo_encoded.zip" 2>&1
    type temp.txt
    for /F "tokens=7,9,12,15,16,18,19" %%a in ('type temp.txt') do (
        echo N/A N/A N/A !quality! %%a %%b %%c %%d >> resultados.txt
    )
)

REM Bucle para generar videos con diferentes valores SeekRange y recopilar información
for /L %%s in (%SEEKRANGE_MIN%, 1, %SEEKRANGE_MAX%) do (
    echo Procesando SeekRange = %%s
    tmproject -i "%working_dir%\data\raw\Cubo.zip" --seekRange %%s -o "%working_dir%\data\processed\cubo_encoded.zip" 2>&1
    type temp.txt
    for /F "tokens=7,9,12,15,16,18,19" %%a in ('type temp.txt') do (
        echo N/A N/A %%s N/A %%a %%b %%c %%d >> resultados.txt
    )
)

REM Limpiar la carpeta tmp
del /Q "%working_dir%\data\tmp\*"

REM Eliminar temp.txt
del /Q temp.txt

echo Proceso completado. Los resultados se han guardado en resultados.txt.
pause
endlocal