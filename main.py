# main.py

import data_loader
import data_analysis
import input_validation
import output_handler
import google_maps_api
from classes import Location
import sys

def main():
    try:
        charging_stations = data_loader.load_geojson("colonnine-elettriche.geojson", "charging_station")
        taxi_stands = data_loader.load_geojson("piazzole_taxi.geojson", "taxi_stand")

        # --- Task 1 & 2:  Count and print spots (Charging Stations) ---
        total_active_spots = data_analysis.count_active_charging_spots(charging_stations)
        print(f"Total active charging spots: {total_active_spots}")

        # --- Task 3: Count by operator and generate pie chart ---
        operator_counts = data_analysis.count_spots_by_operator(charging_stations)
        print(f"Operator Counts: {operator_counts}")
        image_filename = input("Enter filename for the operator pie chart: ")
        image_format = input("Enter image format (png, jpg, pdf, svg): ")
        try:
            data_analysis.generate_pie_chart(operator_counts, "Charging Spots by Operator", image_filename, image_format)
            print(f"Operator pie chart saved as {image_filename}.{image_format}")
        except ValueError as e:
            print(e)

        # --- Task 4 & 5: Count and print spots (Taxi Stands) ---
        total_taxi_spots = data_analysis.count_taxi_spots(taxi_stands)
        print(f"Total taxi spots: {total_taxi_spots}")

        taxi_spots_with_phone = data_analysis.count_taxi_spots_with_phone(taxi_stands)
        print(f"Taxi Spots with Phone: {taxi_spots_with_phone}")
        image_filename = input("Enter filename for the taxi stand pie chart: ")
        image_format = input("Enter image format (png, jpg, pdf, svg): ")

        try:
            data_analysis.generate_pie_chart(taxi_spots_with_phone, "Taxi Stands with Phone Numbers", image_filename, image_format)
            print(f"Taxi stand pie chart saved as {image_filename}.{image_format}")
        except ValueError as e:
            print(e)

        # --- Task 6 & 7:  Process Centers and Parking Meters ---
        centers_filepath = input("Enter the filepath for the centers file (txt): ")
        try:
            centers = input_validation.parse_centers_file(centers_filepath)
        except Exception as e: #FileNotFoundError and other errors
            print(e)
            return

        stations_count_by_district = data_analysis.count_stations_by_district(centers, charging_stations)
        csv_filepath = input("Enter the filepath for the output CSV file: ")
        try:
             output_handler.save_to_custom_csv(stations_count_by_district, csv_filepath)
             print("Data saved in CSV file")
        except Exception as e:
             print(e)


        # --- Task 8 & 9:  User Location, Nearest Stations, Google API ---
        while True:
            try:
                user_lat_str = input("Enter your latitude: ")
                user_lon_str = input("Enter your longitude: ")
                user_latitude = input_validation.validate_coordinate(user_lat_str, 'latitude')
                user_longitude = input_validation.validate_coordinate(user_lon_str, 'longitude')
                user_location = Location(user_latitude, user_longitude)
                break  # Exit loop if coordinates are valid
            except ValueError as e:
                print(e)

        nearest_stations = data_analysis.find_nearest_charging_stations(user_location, charging_stations)

        output_data = []
        for station, station_distance in nearest_stations:
            try:
                location = Location(station.get_latitude(), station.get_longitude())
                distance, duration = google_maps_api.get_google_maps_data(user_location, location)
                nearest_taxi, taxi_distance = data_analysis.find_nearest_taxi_stand(station, taxi_stands)
                taxi_info = {
                    "name": nearest_taxi.get_name(),
                    "distance": taxi_distance,
                    "phone_number": nearest_taxi.get_phone_number()
                } if nearest_taxi else None

                station_data = {
                    'charging_station': {
                        'latitude': station.get_latitude(),
                        'longitude': station.get_longitude(),
                        'operator': station.get_operator(),
                    },
                    'distance_from_user': station_distance,
                    'driving_distance': distance,
                    'driving_duration': duration,
                    'nearest_taxi_stand': taxi_info
                }
                output_data.append(station_data)
            except Exception as e:
                print(f"Error processing station {station.get_latitude()},{station.get_longitude()}: {e}")
                continue #Skips errors


        json_filepath = input("Enter the filepath for the output JSON file: ")
        try:
            output_handler.save_to_json(output_data, json_filepath)
            print(f"Results saved to {json_filepath}")
        except Exception as e:
            print(e)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()