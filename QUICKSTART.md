# Quick Start Guide

## For Users (Pre-built Executable)

1. Download `Windows Font Changer.exe` from the [Releases](https://github.com/yourusername/windows-font-changer/releases) page
2. Right-click the executable and select **"Run as administrator"**
3. Select your desired font from the dropdown
4. Click **"Apply Font"**
5. Restart your computer

## For Developers

### Prerequisites
- Python 3.9 or higher
- Windows 10/11

### Setup and Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/windows-font-changer.git
   cd windows-font-changer
   ```

2. **Run the setup script:**
   ```bash
   python setup.py --dev
   ```

3. **Run the application:**
   ```bash
   # Using the batch file (recommended)
   run.bat
   
   # Or using uv directly
   uv run python -m windows_font_changer
   ```

### Build Executable

Run the build script:
```bash
build.bat
```

The executable will be created in the `dist` folder.

## Important Notes

- **Administrator privileges are required** to modify system fonts
- A **system restart is required** after changing fonts
- The application automatically backs up your current settings

## Troubleshooting

### "Permission Denied" Error
Right-click and "Run as administrator"

### uv not found
Install uv with: `pip install uv`

### PySide6 Import Error
Run: `uv sync` to install dependencies 