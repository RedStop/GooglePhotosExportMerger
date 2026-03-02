# Google Photos Export Merger

The purpose of this tool is to merge the json data accompanying a Google Photos Export into the Exif properties of the images and possibly the videos.
No guarantees are made, so ensure you have a backup of your photos somewhere else before running this script.

## Quick Start

### Windows (PowerShell)
```powershell
.\setup.ps1
```

### Linux / macOS / WSL (Bash)
```bash
chmod +x setup.sh
./setup.sh
```

The setup script will:
1. Verify Python is installed
2. Create a `.venv` virtual environment
3. Install Python dependencies from `requirements.txt`
4. Check for ExifTool and attempt to download/install it if missing

## Manual Setup

If you prefer to set up manually or the setup script doesn't work for your environment:

1. **Python 3.10+** — install from [python.org](https://www.python.org/)
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   # Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # Linux/macOS:
   source .venv/bin/activate
   ```
3. **Install Python packages:**
   ```bash
   pip install -r requirements.txt
   ```
4. **ExifTool 12.45** — download from [exiftool.org](https://exiftool.org/):
   - Place `exiftool.exe` in the project folder, **or**
   - Install it to a directory on your system PATH

## Requirements

- Python 3.10.11
- [ExifTool](https://exiftool.org/) 12.45 (should be available in the system PATH) — I used the Windows executable.
- Only tested on Windows.

## Python Packages

- PyExifTool 0.5.6 (`pip install PyExifTool`)
- sortedcontainers 2.4.0 (`pip install sortedcontainers`)
