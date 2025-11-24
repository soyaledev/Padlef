"""
Ventana principal de la aplicación mdPdf
"""

import sys
from pathlib import Path
from typing import List, Optional

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QListWidget, QFileDialog, QMessageBox,
    QCheckBox, QGroupBox, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QDragEnterEvent, QDropEvent, QPixmap, QPainter
from PyQt6.QtSvg import QSvgRenderer

from ..pdf_generator import PDFGenerator


class ConversionThread(QThread):
    """Thread para realizar la conversión en segundo plano"""
    
    progress = pyqtSignal(int, int)  # (actual, total)
    finished = pyqtSignal(list)  # Lista de archivos generados
    error = pyqtSignal(str)  # Mensaje de error
    
    def __init__(self, files: List[str], output_dir: Optional[str], 
                 line_numbers: bool, style: str):
        super().__init__()
        self.files = files
        self.output_dir = output_dir
        self.line_numbers = line_numbers
        self.style = style
    
    def run(self):
        """Ejecuta la conversión"""
        try:
            generator = PDFGenerator(style=self.style)
            output_files = []
            
            for i, file in enumerate(self.files, 1):
                try:
                    output_file = generator.convert_to_pdf(
                        file,
                        output_file=None if not self.output_dir else 
                                   str(Path(self.output_dir) / Path(file).with_suffix('.pdf').name),
                        line_numbers=self.line_numbers
                    )
                    output_files.append(output_file)
                    self.progress.emit(i, len(self.files))
                except Exception as e:
                    self.error.emit(f"Error en {Path(file).name}: {str(e)}")
            
            self.finished.emit(output_files)
            
        except Exception as e:
            self.error.emit(f"Error general: {str(e)}")


