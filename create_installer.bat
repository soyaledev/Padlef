@echo off
REM Script para crear el instalador de Padlef
REM Requiere Inno Setup instalado

echo ========================================
echo Padlef - Crear Instalador
echo ========================================
echo.

REM Verificar que existe el ejecutable
if not exist "dist\mdPdf.exe" (
    echo ERROR: No se encuentra dist\mdPdf.exe
    echo Ejecuta primero: python build.py
    pause
    exit /b 1
)

REM Verificar que Inno Setup esta instalado
set INNO_SETUP="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist %INNO_SETUP% (
    set INNO_SETUP="C:\Program Files\Inno Setup 6\ISCC.exe"
)

if not exist %INNO_SETUP% (
    echo.
    echo ERROR: Inno Setup no encontrado
    echo.
    echo Por favor instala Inno Setup desde:
    echo https://jrsoftware.org/isdl.php
    echo.
    echo O compila manualmente el archivo installer.iss
    echo.
    pause
    exit /b 1
)

REM Crear directorio para el instalador
if not exist "installer" mkdir installer

REM Compilar el instalador
echo Compilando instalador...
%INNO_SETUP% installer.iss

if exist "installer\Padlef-Setup.exe" (
    echo.
    echo ========================================
    echo Instalador creado exitosamente!
    echo ========================================
    echo.
    echo El instalador se encuentra en:
    echo installer\Padlef-Setup.exe
    echo.
) else (
    echo.
    echo ERROR: No se pudo crear el instalador
    echo.
)

pause

