"""Modern Qt UI for Windows Font Changer."""

from pathlib import Path
from typing import Optional

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QIcon, QPalette, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .font_manager import FontManager


class FontChangeWorker(QThread):
    """Worker thread for font change operations."""
    
    finished = Signal(bool, str)
    
    def __init__(self, font_manager: FontManager, font_name: str, restore: bool = False):
        super().__init__()
        self.font_manager = font_manager
        self.font_name = font_name
        self.restore = restore
    
    def run(self):
        """Run the font change operation."""
        if self.restore:
            success, message = self.font_manager.restore_default_font()
        else:
            success, message = self.font_manager.change_font(self.font_name)
        self.finished.emit(success, message)


class FontChangerUI(QMainWindow):
    """Main UI window for Windows Font Changer."""
    
    def __init__(self):
        super().__init__()
        self.font_manager = FontManager()
        self.init_ui()
        self.load_fonts()
        self.update_current_font_label()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Windows Font Changer")
        self.setFixedSize(600, 400)
        
        # Set modern style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #333333;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            QComboBox {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                background-color: white;
                min-height: 20px;
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #333333;
                margin-right: 5px;
            }
        """)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title_label = QLabel("Windows Font Changer")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #0078d4;
            margin-bottom: 10px;
        """)
        main_layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel("Change your Windows system font easily")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet("""
            font-size: 16px;
            color: #666666;
            margin-bottom: 20px;
        """)
        main_layout.addWidget(desc_label)
        
        # Current font label
        self.current_font_label = QLabel()
        self.current_font_label.setAlignment(Qt.AlignCenter)
        self.current_font_label.setStyleSheet("""
            font-size: 14px;
            color: #333333;
            background-color: #e0e0e0;
            padding: 10px;
            border-radius: 4px;
        """)
        main_layout.addWidget(self.current_font_label)
        
        # Font selection
        font_layout = QHBoxLayout()
        font_layout.setSpacing(10)
        
        font_label = QLabel("Select Font:")
        font_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        font_layout.addWidget(font_label)
        
        self.font_combo = QComboBox()
        self.font_combo.setEditable(True)
        self.font_combo.setInsertPolicy(QComboBox.NoInsert)
        self.font_combo.currentTextChanged.connect(self.preview_font)
        font_layout.addWidget(self.font_combo, 1)
        
        main_layout.addLayout(font_layout)
        
        # Preview label
        self.preview_label = QLabel("The quick brown fox jumps over the lazy dog")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet("""
            font-size: 18px;
            padding: 20px;
            background-color: white;
            border: 1px solid #cccccc;
            border-radius: 4px;
            min-height: 40px;
        """)
        main_layout.addWidget(self.preview_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.apply_button = QPushButton("Apply Font")
        self.apply_button.clicked.connect(self.apply_font)
        button_layout.addWidget(self.apply_button)
        
        self.restore_button = QPushButton("Restore Default")
        self.restore_button.clicked.connect(self.restore_default)
        self.restore_button.setStyleSheet("""
            QPushButton {
                background-color: #107c10;
            }
            QPushButton:hover {
                background-color: #0e6e0e;
            }
            QPushButton:pressed {
                background-color: #0c5d0c;
            }
        """)
        button_layout.addWidget(self.restore_button)
        
        self.export_button = QPushButton("Export .REG")
        self.export_button.clicked.connect(self.export_reg_file)
        self.export_button.setStyleSheet("""
            QPushButton {
                background-color: #5c2d91;
            }
            QPushButton:hover {
                background-color: #4a2375;
            }
            QPushButton:pressed {
                background-color: #3a1b5a;
            }
        """)
        button_layout.addWidget(self.export_button)
        
        main_layout.addLayout(button_layout)
        
        # Warning label
        warning_label = QLabel(
            "⚠️ Administrator privileges required. Windows restart needed for changes to take effect."
        )
        warning_label.setAlignment(Qt.AlignCenter)
        warning_label.setStyleSheet("""
            font-size: 12px;
            color: #d83b01;
            background-color: #fff4ce;
            padding: 10px;
            border-radius: 4px;
            margin-top: 10px;
        """)
        main_layout.addWidget(warning_label)
        
        main_layout.addStretch()
        
        central_widget.setLayout(main_layout)
    
    def load_fonts(self):
        """Load available system fonts into the combo box."""
        fonts = self.font_manager.get_system_fonts()
        self.font_combo.addItems(fonts)
        
        # Set current font if available
        current_font = self.font_manager.get_current_font()
        if current_font and current_font in fonts:
            self.font_combo.setCurrentText(current_font)
    
    def update_current_font_label(self):
        """Update the label showing the current system font."""
        current_font = self.font_manager.get_current_font()
        if current_font:
            self.current_font_label.setText(f"Current system font: {current_font}")
        else:
            self.current_font_label.setText("Current system font: Segoe UI (Default)")
    
    def preview_font(self, font_name: str):
        """Preview the selected font."""
        if font_name:
            font = QFont(font_name, 18)
            self.preview_label.setFont(font)
    
    def apply_font(self):
        """Apply the selected font."""
        font_name = self.font_combo.currentText()
        if not font_name:
            QMessageBox.warning(self, "Warning", "Please select a font.")
            return
        
        reply = QMessageBox.question(
            self,
            "Confirm Font Change",
            f"Are you sure you want to change the system font to '{font_name}'?\n\n"
            "This will require administrator privileges and a system restart.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.apply_button.setEnabled(False)
            self.restore_button.setEnabled(False)
            
            self.worker = FontChangeWorker(self.font_manager, font_name)
            self.worker.finished.connect(self.on_font_change_finished)
            self.worker.start()
    
    def restore_default(self):
        """Restore the default system font."""
        reply = QMessageBox.question(
            self,
            "Confirm Restore Default",
            "Are you sure you want to restore the default system font?\n\n"
            "This will require administrator privileges and a system restart.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.apply_button.setEnabled(False)
            self.restore_button.setEnabled(False)
            
            self.worker = FontChangeWorker(self.font_manager, "", restore=True)
            self.worker.finished.connect(self.on_font_change_finished)
            self.worker.start()
    
    def on_font_change_finished(self, success: bool, message: str):
        """Handle font change completion."""
        self.apply_button.setEnabled(True)
        self.restore_button.setEnabled(True)
        
        if success:
            QMessageBox.information(self, "Success", message)
            self.update_current_font_label()
        else:
            QMessageBox.critical(self, "Error", message)
    
    def export_reg_file(self):
        """Export a .reg file for manual font change."""
        font_name = self.font_combo.currentText()
        if not font_name:
            QMessageBox.warning(self, "Warning", "Please select a font.")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Registry File",
            f"change_font_to_{font_name.replace(' ', '_')}.reg",
            "Registry Files (*.reg)"
        )
        
        if file_path:
            try:
                self.font_manager.create_reg_file(font_name, Path(file_path))
                QMessageBox.information(
                    self,
                    "Success",
                    f"Registry file saved to:\n{file_path}\n\n"
                    "You can run this file manually with administrator privileges."
                )
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create registry file: {str(e)}")


def main():
    """Main entry point for the application."""
    app = QApplication([])
    app.setStyle("Fusion")
    
    # Set application metadata
    app.setApplicationName("Windows Font Changer")
    app.setOrganizationName("FontChanger")
    
    window = FontChangerUI()
    window.show()
    
    return app.exec() 