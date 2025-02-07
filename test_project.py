# test_project.py

import unittest
from classes import Location, ChargingStation, TaxiStand, Center
from data_loader import load_geojson
from calculations import haversine, is_within_radius
from data_analysis import count_active_charging_spots, count_taxi_spots, find_nearest_charging_stations
from input_validation import validate_coordinate, validate_filepath, validate_positive_number, parse_centers_file
import os
import json
import io
from contextlib import redirect_stdout

class TestProject(unittest.TestCase):

    # --- Test Classes ---
    def test_location_creation(self):
        loc = Location(40.7128, -74.0060)
        self.assertEqual(loc.get_latitude(), 40.7128)
        self.assertEqual(loc.get_longitude(), -74.0060)

    def test_location_invalid_latitude(self):
        with self.assertRaises(ValueError):
            Location(91, 0)  # Invalid latitude
        with self.assertRaises(ValueError):
            Location(-91, 0)  # Invalid latitude

    def test_location_invalid_longitude(self):
        with self.assertRaises(ValueError):
            Location(0, 181)  # Invalid longitude
        with self.assertRaises(ValueError):
            Location(0, -181) # Invalid longitude
    
    def test_charging_station_creation(self):
        station = ChargingStation(40.7, -74.0, "Operator A", 5, 10, {})
        self.assertEqual(station.get_operator(), "Operator A")
        self.assertEqual(station.get_available_spots(), 5)
        self.assertEqual(station.get_total_spots(), 10)
    
    def test_taxi_stand_creation(self):
        station = TaxiStand(40.7, -74.0, "Central Taxi", "123-456-7890", 10, {})
        self.assertEqual(station.get_name(), "Central Taxi")
        self.assertEqual(station.get_phone_number(), "123-456-7890")
        self.assertEqual(station.get_total_spots(), 10)
    
    def test_center_creation(self):
        loc = Center(40.7128, -74.0060, 1000)
        self.assertEqual(loc.get_location().get_latitude(), 40.7128)
        self.assertEqual(loc.get_location().get_longitude(), -74.0060)
        self.assertEqual(loc.get_radius(), 1000)

    def test_center_invalid_radius(self):
        with self.assertRaises(ValueError):
            Center(0, 0, -10)

    # --- Test Data Loader ---

    def setUp(self):
        # Create dummy GeoJSON files for testing
        self.charging_data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [-74.0060, 40.7128]},
                    "properties": {"OPERATORE": "Op1", "Numero_Stalli_Attivi": "2", "Numero_Stalli": "5", "quartiere": "A"}
                },
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [-73.9857, 40.7484]},
                    "properties": {"OPERATORE": "Op2", "Numero_Stalli_Attivi": 3, "Numero_Stalli": "3", "quartiere": "B"}
                },
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [-73.9857, 40.7484]},
                    "properties": {"OPERATORE": "Op2", "Numero_Stalli_Attivi": "", "Numero_Stalli": "10", "quartiere": "B"}
                }
            ]
        }
        self.taxi_data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [-73.99, 40.75]},
                    "properties": {"DENOMINAZIONE": "Taxi A", "TELEFONO": "111-222", "NUMERO_STALLI" : "10"}
                },
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [-73.98, 40.76]},
                    "properties": {"DENOMINAZIONE": "Taxi B", "TELEFONO": None, "NUMERO_STALLI": "5"}
                }
            ]
        }

        with open('test_charging.geojson', 'w') as f:
            json.dump(self.charging_data, f)
        with open('test_taxi.geojson', 'w') as f:
            json.dump(self.taxi_data, f)

    def tearDown(self):
        # Remove the dummy files
        os.remove('test_charging.geojson')
        os.remove('test_taxi.geojson')

    def test_load_geojson_charging(self):
        stations = load_geojson('test_charging.geojson', 'charging_station')
        self.assertEqual(len(stations), 3)
        self.assertEqual(stations[0].get_operator(), "Op1")
        self.assertEqual(stations[0].get_available_spots(), 2)
        self.assertEqual(stations[0].get_total_spots(), 5)
        self.assertEqual(stations[1].get_available_spots(), 3)
        self.assertEqual(stations[2].get_available_spots(), 0)
        self.assertEqual(stations[2].get_total_spots(), 10)


    def test_load_geojson_taxi(self):
        stands = load_geojson('test_taxi.geojson', 'taxi_stand')
        self.assertEqual(len(stands), 2)
        self.assertEqual(stands[0].get_name(), "Taxi A")
        self.assertEqual(stands[0].get_phone_number(), "111-222")
        self.assertEqual(stands[1].get_phone_number(), None)
        self.assertEqual(stands[0].get_total_spots(), 10)

    def test_load_geojson_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            load_geojson('nonexistent_file.geojson', 'charging_station')

    def test_load_geojson_invalid_format(self):
        with open('invalid.geojson', 'w') as f:
            f.write("This is not valid GeoJSON")  # Create an invalid file
        with self.assertRaises(ValueError):
            load_geojson('invalid.geojson', 'charging_station')
        os.remove('invalid.geojson')  # Clean up

    def test_load_geojson_invalid_type(self):
        with self.assertRaises(ValueError):
            load_geojson('test_charging.geojson', 'invalid_type')

    # --- Test Calculations ---

    def test_haversine(self):
        # Test case with known distance (approximately)
        lat1, lon1 = 40.7128, -74.0060  # New York City
        lat2, lon2 = 34.0522, -118.2437  # Los Angeles
        distance = haversine(lat1, lon1, lat2, lon2)
        self.assertAlmostEqual(distance, 3935751, delta=1000)  # Allow 1km difference

    def test_is_within_radius(self):
        center_lat, center_lon, radius = 40.7, -74.0, 1000  # Center and radius (1km)
        point_inside_lat, point_inside_lon = 40.705, -74.005  # Inside
        point_outside_lat, point_outside_lon = 40.8, -74.1  # Outside

        self.assertTrue(is_within_radius(center_lat, center_lon, radius, point_inside_lat, point_inside_lon))
        self.assertFalse(is_within_radius(center_lat, center_lon, radius, point_outside_lat, point_outside_lon))

    # --- Test Data Analysis ---

    def test_count_active_charging_spots(self):
        stations = [
            ChargingStation(0, 0, "Op1", 2, 5, {}),
            ChargingStation(0, 0, "Op2", 3, 5, {}),
            ChargingStation(0, 0, "Op1", 0, 5, {}),
        ]
        total_spots = count_active_charging_spots(stations)
        self.assertEqual(total_spots, 5)

    def test_count_taxi_spots(self):
        stations = [
            TaxiStand(0, 0, "Taxi1", "111-222", 10, {}),
            TaxiStand(0, 0, "Taxi2", None, 5, {}),
            TaxiStand(0, 0, "Taxi3", "111-333", 0, {}),
        ]
        total_spots = count_taxi_spots(stations)
        self.assertEqual(total_spots, 15)
    
    def test_find_nearest_charging_stations(self):
        user_location = Location