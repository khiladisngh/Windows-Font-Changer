"""Tests for the FontManager class."""

import platform
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from windows_font_changer.font_manager import FontManager


class TestFontManager(unittest.TestCase):
    """Test cases for FontManager class."""

    @patch("platform.system")
    def test_init_windows_platform(self, mock_platform):
        """Test initialization on Windows platform."""
        mock_platform.return_value = "Windows"
        manager = FontManager()
        assert manager._backup_file == Path.home() / ".windows_font_changer_backup.reg"

    @patch("platform.system")
    def test_init_non_windows_platform(self, mock_platform):
        """Test initialization on non-Windows platform raises error."""
        mock_platform.return_value = "Linux"
        with pytest.raises(OSError, match="This application only works on Windows"):
            FontManager()

    @patch("platform.system")
    @patch("windows_font_changer.font_manager.QFontDatabase")
    def test_get_system_fonts(self, mock_font_db, mock_platform):
        """Test getting system fonts."""
        mock_platform.return_value = "Windows"
        mock_db_instance = Mock()
        mock_db_instance.families.return_value = ["Arial", "Times New Roman", "Calibri"]
        mock_font_db.return_value = mock_db_instance
        
        manager = FontManager()
        fonts = manager.get_system_fonts()
        
        assert fonts == ["Arial", "Calibri", "Times New Roman"]  # Should be sorted
        mock_db_instance.families.assert_called_once()

    @patch("platform.system")
    @patch("winreg.OpenKey")
    def test_get_current_font_exists(self, mock_open_key, mock_platform):
        """Test getting current font when it exists."""
        mock_platform.return_value = "Windows"
        mock_key = MagicMock()
        mock_open_key.return_value.__enter__.return_value = mock_key
        
        # Mock QueryValueEx to return a font name
        with patch("winreg.QueryValueEx", return_value=("Comic Sans MS", 1)):
            manager = FontManager()
            current_font = manager.get_current_font()
            
            assert current_font == "Comic Sans MS"

    @patch("platform.system")
    @patch("winreg.OpenKey")
    def test_get_current_font_not_exists(self, mock_open_key, mock_platform):
        """Test getting current font when it doesn't exist."""
        mock_platform.return_value = "Windows"
        mock_key = MagicMock()
        mock_open_key.return_value.__enter__.return_value = mock_key
        
        # Mock QueryValueEx to raise FileNotFoundError
        with patch("winreg.QueryValueEx", side_effect=FileNotFoundError):
            manager = FontManager()
            current_font = manager.get_current_font()
            
            assert current_font is None

    @patch("platform.system")
    @patch("winreg.OpenKey")
    def test_get_current_font_error(self, mock_open_key, mock_platform):
        """Test getting current font when registry access fails."""
        mock_platform.return_value = "Windows"
        mock_open_key.side_effect = Exception("Registry error")
        
        manager = FontManager()
        current_font = manager.get_current_font()
        
        assert current_font is None

    @patch("platform.system")
    @patch("pathlib.Path.write_text")
    @patch("windows_font_changer.font_manager.FontManager.get_current_font")
    def test_backup_current_settings(self, mock_get_font, mock_write_text, mock_platform):
        """Test backing up current settings."""
        mock_platform.return_value = "Windows"
        mock_get_font.return_value = "Arial"
        
        manager = FontManager()
        manager.backup_current_settings()
        
        mock_write_text.assert_called_once()
        args = mock_write_text.call_args[0]
        backup_content = args[0]
        
        assert "Windows Registry Editor Version 5.00" in backup_content
        assert '"Segoe UI"="Arial"' in backup_content

    @patch("platform.system")
    @patch("winreg.OpenKey")
    @patch("winreg.SetValueEx")
    @patch("windows_font_changer.font_manager.FontManager.backup_current_settings")
    def test_change_font_success(self, mock_backup, mock_set_value, mock_open_key, mock_platform):
        """Test successful font change."""
        mock_platform.return_value = "Windows"
        mock_key = MagicMock()
        mock_open_key.return_value.__enter__.return_value = mock_key
        
        manager = FontManager()
        success, message = manager.change_font("Arial")
        
        assert success is True
        assert "Font changed to Arial" in message
        assert "restart Windows" in message
        mock_backup.assert_called_once()

    @patch("platform.system")
    @patch("winreg.OpenKey")
    @patch("windows_font_changer.font_manager.FontManager.backup_current_settings")
    def test_change_font_permission_error(self, mock_backup, mock_open_key, mock_platform):
        """Test font change with permission error."""
        mock_platform.return_value = "Windows"
        mock_open_key.side_effect = PermissionError
        
        manager = FontManager()
        success, message = manager.change_font("Arial")
        
        assert success is False
        assert "Permission denied" in message
        assert "administrator" in message

    @patch("platform.system")
    @patch("winreg.OpenKey")
    @patch("winreg.SetValueEx")
    @patch("winreg.DeleteValue")
    def test_restore_default_font_success(self, mock_delete_value, mock_set_value, mock_open_key, mock_platform):
        """Test successful default font restoration."""
        mock_platform.return_value = "Windows"
        mock_key = MagicMock()
        mock_open_key.return_value.__enter__.return_value = mock_key
        
        manager = FontManager()
        success, message = manager.restore_default_font()
        
        assert success is True
        assert "Default font restored" in message
        assert "restart Windows" in message

    @patch("platform.system")
    @patch("pathlib.Path.write_text")
    def test_create_reg_file(self, mock_write_text, mock_platform):
        """Test creating a .reg file."""
        mock_platform.return_value = "Windows"
        
        manager = FontManager()
        output_path = Path("test.reg")
        manager.create_reg_file("Comic Sans MS", output_path)
        
        mock_write_text.assert_called_once()
        args = mock_write_text.call_args[0]
        reg_content = args[0]
        
        assert "Windows Registry Editor Version 5.00" in reg_content
        assert '"Segoe UI"="Comic Sans MS"' in reg_content
        assert 'encoding' in mock_write_text.call_args[1]
        assert mock_write_text.call_args[1]['encoding'] == 'utf-16-le'


if __name__ == "__main__":
    unittest.main() 