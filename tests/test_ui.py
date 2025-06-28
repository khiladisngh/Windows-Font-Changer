"""Tests for the UI components."""

import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMessageBox

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from windows_font_changer.ui import FontChangerUI, FontChangeWorker


@pytest.fixture
def qapp():
    """Create QApplication for tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    app.quit()


@pytest.fixture
def window(qapp, monkeypatch):
    """Create FontChangerUI window for tests."""
    # Mock platform check
    monkeypatch.setattr("platform.system", lambda: "Windows")
    
    # Mock FontManager methods
    with patch("windows_font_changer.font_manager.FontManager") as mock_fm:
        mock_instance = Mock()
        mock_instance.get_system_fonts.return_value = ["Arial", "Calibri", "Times New Roman"]
        mock_instance.get_current_font.return_value = "Arial"
        mock_fm.return_value = mock_instance
        
        window = FontChangerUI()
        yield window
        window.close()


class TestFontChangerUI:
    """Test cases for FontChangerUI class."""

    def test_window_initialization(self, window):
        """Test window is properly initialized."""
        assert window.windowTitle() == "Windows Font Changer"
        assert window.width() == 600
        assert window.height() == 400

    def test_font_loading(self, window):
        """Test fonts are loaded into combo box."""
        assert window.font_combo.count() == 3
        assert window.font_combo.itemText(0) == "Arial"
        assert window.font_combo.itemText(1) == "Calibri"
        assert window.font_combo.itemText(2) == "Times New Roman"

    def test_current_font_display(self, window):
        """Test current font is displayed correctly."""
        assert "Arial" in window.current_font_label.text()

    def test_font_preview(self, window, qtbot):
        """Test font preview updates when selection changes."""
        # Change font selection
        window.font_combo.setCurrentText("Times New Roman")
        
        # Check preview label font
        font = window.preview_label.font()
        assert font.family() == "Times New Roman"

    def test_apply_font_no_selection(self, window, qtbot, monkeypatch):
        """Test apply font with no selection shows warning."""
        window.font_combo.setCurrentText("")
        
        # Mock QMessageBox
        mock_warning = Mock()
        monkeypatch.setattr(QMessageBox, "warning", mock_warning)
        
        # Click apply button
        window.apply_button.click()
        
        # Check warning was shown
        mock_warning.assert_called_once()
        args = mock_warning.call_args[0]
        assert "Please select a font" in args[2]

    def test_apply_font_user_cancels(self, window, qtbot, monkeypatch):
        """Test apply font when user cancels confirmation."""
        window.font_combo.setCurrentText("Arial")
        
        # Mock QMessageBox to return No
        monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.No)
        
        # Click apply button
        window.apply_button.click()
        
        # Buttons should still be enabled
        assert window.apply_button.isEnabled()
        assert window.restore_button.isEnabled()

    def test_export_reg_file_no_selection(self, window, qtbot, monkeypatch):
        """Test export reg file with no selection shows warning."""
        window.font_combo.setCurrentText("")
        
        # Mock QMessageBox
        mock_warning = Mock()
        monkeypatch.setattr(QMessageBox, "warning", mock_warning)
        
        # Click export button
        window.export_button.click()
        
        # Check warning was shown
        mock_warning.assert_called_once()


class TestFontChangeWorker:
    """Test cases for FontChangeWorker class."""

    @patch("platform.system", return_value="Windows")
    def test_worker_change_font(self, mock_platform):
        """Test worker thread for font change."""
        mock_manager = Mock()
        mock_manager.change_font.return_value = (True, "Success")
        
        worker = FontChangeWorker(mock_manager, "Arial", restore=False)
        worker.run()
        
        mock_manager.change_font.assert_called_once_with("Arial")

    @patch("platform.system", return_value="Windows")
    def test_worker_restore_font(self, mock_platform):
        """Test worker thread for font restoration."""
        mock_manager = Mock()
        mock_manager.restore_default_font.return_value = (True, "Success")
        
        worker = FontChangeWorker(mock_manager, "", restore=True)
        worker.run()
        
        mock_manager.restore_default_font.assert_called_once() 