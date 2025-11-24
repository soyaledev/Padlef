

from pathlib import Path
from PIL import Image
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt

def svg_to_ico(svg_path: str, ico_path: str):
    """Convierte SVG a ICO usando PyQt6 y PIL"""
    try:
        renderer = QSvgRenderer(svg_path)
        if not renderer.isValid():
            print(f"Error: SVG invalido: {svg_path}")
            return False
        
        # Crear pixmap de 256x256
        pixmap = QPixmap(256, 256)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        
        # Guardar como PNG temporal
        png_path = svg_path.replace('.svg', '_temp.png')
        pixmap.save(png_path)
        
        # Convertir PNG a ICO con múltiples tamaños
        img = Image.open(png_path)
        img.save(ico_path, format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
        
        # Eliminar PNG temporal
        Path(png_path).unlink()
        
        print(f"Icono creado: {ico_path}")
        return True
    except Exception as e:
        print(f"Error al crear icono: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    svg_file = Path("assets/logoPadlefTipoFavicon.svg")
    ico_file = Path("assets/icon.ico")
    
    if svg_file.exists():
        if svg_to_ico(str(svg_file), str(ico_file)):
            print("Conversion exitosa!")
        else:
            print("Error en la conversion")
    else:
        print(f"No se encuentra: {svg_file}")

