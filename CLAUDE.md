# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Google Photos Export Merger — a Python utility that merges JSON metadata from Google Photos Takeout exports into image/video EXIF properties using ExifTool. Windows-only.

## Requirements

- Python 3.10.11 (virtual environment in `.venv/`)
- ExifTool 12.45 (must be in system PATH)
- PyExifTool 0.5.6, sortedcontainers 2.4.0

## Running

```bash
# Analyse JSON metadata structure across a directory tree
python JsonKeyExtractor.py <input_directory> [output_directory]

# Merge metadata into media files
python GooglePhotosExportMerger.py <input_dir> <output_dir> [--dry-run]

# Run tests
python -m pytest TestMerger.py
```

## Testing

`TestMerger.py` is a comprehensive `unittest`-based test suite with 100+ test cases. It runs as a single-pass integration test: `setUpClass` builds an input tree with programmatically generated binary test files (JPEG, PNG, GIF, CR2, HEIC, MP4, MOV, AVI, MKV, WebM), runs the merger once, then individual tests assert on the output. Test categories include GPS, timezones, descriptions, file types, orphan files, XMP sidecars, duplicates, bracket notation, file timestamps, video UTC time, special filenames, metadata preservation, and stats verification.

## Architecture

Five modules with clear separation of concerns:

1. **AbstractMediaMerger.py** — Abstract base class defining the merge pipeline. Defines `WriteStrategy` enum (DIRECT, PARTIAL_WITH_SIDECAR, VIDEO_WITH_SIDECAR), `MediaFileInfo` dataclass, and `MergeStats` dataclass. Implements the 9-step merge pipeline, GPS resolution, duplicate filename resolution, dry-run logging, and summary reporting.

2. **GooglePhotosExportMerger.py** — Concrete implementation of AbstractMediaMerger and the CLI entry point. Builds ExifTool parameters for dates, descriptions, GPS, and timezones. Has a `blocked_descriptions` list in `__main__` for filtering unwanted descriptions.

3. **JsonFileIdentifier.py** — Matches JSON metadata files to their corresponding media files. Uses `SortedSet` for O(log n + k) prefix-based lookups. Handles Google's bracket notation (e.g., `filename(2).jpg`) and case-insensitive extension matching.

4. **JsonKeyExtractor.py** — Analysis entry point. Scans a directory tree once, groups files by directory, extracts JSON structure (2-level depth), and generates analysis output (combined_structure.json, individual_files.json, file_types.json, plus conditional error/conflict files).

5. **TestMerger.py** — Integration test suite (see Testing section above).

**Data flow:** JsonKeyExtractor scans directories → JsonFileIdentifier matches JSON-to-media files → GooglePhotosExportMerger writes metadata to EXIF.

## Key Design Details

- Write strategies: DIRECT (jpg, tiff, dng, cr2, heic), PARTIAL_WITH_SIDECAR (png, gif), VIDEO_WITH_SIDECAR (avi, mkv, mov, mp4, m4v, webm)
- Metadata written: dates, descriptions, GPS coordinates (latitude, longitude, altitude), timezone offsets
- File creation and modified times are updated to match the photo/video date
- Orphan files (no matching JSON) are still copied; dates resolved from existing EXIF or filesystem creation date
- Duplicate output filenames resolved by appending `_2`, `_3`, etc.
- `.gitignore` excludes all media and JSON files — only Python source is tracked
