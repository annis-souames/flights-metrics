import json


class StateParser():
    def __init__(self, resp: dict):
        self.time = resp['time']
        self.states = [self._parseState(s) for s in resp['states']]

    def _parseState(self, state: list):
        return {
            'icao24': state[0],
            'callsign': state[1],
            'origin_country': state[2],
            'updated_at': state[4],
            'position': {
                'lon': state[5],
                'lat': state[6]
            },
            'velocity': state[9],
            'altitude': state[13]
        }