class MainWindow(QMainWindow):
    """Ventana principal de la aplicación"""
    
    def __init__(self):
        super().__init__()
        self.files_to_convert: List[str] = []
        self.output_directory: Optional[str] = None
        self.conversion_thread: Optional[ConversionThread] = None
        
        # Obtener ruta de assets
        self.assets_path = self._get_assets_path()
        
        self.init_ui()
    
    def _get_assets_path(self) -> Path:
        """Obtiene la ruta de la carpeta assets"""
        # Intentar desde el directorio del ejecutable (cuando está empaquetado)
        if getattr(sys, 'frozen', False):
            base_path = Path(sys.executable).parent
        else:
            base_path = Path(__file__).parent.parent.parent
        
        return base_path / 'assets'
    
    def _load_image(self, filename: str) -> Optional[QPixmap]:
        """Carga una imagen (PNG, JPG, SVG) desde assets"""
        file_path = self.assets_path / filename
        
        if not file_path.exists():
            return None
        
        # Intentar cargar como imagen raster (PNG, JPG)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            pixmap = QPixmap(str(file_path))
            if not pixmap.isNull():
                return pixmap
        
        # Intentar cargar como SVG
        elif filename.lower().endswith('.svg'):
            renderer = QSvgRenderer(str(file_path))
            if renderer.isValid():
                pixmap = QPixmap(200, 200)  # Tamaño por defecto
                pixmap.fill(Qt.GlobalColor.transparent)
                painter = QPainter(pixmap)
                renderer.render(painter)
                painter.end()
                return pixmap
        
        return None
    
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        self.setWindowTitle("Padlef - Conversor de Archivos a PDF")
        self.setMinimumSize(800, 600)
        
        # Cargar icono de la ventana (favicon)
        favicon_pixmap = self._load_image('logoPadlefTipoFavicon.svg')
        if favicon_pixmap:
            icon = QIcon(favicon_pixmap.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            self.setWindowIcon(icon)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout()

        central_widget.setLayout(main_layout)
        
        # Título
        title_label = QLabel("Conversor de Archivos a PDF")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Descripción
        desc_label = QLabel(
            "Convierte archivos Markdown (.md), texto (.txt) y código fuente a PDF"
        )
        desc_label.setStyleSheet("font-size: 12px; color: #666; margin-bottom: 10px;")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(desc_label)
        
        # Sección de archivos
        files_group = QGroupBox("Archivos a Convertir")
        files_layout = QVBoxLayout()
        files_group.setLayout(files_layout)
        
        # Botones de agregar/eliminar archivos
        buttons_layout = QHBoxLayout()
        
        self.add_files_btn = QPushButton("Agregar Archivos")
        self.add_files_btn.clicked.connect(self.add_files)
        buttons_layout.addWidget(self.add_files_btn)
        
        self.remove_files_btn = QPushButton("Eliminar Seleccionados")
        self.remove_files_btn.clicked.connect(self.remove_files)
        self.remove_files_btn.setEnabled(False)
        buttons_layout.addWidget(self.remove_files_btn)
        
        self.clear_files_btn = QPushButton("Limpiar Todo")
        self.clear_files_btn.clicked.connect(self.clear_files)
        self.clear_files_btn.setEnabled(False)
        buttons_layout.addWidget(self.clear_files_btn)
        
        files_layout.addLayout(buttons_layout)
        
        # Lista de archivos
        self.files_list = QListWidget()
        self.files_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.files_list.itemSelectionChanged.connect(self.on_selection_changed)
        self.files_list.setAcceptDrops(True)
        self.files_list.setStyleSheet("min-height: 200px;")
        files_layout.addWidget(self.files_list)
        
        # Habilitar drag and drop
        self.setAcceptDrops(True)
        
        main_layout.addWidget(files_group)
        
        # Opciones
        options_group = QGroupBox("Opciones")
        options_layout = QVBoxLayout()
        options_group.setLayout(options_layout)
        
        # Directorio de salida
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Directorio de salida:"))
        
        self.output_label = QLabel("(Mismo directorio que el archivo original)")
        self.output_label.setStyleSheet("color: #666; font-style: italic;")
        output_layout.addWidget(self.output_label, 1)
        
        self.select_output_btn = QPushButton("Seleccionar")
        self.select_output_btn.clicked.connect(self.select_output_directory)
        output_layout.addWidget(self.select_output_btn)
        
        self.clear_output_btn = QPushButton("X")
        self.clear_output_btn.clicked.connect(self.clear_output_directory)
        self.clear_output_btn.setEnabled(False)
        self.clear_output_btn.setMaximumWidth(40)
        output_layout.addWidget(self.clear_output_btn)
        
        options_layout.addLayout(output_layout)
        
        # Números de línea
        self.line_numbers_check = QCheckBox("Mostrar números de línea en código")
        self.line_numbers_check.setChecked(True)
        options_layout.addWidget(self.line_numbers_check)
        
        main_layout.addWidget(options_group)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Botón de conversión
        self.convert_btn = QPushButton("Convertir a PDF")
        self.convert_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        self.convert_btn.clicked.connect(self.convert_files)
        self.convert_btn.setEnabled(False)
        main_layout.addWidget(self.convert_btn)
        
        # Información de formatos soportados
        info_label = QLabel(
            "Formatos soportados: .md, .txt, .py, .js, .jsx, .ts, .tsx, .java, "
            ".c, .cpp, .cs, .php, .rb, .go, .rs, .swift, .kt, .html, .css, .json, .xml, y más"
        )
        info_label.setStyleSheet("font-size: 10px; color: #999; margin-top: 10px;")
        info_label.setWordWrap(True)
        main_layout.addWidget(info_label)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Maneja el evento de arrastrar archivos"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        """Maneja el evento de soltar archivos"""
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        self.add_files_to_list(files)
    
    def add_files(self):
        """Abre diálogo para agregar archivos"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Seleccionar Archivos",
            "",
            "Todos los archivos soportados (*.md *.txt *.py *.js *.jsx *.ts *.tsx *.java *.c *.cpp *.cs *.php *.rb *.go *.rs *.swift *.kt *.html *.css *.json *.xml);;Todos los archivos (*.*)"
        )
        
        if files:
            self.add_files_to_list(files)
    
    def add_files_to_list(self, files: List[str]):
        """Agrega archivos a la lista"""
        for file in files:
            if file not in self.files_to_convert:
                self.files_to_convert.append(file)
                self.files_list.addItem(file)
        
        self.update_buttons_state()
    
    def remove_files(self):
        """Elimina archivos seleccionados"""
        selected_items = self.files_list.selectedItems()
        
        for item in selected_items:
            file_path = item.text()
            if file_path in self.files_to_convert:
                self.files_to_convert.remove(file_path)
            self.files_list.takeItem(self.files_list.row(item))
        
        self.update_buttons_state()
    
    def clear_files(self):
        """Limpia todos los archivos"""
        self.files_to_convert.clear()
        self.files_list.clear()
        self.update_buttons_state()
    
    def select_output_directory(self):
        """Selecciona directorio de salida"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar Directorio de Salida"
        )
        
        if directory:
            self.output_directory = directory
            self.output_label.setText(directory)
            self.output_label.setStyleSheet("color: #2c3e50;")
            self.clear_output_btn.setEnabled(True)
    
    def clear_output_directory(self):
        """Limpia el directorio de salida"""
        self.output_directory = None
        self.output_label.setText("(Mismo directorio que el archivo original)")
        self.output_label.setStyleSheet("color: #666; font-style: italic;")
        self.clear_output_btn.setEnabled(False)
    
    def on_selection_changed(self):
        """Maneja cambios en la selección de archivos"""
        has_selection = len(self.files_list.selectedItems()) > 0
        self.remove_files_btn.setEnabled(has_selection)
    
    def update_buttons_state(self):
        """Actualiza el estado de los botones"""
        has_files = len(self.files_to_convert) > 0
        self.convert_btn.setEnabled(has_files)
        self.clear_files_btn.setEnabled(has_files)
    
    def convert_files(self):
        """Inicia la conversión de archivos"""
        if not self.files_to_convert:
            return
        
        # Deshabilitar controles
        self.convert_btn.setEnabled(False)
        self.add_files_btn.setEnabled(False)
        self.remove_files_btn.setEnabled(False)
        self.clear_files_btn.setEnabled(False)
        
        # Mostrar barra de progreso
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(self.files_to_convert))
        self.progress_bar.setValue(0)
        
        # Crear y ejecutar thread de conversión
        self.conversion_thread = ConversionThread(
            self.files_to_convert,
            self.output_directory,
            self.line_numbers_check.isChecked(),
            'default'  # Siempre usar estilo default
        )
        
        self.conversion_thread.progress.connect(self.on_conversion_progress)
        self.conversion_thread.finished.connect(self.on_conversion_finished)
        self.conversion_thread.error.connect(self.on_conversion_error)
        
        self.conversion_thread.start()
    
    def on_conversion_progress(self, current: int, total: int):
        """Actualiza el progreso de la conversión"""
        self.progress_bar.setValue(current)
    
    def on_conversion_finished(self, output_files: List[str]):
        """Maneja la finalización de la conversión"""
        self.progress_bar.setVisible(False)
        
        # Habilitar controles
        self.convert_btn.setEnabled(True)
        self.add_files_btn.setEnabled(True)
        self.clear_files_btn.setEnabled(True)
        
        # Mostrar mensaje de éxito
        QMessageBox.information(
            self,
            "Conversión Completada",
            f"Se han convertido exitosamente {len(output_files)} archivo(s) a PDF."
        )
    
    def on_conversion_error(self, error_message: str):
        """Maneja errores durante la conversión"""
        QMessageBox.warning(
            self,
            "Error en la Conversión",
            error_message
        )


def run_app():
    """Ejecuta la aplicación"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Estilo moderno
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

