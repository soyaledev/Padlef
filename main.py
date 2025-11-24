

import sys
import os
from pathlib import Path


def setup_gtk_path():
    """Configura el PATH para encontrar las bibliotecas GTK3 en Windows"""
    if sys.platform == 'win32':
        # Posibles ubicaciones de GTK3 en Windows
        gtk_paths = [
            r"C:\Program Files\GTK3-Runtime Win64\bin",
            r"C:\msys64\mingw64\bin",
            r"C:\msys64\ucrt64\bin",
            r"C:\gtk\bin",
        ]
        
        # Agregar las rutas que existan al PATH
        for gtk_path in gtk_paths:
            if Path(gtk_path).exists():
                os.environ['PATH'] = gtk_path + os.pathsep + os.environ.get('PATH', '')
                print(f"GTK3 encontrado en: {gtk_path}")
                break


def main():
    """Función principal"""
    try:
        # Configurar GTK3 antes de importar la GUI
        setup_gtk_path()
        
        # Importar después de configurar el PATH
        from src.gui.main_window import run_app
        
        run_app()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

