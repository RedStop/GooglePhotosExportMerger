import json
import sys
from pathlib import Path
from collections import defaultdict

def getNestedKeys(data, maxDepth=2, currentDepth=0):
    """
    Extract keys up to a specified depth from a JSON structure.
    Returns a dictionary with the structure of keys.
    """
    if currentDepth >= maxDepth:
        return None
    
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            if currentDepth < maxDepth - 1:
                nested = getNestedKeys(value, maxDepth, currentDepth + 1)
                result[key] = nested if nested else type(value).__name__
            else:
                result[key] = type(value).__name__
        return result
    elif isinstance(data, list) and data:
        # For lists, analyze the first item to understand structure
        return [getNestedKeys(data[0], maxDepth, currentDepth)]
    else:
        return type(data).__name__

def mergeStructures(struct1, struct2):
    """
    Merge two structure dictionaries, combining all keys from both.
    """
    if not isinstance(struct1, dict) or not isinstance(struct2, dict):
        # If either is not a dict, prefer dict over other types, otherwise return struct2
        if isinstance(struct1, dict):
            return struct1
        elif isinstance(struct2, dict):
            return struct2
        else:
            return struct2
    
    result = struct1.copy()
    
    for key, value in struct2.items():
        if key in result:
            # If both have the key, merge their values recursively
            if isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = mergeStructures(result[key], value)
            elif isinstance(result[key], list) and isinstance(value, list):
                # For lists, merge the structure of their first elements
                if result[key] and value:
                    result[key] = [mergeStructures(result[key][0], value[0])]
                elif value:
                    result[key] = value
            # Otherwise, keep existing value (could also choose to keep the new one)
        else:
            # Key only exists in struct2, add it
            result[key] = value
    
    return result

def processJsonFiles(directoryPath, outputFile='extracted_keys.json'):
    """
    Process all JSON files in directory and subdirectories.
    Extract first and second level keys and save to a new JSON file.
    """
    directory = Path(directoryPath)
    
    if not directory.exists():
        print(f"Error: Directory '{directoryPath}' does not exist")
        return
    
    # Dictionary to store all unique key structures found
    allStructures = {}
    combinedStructure = {}
    filesProcessed = 0
    filesWithErrors = []
    
    # Find all JSON files recursively
    jsonFiles = list(directory.rglob('*.json'))
    
    if not jsonFiles:
        print(f"No JSON files found in '{directoryPath}'")
        return
    
    print(f"Found {len(jsonFiles)} JSON file(s) to process...")
    
    for jsonFile in jsonFiles:
        try:
            with open(jsonFile, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Get the key structure (first and second level)
                structure = getNestedKeys(data, maxDepth=2)
                
                # Store with relative path as key
                relativePath = jsonFile.relative_to(directory)
                allStructures[str(relativePath)] = structure
                
                # Merge into combined structure
                combinedStructure = mergeStructures(combinedStructure, structure)
                
                filesProcessed += 1
                
        except json.JSONDecodeError as e:
            filesWithErrors.append((str(jsonFile), f"JSON decode error: {e}"))
        except Exception as e:
            filesWithErrors.append((str(jsonFile), f"Error: {e}"))
    
    # Create final output with both individual and combined structures
    outputData = {
        "combined_structure": combinedStructure,
        "individual_files": allStructures
    }
    
    # Save the results
    outputPath = Path(outputFile)
    with open(outputPath, 'w', encoding='utf-8') as f:
        json.dump(outputData, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print(f"\nProcessing complete!")
    print(f"Files processed successfully: {filesProcessed}")
    print(f"Files with errors: {len(filesWithErrors)}")
    
    if filesWithErrors:
        print("\nErrors encountered:")
        for filePath, error in filesWithErrors:
            print(f"  - {filePath}: {error}")
    
    print(f"\nOutput saved to: {outputPath.absolute()}")
    print(f"\nThe output contains:")
    print(f"  - 'combined_structure': Merged structure from all files")
    print(f"  - 'individual_files': Structure for each file")

if __name__ == "__main__":
    # Specify the directory to scan
    directoryToScan = "."  # Current directory, use arg to change
    if len(sys.argv) > 1:
        directoryToScan = sys.argv[1]
    
    # Optional: specify custom output file name
    outputFilename = "extracted_keys.json"
    
    processJsonFiles(directoryToScan, outputFilename)