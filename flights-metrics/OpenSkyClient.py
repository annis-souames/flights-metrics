
class OpenSkyClient():
    def __init__():
        self.api = OpenSkyApi()
        pass

    def getFlightsInBBox(bbox:tuple):
        #bbox = (min latitude, max latitude, min longitude, max longitude)
        states = self.api.get_states(bbox=bbox)
        for s in states.states:
            print("(%r, %r, %r, %r)" % (s.longitude, s.latitude, s.baro_altitude, s.velocity))
        