class Event:
    def __init__(self, event_name, capacity, location, pph, status=True):
        self.event_name = event_name
        self.capacity = capacity
        self.location = location
        self.price_per_hour = pph
        self.status = status


class User:
    def __init__(self, username, password, role="USER"):
        self.username = username
        self.password = password
        self.role = role