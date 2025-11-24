"""
Generador de archivos PDF a partir de HTML
"""

from weasyprint import HTML, CSS
from pathlib import Path
from typing import Optional

from .converters import MarkdownConverter, CodeConverter, TextConverter
from .utils import (
    is_markdown_file, 
    is_text_file, 
    is_code_file,
    ensure_directory_exists
)


class PDFGenerator:
    """Genera archivos PDF a partir de diferentes tipos de archivos"""
    
    def __init__(self, style: str = 'default'):
        """
        Inicializa el generador de PDF
        
        Args:
            style: Estilo de Pygments para resaltado de código
        """
        self.markdown_converter = MarkdownConverter()
        self.code_converter = CodeConverter(style=style)
        self.text_converter = TextConverter()
        
        # Obtener ruta del archivo CSS
        self.css_path = Path(__file__).parent.parent / 'templates' / 'pdf_styles.css'
    
    def _get_html_template(self, content: str, title: str = "Documento") -> str:
        """
        Crea una plantilla HTML completa
        
        Args:
            content: Contenido HTML del cuerpo
            title: Título del documento
            
        Returns:
            HTML completo con estructura
        """
        # Obtener CSS de Pygments para resaltado de sintaxis
        pygments_css = self.code_converter.get_css()
        
        html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        {pygments_css}
    </style>
</head>
<body>
    {content}
</body>
</html>
"""
        return html
    
    def convert_to_pdf(
        self, 
        input_file: str, 
        output_file: Optional[str] = None,
        line_numbers: bool = True
    ) -> str:
        """
        Convierte un archivo a PDF
        
        Args:
            input_file: Ruta del archivo de entrada
            output_file: Ruta del archivo PDF de salida (opcional)
            line_numbers: Si mostrar números de línea en código
            
        Returns:
            Ruta del archivo PDF generado
        """
        input_path = Path(input_file)
        
        # Determinar archivo de salida si no se proporciona
        if output_file is None:
            output_file = str(input_path.with_suffix('.pdf'))
        
        # Asegurar que el directorio de salida existe
        output_path = Path(output_file)
        ensure_directory_exists(str(output_path.parent))
        
        # Convertir según el tipo de archivo
        try:
            if is_markdown_file(input_file):
                html_content = self.markdown_converter.convert_file(input_file)
            elif is_code_file(input_file):
                html_content = self.code_converter.convert_file(input_file, line_numbers)
            elif is_text_file(input_file):
                html_content = self.text_converter.convert_file(input_file)
            else:
                # Por defecto, tratar como texto plano
                html_content = self.text_converter.convert_file(input_file)
            
            # Crear HTML completo
            full_html = self._get_html_template(
                html_content, 
                title=input_path.name
            )
            
            # Generar PDF
            self._generate_pdf_from_html(full_html, output_file)
            
            return output_file
            
        except Exception as e:
            raise Exception(f"Error al convertir archivo a PDF: {str(e)}")
    
    def _generate_pdf_from_html(self, html_content: str, output_file: str) -> None:
        """
        Genera un PDF a partir de contenido HTML
        
        Args:
            html_content: Contenido HTML completo
            output_file: Ruta del archivo PDF de salida
        """
        # Cargar CSS externo si existe
        stylesheets = []
        if self.css_path.exists():
            stylesheets.append(CSS(filename=str(self.css_path)))
        
        # Generar PDF
        html_obj = HTML(string=html_content)
        html_obj.write_pdf(
            output_file,
            stylesheets=stylesheets
        )
    
    def convert_multiple_files(
        self, 
        input_files: list[str],
        output_directory: Optional[str] = None,
        line_numbers: bool = True
    ) -> list[str]:
        """
        Convierte múltiples archivos a PDF
        
        Args:
            input_files: Lista de rutas de archivos de entrada
            output_directory: Directorio de salida (opcional)
            line_numbers: Si mostrar números de línea en código
            
        Returns:
            Lista de rutas de archivos PDF generados
        """
        output_files = []
        
        for input_file in input_files:
            try:
                if output_directory:
                    input_path = Path(input_file)
                    output_file = str(Path(output_directory) / input_path.with_suffix('.pdf').name)
                else:
                    output_file = None
                
                result = self.convert_to_pdf(input_file, output_file, line_numbers)
                output_files.append(result)
                
            except Exception as e:
                print(f"Error al convertir {input_file}: {str(e)}")
                continue
        
        return output_files
    
    def get_supported_extensions(self) -> list[str]:
        """
        Obtiene la lista de extensiones soportadas
        
        Returns:
            Lista de extensiones de archivo soportadas
        """
        return [
            # Markdown
            '.md', '.markdown',
            # Texto
            '.txt',
            # Código
            '.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.c', '.cpp', '.h', '.hpp',
            '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala', '.r',
            '.html', '.css', '.scss', '.sass', '.json', '.xml', '.yaml', '.yml',
            '.sh', '.bash', '.sql', '.vue', '.dart', '.lua', '.perl', '.asm'
        ]

