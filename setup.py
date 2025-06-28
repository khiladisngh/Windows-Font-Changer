#!/usr/bin/env python
"""Setup script for Windows Font Changer."""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    print(f"Running: {' '.join(cmd)}")
    return subprocess.run(cmd, check=check, shell=True)


def main():
    """Main setup function."""
    print("Windows Font Changer Setup")
    print("=" * 50)

    # Check if uv is installed
    try:
        run_command(["uv", "--version"])
        print("✓ uv is installed")
    except subprocess.CalledProcessError:
        print("✗ uv is not installed")
        print("Installing uv...")
        run_command([sys.executable, "-m", "pip", "install", "uv"])

    # Install dependencies
    print("\nInstalling dependencies...")
    run_command(["uv", "sync"])

    # Install dev dependencies if requested
    if "--dev" in sys.argv:
        print("\nInstalling development dependencies...")
        run_command(["uv", "sync", "--dev"])

        # Install pre-commit hooks
        print("\nInstalling pre-commit hooks...")
        run_command(["uv", "run", "pre-commit", "install"])

    print("\n✓ Setup complete!")
    print("\nTo run the application:")
    print("  uv run python -m windows_font_changer")
    print(
        "\nNote: The application requires administrator privileges to modify system fonts."
    )


if __name__ == "__main__":
    main()
