# Windows Font Changer

[![CI](https://github.com/yourusername/windows-font-changer/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/windows-font-changer/actions/workflows/ci.yml)
[![Build](https://github.com/yourusername/windows-font-changer/actions/workflows/build.yml/badge.svg)](https://github.com/yourusername/windows-font-changer/actions/workflows/build.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern, user-friendly application to change the default system font on Windows 11 with a clean Qt interface.

![Windows Font Changer Screenshot](screenshot.png)

## Features

- 🎨 **Easy Font Selection**: Browse and preview all system fonts
- 👁️ **Live Preview**: See how fonts look before applying
- 🔄 **One-Click Restore**: Easily restore the default Windows font
- 📁 **Export to .REG**: Create registry files for manual installation
- 🛡️ **Safe**: Automatic backup of current settings before changes
- 🎯 **Modern UI**: Clean and intuitive interface built with Qt

## Requirements

- Windows 10/11
- Administrator privileges (for registry modifications)
- Python 3.9+ (for development)

## Installation

### Option 1: Download Pre-built Executable

Download the latest release from the [Releases](https://github.com/yourusername/windows-font-changer/releases) page.

### Option 2: Build from Source

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/windows-font-changer.git
   cd windows-font-changer
   ```

2. **Install uv (if not already installed):**
   ```bash
   pip install uv
   ```

3. **Install dependencies:**
   ```bash
   uv sync
   ```

4. **Run the application:**
   ```bash
   uv run python -m windows_font_changer
   ```

## Usage

1. **Run as Administrator**: Right-click the application and select "Run as administrator"
2. **Select a Font**: Choose your desired font from the dropdown menu
3. **Preview**: The preview text will update to show the selected font
4. **Apply Changes**: Click "Apply Font" to change the system font
5. **Restart Windows**: Restart your computer for changes to take effect

### Restoring Default Font

Click the "Restore Default" button to revert to the original Windows font (Segoe UI).

### Exporting Registry File

Use the "Export .REG" button to create a registry file that can be run manually or shared with others.

## Development

### Setting Up Development Environment

1. **Install development dependencies:**
   ```bash
   uv sync --dev
   ```

2. **Install pre-commit hooks:**
   ```bash
   uv run pre-commit install
   ```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=windows_font_changer

# Run specific test file
uv run pytest tests/test_font_manager.py
```

### Code Quality

```bash
# Run linting
uv run ruff check .

# Format code
uv run ruff format .

# Type checking
uv run mypy windows_font_changer
```

### Building Executable

```bash
uv run pyinstaller --name "Windows Font Changer" \
  --onefile \
  --windowed \
  --add-data "windows_font_changer;windows_font_changer" \
  windows_font_changer/__main__.py
```

## Project Structure

```
windows-font-changer/
├── windows_font_changer/
│   ├── __init__.py
│   ├── __main__.py
│   ├── font_manager.py    # Core font management logic
│   └── ui.py              # Qt UI implementation
├── tests/
│   ├── test_font_manager.py
│   └── test_ui.py
├── .github/
│   └── workflows/
│       ├── ci.yml         # Testing and linting
│       └── build.yml      # Build executables
├── pyproject.toml         # Project configuration
├── .pre-commit-config.yaml
└── README.md
```

## How It Works

The application modifies Windows registry entries to change the system font:

1. **Font Substitution**: Creates a mapping from "Segoe UI" to your chosen font
2. **Registry Keys Modified**:
   - `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts`
   - `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\FontSubstitutes`

## Safety

- Automatic backup of current settings before any changes
- Backup file saved to: `~/.windows_font_changer_backup.reg`
- Can export changes to .REG file for manual review before applying

## Troubleshooting

### "Permission Denied" Error
- Make sure to run the application as Administrator
- Right-click → "Run as administrator"

### Changes Not Taking Effect
- A system restart is required after changing fonts
- Some applications may cache fonts and require their own restart

### Font Not Available
- Ensure the font is properly installed in Windows
- Check in Settings → Personalization → Fonts

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [PySide6](https://doc.qt.io/qtforpython/) for the UI
- Uses [uv](https://github.com/astral-sh/uv) for Python package management
- Formatted with [Ruff](https://github.com/astral-sh/ruff)

## Disclaimer

This application modifies Windows registry settings. While it includes safety features and backups, use at your own risk. Always ensure you have system backups before making system-level changes. 