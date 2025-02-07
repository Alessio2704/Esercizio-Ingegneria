class Location:
    def __init__(self, latitude, longitude):
        if not (-90 <= latitude <= 90):
            raise ValueError("Invalid latitude value")
        if not (-180 <= longitude <= 180):
            raise ValueError("Invalid longitude value")
        self.latitude = latitude
        self.longitude = longitude

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude

class ChargingStation(Location):
    def __init__(self, latitude, longitude, operator, available_spots, state, properties):
        super().__init__(latitude, longitude)
        self.operator = operator
        self.state = state
        self.available_spots = available_spots
        self.properties = properties

    def get_operator(self):
        return self.operator

    def get_available_spots(self):
        return self.available_spots if self.state == "attivo" else 0
    
    def get_state(self):
        return self.state

    def get_properties(self):
        return self.properties
    


class TaxiStand(Location):
    def __init__(self, latitude, longitude, name, phone_number, total_spots, properties):
        super().__init__(latitude, longitude)
        self.name = name
        self.total_spots = total_spots
        self.phone_number = phone_number
        self.properties = properties

    def get_total_spots(self):
        return self.total_spots

    def get_name(self):
        return self.name

    def get_phone_number(self):
        return self.phone_number
    
    def get_properties(self):
        return self.properties

class Center:
    def __init__(self, latitude, longitude, radius):
        if radius <= 0:
            raise ValueError("Radius must be positive")
        self.location = Location(latitude, longitude)
        self.radius = radius
    
    def get_location(self):
        return self.location
    
    def get_radius(self):
        return self.radius