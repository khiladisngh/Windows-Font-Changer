"""Font management functionality for Windows registry operations."""

import os
import platform
import winreg
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from PySide6.QtGui import QFontDatabase


class FontManager:
    """Manages Windows system font changes through registry modifications."""

    FONTS_KEY_PATH = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
    FONT_SUBSTITUTES_KEY_PATH = (
        r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\FontSubstitutes"
    )

    SEGOE_UI_FONTS = {
        "Segoe UI (TrueType)": "segoeui.ttf",
        "Segoe UI Bold (TrueType)": "segoeuib.ttf",
        "Segoe UI Bold Italic (TrueType)": "segoeuiz.ttf",
        "Segoe UI Italic (TrueType)": "segoeuii.ttf",
        "Segoe UI Light (TrueType)": "segoeuil.ttf",
        "Segoe UI Semibold (TrueType)": "seguisb.ttf",
        "Segoe UI Symbol (TrueType)": "seguisym.ttf",
        "Segoe UI Black (TrueType)": "seguibl.ttf",
        "Segoe UI Black Italic (TrueType)": "seguibli.ttf",
        "Segoe UI Emoji (TrueType)": "seguiemj.ttf",
        "Segoe UI Historic (TrueType)": "seguihis.ttf",
        "Segoe UI Light Italic (TrueType)": "seguili.ttf",
        "Segoe UI Semibold Italic (TrueType)": "seguisbi.ttf",
        "Segoe UI Semilight (TrueType)": "segoeuisl.ttf",
        "Segoe UI Semilight Italic (TrueType)": "seguisli.ttf",
        "Segoe MDL2 Assets (TrueType)": "segmdl2.ttf",
        "Segoe Print (TrueType)": "segoepr.ttf",
        "Segoe Print Bold (TrueType)": "segoeprb.ttf",
        "Segoe Script (TrueType)": "segoesc.ttf",
        "Segoe Script Bold (TrueType)": "segoescb.ttf",
    }

    def __init__(self):
        """Initialize the font manager."""
        self._check_windows_platform()
        self._backup_file = Path.home() / ".windows_font_changer_backup.reg"

    def _check_windows_platform(self) -> None:
        """Check if running on Windows platform."""
        if platform.system() != "Windows":
            raise OSError("This application only works on Windows.")

    def get_system_fonts(self) -> List[str]:
        """Get list of all available system fonts.

        Returns:
            List of font family names available on the system.
        """
        font_db = QFontDatabase()
        return sorted(font_db.families())

    def get_current_font(self) -> Optional[str]:
        """Get the current system font.

        Returns:
            Current font name or None if default.
        """
        try:
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                self.FONT_SUBSTITUTES_KEY_PATH,
                0,
                winreg.KEY_READ,
            ) as key:
                try:
                    value, _ = winreg.QueryValueEx(key, "Segoe UI")
                    return value
                except FileNotFoundError:
                    return None
        except Exception:
            return None

    def backup_current_settings(self) -> None:
        """Backup current font settings to a file."""
        backup_content = ["Windows Registry Editor Version 5.00", ""]

        # Backup Fonts key
        backup_content.append(f"[HKEY_LOCAL_MACHINE\\{self.FONTS_KEY_PATH}]")
        try:
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, self.FONTS_KEY_PATH, 0, winreg.KEY_READ
            ) as key:
                for name, file in self.SEGOE_UI_FONTS.items():
                    backup_content.append(f'"{name}"="{file}"')
        except Exception:
            pass

        backup_content.append("")

        # Backup FontSubstitutes key
        backup_content.append(f"[HKEY_LOCAL_MACHINE\\{self.FONT_SUBSTITUTES_KEY_PATH}]")
        current_font = self.get_current_font()
        if current_font:
            backup_content.append(f'"Segoe UI"="{current_font}"')
        else:
            backup_content.append('"Segoe UI"=-')

        # Write backup file
        self._backup_file.write_text("\n".join(backup_content), encoding="utf-16-le")

    def change_font(self, font_name: str) -> Tuple[bool, str]:
        """Change the system font.

        Args:
            font_name: Name of the font to set as system font.

        Returns:
            Tuple of (success, message).
        """
        try:
            # First, backup current settings
            self.backup_current_settings()

            # Clear Segoe UI font mappings
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, self.FONTS_KEY_PATH, 0, winreg.KEY_SET_VALUE
            ) as key:
                for font_entry in self.SEGOE_UI_FONTS:
                    if "Segoe UI" in font_entry:
                        winreg.SetValueEx(key, font_entry, 0, winreg.REG_SZ, "")

            # Set font substitution
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                self.FONT_SUBSTITUTES_KEY_PATH,
                0,
                winreg.KEY_SET_VALUE,
            ) as key:
                winreg.SetValueEx(key, "Segoe UI", 0, winreg.REG_SZ, font_name)

            return (
                True,
                f"Font changed to {font_name}. Please restart Windows to apply changes.",
            )
        except PermissionError:
            return False, "Permission denied. Please run as administrator."
        except Exception as e:
            return False, f"Error changing font: {str(e)}"

    def restore_default_font(self) -> Tuple[bool, str]:
        """Restore the default system font.

        Returns:
            Tuple of (success, message).
        """
        try:
            # Restore Segoe UI font mappings
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, self.FONTS_KEY_PATH, 0, winreg.KEY_SET_VALUE
            ) as key:
                for font_entry, font_file in self.SEGOE_UI_FONTS.items():
                    winreg.SetValueEx(key, font_entry, 0, winreg.REG_SZ, font_file)

            # Remove font substitution
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                self.FONT_SUBSTITUTES_KEY_PATH,
                0,
                winreg.KEY_SET_VALUE,
            ) as key:
                try:
                    winreg.DeleteValue(key, "Segoe UI")
                except FileNotFoundError:
                    pass  # Value doesn't exist, which is fine

            return (
                True,
                "Default font restored. Please restart Windows to apply changes.",
            )
        except PermissionError:
            return False, "Permission denied. Please run as administrator."
        except Exception as e:
            return False, f"Error restoring default font: {str(e)}"

    def create_reg_file(self, font_name: str, output_path: Path) -> None:
        """Create a .reg file for manual font change.

        Args:
            font_name: Name of the font to set.
            output_path: Path where to save the .reg file.
        """
        reg_content = [
            "Windows Registry Editor Version 5.00",
            "",
            f"[HKEY_LOCAL_MACHINE\\{self.FONTS_KEY_PATH}]",
        ]

        # Add entries to clear Segoe UI fonts
        for font_entry in self.SEGOE_UI_FONTS:
            if "Segoe UI" in font_entry:
                reg_content.append(f'"{font_entry}"=""')

        reg_content.extend(
            [
                "",
                f"[HKEY_LOCAL_MACHINE\\{self.FONT_SUBSTITUTES_KEY_PATH}]",
                f'"Segoe UI"="{font_name}"',
            ]
        )

        output_path.write_text("\n".join(reg_content), encoding="utf-16-le")
