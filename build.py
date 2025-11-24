
import os
import sys
import subprocess
from pathlib import Path


def build_executable():
    """Construye el ejecutable usando PyInstaller"""
    
    print("Iniciando construccion de Padlef...")
    print("=" * 50)
    
    # Verificar que PyInstaller esté instalado
    try:
        import PyInstaller
        print(f"PyInstaller {PyInstaller.__version__} encontrado")
    except ImportError:
        print("ERROR: PyInstaller no esta instalado")
        print("Ejecuta: pip install pyinstaller")
        return False
    
    # Crear directorio de assets si no existe
    assets_dir = Path("assets")
    assets_dir.mkdir(exist_ok=True)
    
    # Verificar que existan los archivos necesarios
    if not Path("main.py").exists():
        print("ERROR: No se encuentra main.py")
        return False
    
    if not Path("templates").exists():
        print("ERROR: No se encuentra el directorio templates")
        return False
    
    print("\nConstruyendo ejecutable...")
    
    # Ejecutar PyInstaller
    try:
        if Path("mdPdf.spec").exists():
            # Usar archivo .spec si existe
            cmd = ["pyinstaller", "mdPdf.spec", "--clean"]
        else:
            # Crear ejecutable básico
            cmd = [
                "pyinstaller",
                "--name=mdPdf",
                "--onefile",
                "--windowed",
                "--add-data=templates:templates",
                "--add-data=assets:assets",
                "--hidden-import=weasyprint",
                "--hidden-import=markdown2",
                "--hidden-import=pygments",
                "--hidden-import=PyQt6",
                "main.py"
            ]
        
        result = subprocess.run(cmd, check=True)
        
        if result.returncode == 0:
            # Copiar DLLs de GTK3 en Windows
            if sys.platform == "win32":
                print("\nCopiando DLLs de GTK3...")
                gtk_paths = [
                    Path(r"C:\Program Files\GTK3-Runtime Win64\bin"),
                    Path(r"C:\msys64\mingw64\bin"),
                    Path(r"C:\msys64\ucrt64\bin"),
                ]
                
                dist_path = Path("dist")
                dlls_copied = False
                
                for gtk_path in gtk_paths:
                    if gtk_path.exists():
                        import shutil
                        dll_files = list(gtk_path.glob("*.dll"))
                        if dll_files:
                            for dll in dll_files:
                                try:
                                    shutil.copy2(dll, dist_path)
                                except Exception:
                                    pass
                            dlls_copied = True
                            print(f"   DLLs copiadas desde: {gtk_path}")
                            break
                
                if not dlls_copied:
                    print("   ADVERTENCIA: No se encontraron DLLs de GTK3")
                    print("   El ejecutable puede no funcionar sin ellas")
            
            print("\nConstruccion completada exitosamente!")
            print("\nEl ejecutable se encuentra en:")
            
            if sys.platform == "win32":
                exe_path = Path("dist") / "mdPdf.exe"
            elif sys.platform == "darwin":
                exe_path = Path("dist") / "Padlef.app"
            else:
                exe_path = Path("dist") / "Padlef"
            
            print(f"   {exe_path.absolute()}")
            
            # Información adicional
            print("\nProximos pasos:")
            print("   1. Prueba el ejecutable")
            print("   2. Crea un instalador: create_installer.bat")
            print("   3. O crea un paquete portable: create_portable_package.bat")
            
            return True
        
    except subprocess.CalledProcessError as e:
        print(f"\nERROR durante la construccion: {e}")
        return False
    except Exception as e:
        print(f"\nERROR inesperado: {e}")
        return False


def clean_build_files():
    """Limpia archivos de construcción anteriores"""
    import shutil
    
    print("\nLimpiando archivos de construccion anteriores...")
    
    dirs_to_clean = ["build", "dist", "__pycache__"]
    files_to_clean = ["*.spec"]
    
    for dir_name in dirs_to_clean:
        dir_path = Path(dir_name)
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"   Eliminado: {dir_name}/")
    
    print("   Limpieza completada")


if __name__ == "__main__":
    print("mdPdf - Script de Construcción")
    print("=" * 50)
    
    # Preguntar si limpiar archivos anteriores
    if len(sys.argv) > 1 and sys.argv[1] == "--clean":
        clean_build_files()
    
    # Construir ejecutable
    success = build_executable()
    
    sys.exit(0 if success else 1)

