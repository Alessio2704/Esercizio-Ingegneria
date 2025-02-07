import matplotlib.pyplot as plt
from calculations import is_within_radius
from calculations import haversine

def count_active_charging_spots(charging_stations):
    """Counts total active charging spots using a lambda function."""
    count_spots = lambda station: station.get_available_spots()
    total_spots = sum(map(count_spots, charging_stations))
    return total_spots

def count_spots_by_operator(charging_stations):
    """Counts charging spots by operator and generates a pie chart."""
    operator_counts = {}
    for station in charging_stations:
        operator = station.get_operator()
        operator_counts[operator] = operator_counts.get(operator, 0) + station.get_available_spots()

    return operator_counts

def generate_pie_chart(data_dict, title, filename, file_format):
    """Generates and saves a pie chart. Includes format validation."""
    if file_format.lower() not in ['png', 'jpg', 'jpeg', 'pdf', 'svg']:
        raise ValueError("Invalid image format.  Must be one of: png, jpg, jpeg, pdf, svg")

    labels = data_dict.keys()
    sizes = data_dict.values()

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(title)

    try:
        plt.savefig(f"{filename}.{file_format.lower()}")
        plt.close(fig)  # Close the figure to free memory
    except Exception as e:
        raise RuntimeError(f"Error saving image: {e}")


def count_taxi_spots(taxi_stands):
     """Counts total taxi spots using a lambda function."""
     count_spots = lambda stand: stand.get_total_spots()
     total_spots = sum(map(count_spots, taxi_stands))
     return total_spots

def count_taxi_spots_with_phone(taxi_stands):
    """Counts taxi spots with phone numbers and returns dict."""
    count_spots = {}

    for station in taxi_stands:
        if station.get_phone_number() is not None:
            name = station.get_name()
            count_spots[name] = count_spots.get(name, 0) + station.get_total_spots()
    return count_spots


def count_stations_by_district(centers, charging_stations):
    """Counts parking meters within each center's radius, by district."""
    results = []
    for center in centers:
        center_lat = center.get_location().get_latitude()
        center_lon = center.get_location().get_longitude()
        center_radius = center.get_radius()

        district_counts = {}  # Dictionary to store counts per district

        for station in charging_stations:
            point_lat = station.get_latitude()
            point_lon = station.get_longitude()
            if is_within_radius(center_lat, center_lon, center_radius, point_lat, point_lon):
                district = station.get_properties().get('quartiere', 'Unknown')
                district_counts[district] = district_counts.get(district, 0) + 1

        results.append({
            "center_lat": center_lat,
            "center_lon": center_lon,
            "center_radius": center_radius,
            "district_counts": district_counts,
        })
    return results

def find_nearest_charging_stations(user_location, charging_stations, n=2):
    """Finds the n nearest charging stations to the user location."""

    distances = []
    for station in charging_stations:
        distance = haversine(user_location.get_latitude(), user_location.get_longitude(),
                             station.get_latitude(), station.get_longitude())
        distances.append((station, distance))  # Store station object and distance

    # Sort by distance (the second element of the tuple)
    distances.sort(key=lambda x: x[1])
    return distances[:n]  # Return the n nearest

def find_nearest_taxi_stand(charging_station, taxi_stands):
    """Finds the nearest taxi stand to a given charging station."""
    nearest_stand = None
    min_distance = float('inf')

    for stand in taxi_stands:
        distance = haversine(charging_station.get_latitude(), charging_station.get_longitude(),
                             stand.get_latitude(), stand.get_longitude())
        if distance < min_distance:
            min_distance = distance
            nearest_stand = stand

    return nearest_stand, min_distance