@echo off
REM Script para crear un paquete portable (ZIP) de mdPdf

echo ========================================
echo mdPdf - Crear Paquete Portable
echo ========================================
echo.

REM Verificar que existe el ejecutable
if not exist "dist\mdPdf.exe" (
    echo ERROR: No se encuentra dist\mdPdf.exe
    echo Ejecuta primero: python build.py
    pause
    exit /b 1
)

REM Crear directorio temporal para el paquete
set PACKAGE_DIR=mdPdf-Portable
if exist "%PACKAGE_DIR%" rmdir /s /q "%PACKAGE_DIR%"
mkdir "%PACKAGE_DIR%"

echo Copiando archivos...

REM Copiar ejecutable
copy "dist\mdPdf.exe" "%PACKAGE_DIR%\"

REM Copiar DLLs
copy "dist\*.dll" "%PACKAGE_DIR%\" 2>nul

REM Copiar templates
xcopy "templates" "%PACKAGE_DIR%\templates\" /E /I /Y

REM Crear archivo README
(
echo mdPdf - Conversor de Archivos a PDF
echo ====================================
echo.
echo Version Portable - No requiere instalacion
echo.
echo INSTRUCCIONES:
echo.
echo 1. Extrae todos los archivos de este ZIP
echo 2. Ejecuta mdPdf.exe
echo 3. Arrastra archivos .md, .txt, .js, etc. a la ventana
echo 4. Haz clic en "Convertir a PDF"
echo.
echo FORMATOS SOPORTADOS:
echo - Markdown: .md
echo - Texto: .txt
echo - Codigo: .js, .jsx, .ts, .tsx, .py, .java, .c, .cpp, .html, .css, etc.
echo.
echo REQUISITOS:
echo - Windows 10 o superior
echo - No requiere instalacion de Python
echo.
echo Para mas informacion, visita el repositorio del proyecto.
) > "%PACKAGE_DIR%\LEEME.txt"

REM Crear ZIP usando PowerShell
echo Creando archivo ZIP...
powershell -Command "Compress-Archive -Path '%PACKAGE_DIR%\*' -DestinationPath 'mdPdf-Portable.zip' -Force"

REM Limpiar directorio temporal
rmdir /s /q "%PACKAGE_DIR%"

echo.
echo ========================================
echo Paquete portable creado exitosamente!
echo ========================================
echo.
echo El archivo ZIP se encuentra en:
echo mdPdf-Portable.zip
echo.
echo Puedes compartir este archivo con otros usuarios.
echo Solo necesitan extraerlo y ejecutar mdPdf.exe
echo.
pause

