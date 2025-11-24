"""
Utilidades generales para el proyecto
"""

import os
from pathlib import Path
from typing import Optional


def get_file_extension(filepath: str) -> str:
    """
    Obtiene la extensión del archivo
    
    Args:
        filepath: Ruta del archivo
        
    Returns:
        Extensión del archivo (sin el punto)
    """
    return Path(filepath).suffix.lstrip('.')


def is_markdown_file(filepath: str) -> bool:
    """Verifica si el archivo es Markdown"""
    return get_file_extension(filepath).lower() in ['md', 'markdown']


def is_text_file(filepath: str) -> bool:
    """Verifica si el archivo es texto plano"""
    return get_file_extension(filepath).lower() == 'txt'


def is_code_file(filepath: str) -> bool:
    """Verifica si el archivo es código fuente"""
    code_extensions = [
        'py', 'js', 'jsx', 'ts', 'tsx', 'java', 'c', 'cpp', 'h', 'hpp',
        'cs', 'php', 'rb', 'go', 'rs', 'swift', 'kt', 'scala', 'r',
        'html', 'css', 'scss', 'sass', 'json', 'xml', 'yaml', 'yml',
        'sh', 'bash', 'sql', 'vue', 'dart', 'lua', 'perl', 'asm'
    ]
    return get_file_extension(filepath).lower() in code_extensions


def get_language_from_extension(filepath: str) -> str:
    """
    Determina el lenguaje de programación basado en la extensión
    
    Args:
        filepath: Ruta del archivo
        
    Returns:
        Nombre del lenguaje para Pygments
    """
    ext = get_file_extension(filepath).lower()
    
    language_map = {
        'py': 'python',
        'js': 'javascript',
        'jsx': 'jsx',
        'ts': 'typescript',
        'tsx': 'tsx',
        'java': 'java',
        'c': 'c',
        'cpp': 'cpp',
        'h': 'c',
        'hpp': 'cpp',
        'cs': 'csharp',
        'php': 'php',
        'rb': 'ruby',
        'go': 'go',
        'rs': 'rust',
        'swift': 'swift',
        'kt': 'kotlin',
        'scala': 'scala',
        'r': 'r',
        'html': 'html',
        'css': 'css',
        'scss': 'scss',
        'sass': 'sass',
        'json': 'json',
        'xml': 'xml',
        'yaml': 'yaml',
        'yml': 'yaml',
        'sh': 'bash',
        'bash': 'bash',
        'sql': 'sql',
        'vue': 'vue',
        'dart': 'dart',
        'lua': 'lua',
        'perl': 'perl',
        'asm': 'nasm'
    }
    
    return language_map.get(ext, 'text')


def read_file_content(filepath: str, encoding: str = 'utf-8') -> Optional[str]:
    """
    Lee el contenido de un archivo
    
    Args:
        filepath: Ruta del archivo
        encoding: Codificación del archivo
        
    Returns:
        Contenido del archivo o None si hay error
    """
    try:
        with open(filepath, 'r', encoding=encoding) as f:
            return f.read()
    except UnicodeDecodeError:
        # Intentar con otra codificación
        try:
            with open(filepath, 'r', encoding='latin-1') as f:
                return f.read()
        except Exception as e:
            print(f"Error al leer archivo: {e}")
            return None
    except Exception as e:
        print(f"Error al leer archivo: {e}")
        return None


def ensure_directory_exists(directory: str) -> None:
    """
    Asegura que un directorio exista, creándolo si es necesario
    
    Args:
        directory: Ruta del directorio
    """
    Path(directory).mkdir(parents=True, exist_ok=True)

