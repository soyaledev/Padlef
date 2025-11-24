

import html
from typing import Optional
from pathlib import Path


class TextConverter:
    """Convierte archivos de texto plano a HTML"""
    
    def __init__(self):
        """Inicializa el conversor"""
        pass
    
    def convert(
        self, 
        text_content: str, 
        filename: Optional[str] = None,
        preserve_formatting: bool = True
    ) -> str:
        """
        Convierte texto plano a HTML
        
        Args:
            text_content: Contenido del texto
            filename: Nombre del archivo (opcional)
            preserve_formatting: Si preservar el formato (espacios, saltos de línea)
            
        Returns:
            Contenido HTML generado
        """
        # Escapar caracteres HTML especiales
        escaped_content = html.escape(text_content)
        
        # Agregar encabezado si se proporciona nombre de archivo
        html_content = ''
        if filename:
            html_content += f'<div class="document-header">'
            html_content += f'<div class="document-title">{filename}</div>'
            html_content += f'<div class="document-info">Archivo de texto plano</div>'
            html_content += f'</div>'
        
        # Preservar formato si se solicita
        if preserve_formatting:
            # Usar <pre> para mantener espacios y saltos de línea
            html_content += f'<pre style="white-space: pre-wrap; word-wrap: break-word;">{escaped_content}</pre>'
        else:
            # Convertir saltos de línea a <br> y párrafos
            paragraphs = escaped_content.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    # Reemplazar saltos de línea simples con <br>
                    para = para.replace('\n', '<br>')
                    html_content += f'<p>{para}</p>'
        
        return html_content
    
    def convert_file(self, filepath: str, preserve_formatting: bool = True) -> str:
        """
        Convierte un archivo de texto a HTML
        
        Args:
            filepath: Ruta del archivo de texto
            preserve_formatting: Si preservar el formato
            
        Returns:
            Contenido HTML generado
        """
        from ..utils import read_file_content
        
        content = read_file_content(filepath)
        if content is None:
            raise ValueError(f"No se pudo leer el archivo: {filepath}")
        
        filename = Path(filepath).name
        return self.convert(content, filename, preserve_formatting)

