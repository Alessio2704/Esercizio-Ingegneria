import requests
import json

def get_google_maps_data(origin, destination):
    lat_1 = origin.get_latitude()
    lon_1 = origin.get_longitude()
    lat_2 = destination.get_latitude()
    lon_2 = origin.get_longitude()
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={lat_1},{lon_1}&destination={lat_2},{lon_2}&key=AIzaSyDTXurHwTbBbjx3vec5B7wZ2ZqXxMuveZA"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)
    distance = data["routes"][0]["legs"][0]["distance"]["text"]
    duration = data["routes"][0]["legs"][0]["duration"]["text"]

    return (distance, duration)