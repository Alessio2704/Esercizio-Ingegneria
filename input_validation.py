import os
from classes import Center

def validate_coordinate(coordinate, coord_type):
    """Validates a latitude or longitude coordinate."""
    try:
        coord = float(coordinate)
        if coord_type == 'latitude':
            if not (-90 <= coord <= 90):
                raise ValueError("Latitude must be between -90 and 90 degrees.")
        elif coord_type == 'longitude':
            if not (-180 <= coord <= 180):
                raise ValueError("Longitude must be between -180 and 180 degrees.")
        return coord
    except ValueError:
        raise ValueError(f"Invalid {coord_type} value: {coordinate}")

def validate_filepath(filepath, extension=None):
    """Validates if a file exists and optionally checks the extension."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    if extension:
        if not filepath.lower().endswith(extension.lower()):
            raise ValueError(f"File must have extension {extension}")
    return filepath

def validate_positive_number(value, value_name):
    """Validates that a value is a positive number."""
    try:
        num = float(value)
        if num <= 0:
            raise ValueError(f"{value_name} must be a positive number.")
        return num # Return the validated float value
    except ValueError:
        raise ValueError(f"Invalid {value_name}: {value}")

def parse_centers_file(filepath):
    """Parses the centers file and returns a list of Center objects."""
    centers = []
    try:
        with open(filepath, 'r') as f:
            for line_number, line in enumerate(f, 1):  # Start line numbering from 1
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                try:
                    parts = line.split(',')
                    if len(parts) != 3:
                        raise ValueError("Each line must have 3 comma-separated values.")
                    lat = validate_coordinate(parts[0].strip(), 'latitude')
                    lon = validate_coordinate(parts[1].strip(), 'longitude')
                    radius = validate_positive_number(parts[2].strip(), "radius")
                    centers.append(Center(lat, lon, radius))
                except ValueError as e:
                    print(f"Skipping line {line_number} in {filepath}: {e}")
                    continue  # Skip to the next line
    except FileNotFoundError:
        raise FileNotFoundError(f"Centers file not found: {filepath}")
    except Exception as e:
        raise RuntimeError(f"Error reading centers file: {e}")

    return centers