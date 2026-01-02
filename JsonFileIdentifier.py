import os
import json
import re
from pathlib import Path
from typing import Tuple, Optional, List, Dict, Any


def JsonFileFinder(
    json_path: str,
    json_data: Optional[Dict[str, Any]] = None,
    all_files: Optional[List[Path]] = None
) -> Tuple[Optional[str], Optional[str]]:
    """
    Find a file matching a .json file and read its new name from the 'title' field.
    
    Args:
        json_path: Path to the .json file
        json_data: Optional pre-loaded JSON data (to avoid re-parsing)
        all_files: Optional list of all files in directory (to avoid re-scanning)
        
    Returns:
        Tuple of (matching_filename, new_title):
        - matching_filename: The filename (not full path) of the matching file, or None if not found
        - new_title: The title read from the json file, or None if error reading json
    """
    try:
        json_path_obj = Path(json_path)
        
        # If json_data is provided, we assume the file exists and use the data
        # Otherwise, check if file exists and read it
        if json_data is None:
            if not json_path_obj.exists() or not json_path_obj.is_file():
                return (None, None)
            
            try:
                with open(json_path_obj, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
            except (json.JSONDecodeError, IOError, KeyError, UnicodeDecodeError):
                return (None, None)
        
        # Extract title from json data
        new_title = json_data.get('title')
        if new_title is None:
            return (None, None)
        
        # Get the directory and json filename
        directory = json_path_obj.parent
        json_filename = json_path_obj.name
        
        # Strategy 1: Try exact match (remove .json extension)
        if json_filename.endswith('.json'):
            base_name = json_filename[:-5]  # Remove '.json'
            candidate_path = directory / base_name
            
            # If all_files provided, check in the list; otherwise check filesystem
            if all_files is not None:
                if candidate_path in all_files:
                    return (base_name, new_title)
            else:
                if candidate_path.exists() and candidate_path.is_file():
                    return (base_name, new_title)
        
        # Strategy 2: Handle bracket notation and truncated filenames
        # Pattern: filename(N).json or truncated versions
        bracket_match = re.search(r'\((\d+)\)\.json$', json_filename)
        
        if bracket_match:
            # Has bracket notation like (2).json
            bracket_num = bracket_match.group(1)
            # Remove (N).json to get base
            base_without_bracket = json_filename[:bracket_match.start()]
            
            # Get list of files to check
            if all_files is not None:
                # Filter to files in the same directory
                files_in_dir = [f for f in all_files if f.parent == directory and f.is_file()]
            else:
                try:
                    files_in_dir = list(directory.iterdir())
                    files_in_dir = [f for f in files_in_dir if f.is_file()]
                except OSError:
                    return (None, new_title)
            
            for file in files_in_dir:
                if file.name != json_filename:
                    # Check if file matches pattern: base*(N).ext
                    file_pattern = re.search(r'^(.+?)\((\d+)\)(\.[^.]+)$', file.name)
                    if file_pattern:
                        file_base = file_pattern.group(1)
                        file_bracket = file_pattern.group(2)
                        
                        # Check if bracket number matches and base is a prefix match
                        if file_bracket == bracket_num and file_base.startswith(base_without_bracket[:len(file_base)]):
                            return (file.name, new_title)
        
        # Strategy 3: Handle truncated filenames without brackets
        # Remove .json and try to find files with matching prefix
        if json_filename.endswith('.json'):
            base_without_json = json_filename[:-5]
            
            # Get list of files to check
            if all_files is not None:
                # Filter to files in the same directory
                files_in_dir = [f for f in all_files if f.parent == directory and f.is_file()]
            else:
                try:
                    files_in_dir = list(directory.iterdir())
                    files_in_dir = [f for f in files_in_dir if f.is_file()]
                except OSError:
                    return (None, new_title)
            
            for file in files_in_dir:
                if file.name != json_filename:
                    # Check if removing the file's extension gives us something that starts with our base
                    file_stem = file.stem  # filename without extension
                    
                    # Check if the json base could be a truncated version of this file
                    # The json base should be a prefix of: filestem + possible partial extension
                    full_name_parts = file.name.rsplit('.', 1)
                    if len(full_name_parts) == 2:
                        stem, ext = full_name_parts
                        # Check all possible truncations
                        for i in range(len(ext) + 1):
                            potential_truncated = stem + ('.' + ext[:i] if i > 0 else '')
                            if potential_truncated == base_without_json:
                                return (file.name, new_title)
        
        # No matching file found
        return (None, new_title)
        
    except Exception:
        # Catch any unexpected errors
        return (None, None)