# @todo : Add some logging
# @todo: Add tests

import requests
import urllib.parse
import pdb

class OpenSkyClient():
    base_url = "https://opensky-network.org/api/"
    
    def __init__(self):
        pass

    def getResource(self, endpoint: str, parameters: dict = {}):
        url = urllib.parse.urljoin(OpenSkyClient.base_url, endpoint)
        print(url)
        #pdb.set_trace()
        try:
            resp = requests.get(url, params=parameters)
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
        else:
            return resp.text

    def getStatesInBBox(self, bbox: tuple):
        #bbox = (min latitude, max latitude, min longitude, max longitude)
        states = requests.get(base_url)
        for s in states.states:
            print("(%r, %r, %r, %r)" % (s.longitude, s.latitude, s.baro_altitude, s.velocity))
        