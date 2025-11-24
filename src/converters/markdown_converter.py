"""
Conversor de archivos Markdown a HTML
"""

import markdown2
from typing import Optional


class MarkdownConverter:
    """Convierte archivos Markdown a HTML"""
    
    def __init__(self):
        """Inicializa el conversor con extras de markdown2"""
        self.extras = [
            'fenced-code-blocks',  # Bloques de código con ```
            'tables',              # Soporte para tablas
            'break-on-newline',    # Saltos de línea
            'strike',              # Texto tachado
            'task_list',           # Listas de tareas
            'code-friendly',       # Mejor manejo de código
            'header-ids',          # IDs en encabezados
            'footnotes',           # Notas al pie
            'cuddled-lists',       # Listas sin líneas en blanco
        ]
    
    def convert(self, markdown_content: str, filename: Optional[str] = None) -> str:
        """
        Convierte contenido Markdown a HTML
        
        Args:
            markdown_content: Contenido en formato Markdown
            filename: Nombre del archivo (opcional, para el título)
            
        Returns:
            Contenido HTML generado
        """
        # Convertir Markdown a HTML
        html_content = markdown2.markdown(
            markdown_content,
            extras=self.extras
        )
        
        # Agregar encabezado si se proporciona nombre de archivo
        if filename:
            header = f'<div class="document-header">'
            header += f'<div class="document-title">{filename}</div>'
            header += f'<div class="document-info">Documento Markdown</div>'
            header += f'</div>'
            html_content = header + html_content
        
        return html_content
    
    def convert_file(self, filepath: str) -> str:
        """
        Convierte un archivo Markdown a HTML
        
        Args:
            filepath: Ruta del archivo Markdown
            
        Returns:
            Contenido HTML generado
        """
        from pathlib import Path
        from ..utils import read_file_content
        
        content = read_file_content(filepath)
        if content is None:
            raise ValueError(f"No se pudo leer el archivo: {filepath}")
        
        filename = Path(filepath).name
        return self.convert(content, filename)

