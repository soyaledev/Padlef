"""
Conversor de archivos de código fuente a HTML con resaltado de sintaxis
"""

from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from typing import Optional
from pathlib import Path


class CodeConverter:
    """Convierte archivos de código a HTML con resaltado de sintaxis"""
    
    def __init__(self, style: str = 'default'):
        """
        Inicializa el conversor
        
        Args:
            style: Estilo de Pygments a usar (default, monokai, github, etc.)
        """
        self.style = style
    
    def convert(
        self, 
        code_content: str, 
        language: str = 'text',
        filename: Optional[str] = None,
        line_numbers: bool = True
    ) -> str:
        """
        Convierte código fuente a HTML con resaltado de sintaxis
        
        Args:
            code_content: Contenido del código
            language: Lenguaje de programación
            filename: Nombre del archivo (opcional)
            line_numbers: Si mostrar números de línea
            
        Returns:
            Contenido HTML con código resaltado
        """
        try:
            # Obtener el lexer apropiado
            if language and language != 'text':
                lexer = get_lexer_by_name(language, stripall=True)
            else:
                # Intentar adivinar el lenguaje
                lexer = guess_lexer(code_content)
        except Exception:
            # Si falla, usar texto plano
            from pygments.lexers import TextLexer
            lexer = TextLexer()
        
        # Configurar el formateador HTML
        formatter = HtmlFormatter(
            style=self.style,
            linenos='table' if line_numbers else False,
            cssclass='highlight',
            full=False
        )
        
        # Generar HTML con resaltado
        highlighted_code = highlight(code_content, lexer, formatter)
        
        # Agregar encabezado con información del archivo
        html_content = ''
        if filename:
            language_name = lexer.name if hasattr(lexer, 'name') else language
            html_content += f'<div class="document-header">'
            html_content += f'<div class="document-title">{filename}</div>'
            html_content += f'<div class="document-info">Archivo de código - {language_name}</div>'
            html_content += f'</div>'
        
        html_content += f'<div class="code-content">{highlighted_code}</div>'
        
        return html_content
    
    def convert_file(self, filepath: str, line_numbers: bool = True) -> str:
        """
        Convierte un archivo de código a HTML
        
        Args:
            filepath: Ruta del archivo de código
            line_numbers: Si mostrar números de línea
            
        Returns:
            Contenido HTML generado
        """
        from ..utils import read_file_content, get_language_from_extension
        
        content = read_file_content(filepath)
        if content is None:
            raise ValueError(f"No se pudo leer el archivo: {filepath}")
        
        filename = Path(filepath).name
        language = get_language_from_extension(filepath)
        
        return self.convert(content, language, filename, line_numbers)
    
    def get_css(self) -> str:
        """
        Obtiene el CSS necesario para el resaltado de sintaxis
        
        Returns:
            CSS de Pygments
        """
        formatter = HtmlFormatter(style=self.style)
        return formatter.get_style_defs('.highlight')

