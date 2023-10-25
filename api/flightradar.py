from loguru import logger
from FlightRadar24 import FlightRadar24API
import sys


class FlightRadarClient:
    def __init__(self, username: str = "", password: str = ""):
        if username == "" and password == "":
            self.client = FlightRadar24API()
        else:
            self.client = FlightRadar24API(username, password)

    def getFlightsInRegion(self, bbox: dict):
        zone = f"{bbox['lamax']},{bbox['lamin']},{bbox['lomin']},{bbox['lomax']}"
        print(zone)
        resp = self.client.get_flights(bounds=zone)
        if resp == None:
            logger.error("FlightRadar24 - API returned none object")
            sys.exit(1)
        elif len(resp) == 0:
            logger.error("FlightRadar24 - API returned empty array of flights")
            sys.exit(1)
        flights = [f.__dict__ for f in resp]
        return flights
