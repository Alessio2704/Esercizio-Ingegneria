import json
import input_validation

def save_to_custom_csv(data, filepath):
    """Saves data to a custom CSV-like format (without using the csv module)."""
    try:
        input_validation.validate_filepath(filepath, ".csv")
    except FileNotFoundError:
        pass #File will be created
    except ValueError as e:
        raise e
    try:
        with open(filepath, 'w') as f:
            # Write header (assuming a consistent structure)
            f.write("Center Latitude,Center Longitude,Radius,District,Parking Meter Count\n")

            for item in data:
                center_lat = item['center_lat']
                center_lon = item['center_lon']
                center_radius = item['center_radius']
                for district, count in item['district_counts'].items():
                    f.write(f"{center_lat},{center_lon},{center_radius},{district},{count}\n")
    except Exception as e:
        raise RuntimeError(f"Error saving to CSV: {e}")


def save_to_json(data, filepath):
    """Saves data to a JSON file."""
    try:
        input_validation.validate_filepath(filepath, ".json")
    except FileNotFoundError:
        pass  # File will be created.
    except ValueError as e:
        raise e

    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)  # Use indent for readability
    except Exception as e:
        raise RuntimeError(f"Error saving to JSON: {e}")