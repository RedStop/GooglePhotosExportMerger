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
# Analyze JSON metadata structure across a directory tree
python JsonKeyExtractor.py [directory_path] [output_dir]

# Merge metadata into image EXIF (library usage, no CLI entry point)
python JsonPropertyMerger.py
```

There are no automated tests or a test framework. Testing is manual using sample data in `TestFileTypes/`.

## Architecture

Three modules with clear separation of concerns:

1. **JsonFileIdentifier.py** — Matches JSON metadata files to their corresponding media files. Uses `SortedSet` for O(log n + k) prefix-based lookups. Handles Google's bracket notation (e.g., `filename(2).jpg`) and case-insensitive extension matching.

2. **JsonKeyExtractor.py** — Primary analysis entry point. Scans a directory tree once, groups files by directory, extracts JSON structure (2-level depth), and generates analysis output in `output/` (combined_structure.json, individual_files.json, file_types.json, unreferenced_files.json, plus conditional error/conflict files).

3. **JsonPropertyMerger.py** — Writes JSON metadata into image/video EXIF tags via PyExifTool. Maps Google's `photoTakenTime.timestamp` to EXIF date fields and `description` to `ImageDescription`. Supports conflict resolution modes: `OVERWRITE`, `KEEP`, `APPEND`, `PROMPT_USER` (via `TagUpdateMode` enum).

**Data flow:** JsonKeyExtractor scans directories → JsonFileIdentifier matches JSON-to-media files → JsonPropertyMerger writes metadata to EXIF.

## Key Design Details

- `jsonFile` parameter in JsonPropertyMerger can be a file path string OR a pre-parsed dict
- `imageFile` must be an explicit valid file path
- GPS metadata handling is a TODO
- `.gitignore` excludes all media and JSON files — only Python source is tracked
