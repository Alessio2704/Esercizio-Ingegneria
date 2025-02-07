import json
from classes import ChargingStation, TaxiStand

def load_geojson(filepath, object_type):
    """Loads GeoJSON data and returns a list of objects."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid GeoJSON format in file: {filepath}")

    objects = []
    for feature in data['features']:
        try:
            latitude = feature['properties']['geo_point_2d']["lat"]
            longitude = feature['properties']['geo_point_2d']["lon"]
            properties = feature['properties']

            if object_type == 'charging_station':
                # Extract relevant properties (adapt to your GeoJSON structure)
                operator = properties["operatore"]
                state = properties["stato"]
                available_spots = int(properties['numstalli'])
                obj = ChargingStation(latitude=latitude, longitude=longitude, operator=operator, available_spots=available_spots, state=state, properties=properties)

            elif object_type == 'taxi_stand':
                name = properties["nome"]
                total_spots = properties["stalli"]
                phone_number = properties["telefono"]
                obj = TaxiStand(latitude, longitude, name, phone_number, total_spots, properties)
            else:
                raise ValueError("Invalid object_type. Must be 'charging_station' or 'taxi_stand'")

            objects.append(obj)
        except (KeyError, TypeError, ValueError) as e:
            print(f"Skipping feature due to error: {e}")
            continue

    return objects