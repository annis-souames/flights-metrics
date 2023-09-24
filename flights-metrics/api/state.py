import json


class StateParser():
    def __init__(self, resp: dict):
        self.time = resp['time']
        self.states = [self._parseState(s) for s in resp['states']]

    def _parseState(self, state: list):
        return {
            'id': state[0],
            'flight': state[1],
            'country': state[2]
        }