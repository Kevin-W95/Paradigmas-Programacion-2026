@echo off
title Herramienta CLI - Analisis de Datos Modular
cls
echo ========================================================
echo   Iniciando Herramienta CLI Modular para Analisis
echo   Paradigmas de Programacion
echo ========================================================
echo.

where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] No se encontro 'python' en la variable PATH del sistema.
    echo Asegurate de tener Python instalado y anadido al PATH de Windows.
    echo.
    pause
    exit /b 1
)

echo Selecciona una opcion:
echo  1. Ejecutar aplicacion interactiva (principal.py)
echo  2. Ejecutar suite de pruebas unitarias (test_cli.py)
echo  3. Salir
echo.
set /p opcion="Opcion [1-3]: "

if "%opcion%"=="1" (
    cls
    python principal.py
) else if "%opcion%"=="2" (
    cls
    python test_cli.py
    pause
) else (
    echo Saliendo...
)

