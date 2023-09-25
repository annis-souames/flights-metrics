# @todo : Add some logging
# @todo: Add tests

import requests
from requests.auth import HTTPBasicAuth
import urllib.parse
import pdb
import time
from .state import StateParser


class OpenSkyClient():
    base_url = "https://opensky-network.org/api/"
    
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.credits = None
        self.retry_after = None
        pass

    def getResource(self, endpoint: str, parameters: dict = {}):
        url = urllib.parse.urljoin(OpenSkyClient.base_url, endpoint)
        print(url)
        #pdb.set_trace()
        try:
            resp = requests.get(
                                url, 
                                params=parameters,
                                auth=HTTPBasicAuth(self.username, self.password)
                                                
                               )
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
        else:
            print(resp.content)
            self.updateLimitInformation(resp)
            if resp.status_code == 429:  # In case of too many requests, wait for X seconds then retry
                # TODO : Add logging here to inform
                time.sleep(self.retry_after)
                self.getResource(endpoint, parameters)
            return resp.json()
        
    def updateLimitInformation(self, response: requests.Response):
        if 'X-Rate-Limit-Remaining' in response.headers:
            self.credits = response.headers['X-Rate-Limit-Remaining']
        if 'X-Rate-Limit-Retry-After-Seconds' in response.headers:
            self.retry_after = response.headers['X-Rate-Limit-Retry-After-Seconds']
        print("You have ", response.headers['X-Rate-Limit-Remaining'])
        #print(response.headers['X-Rate-Limit-Retry-After-Seconds'])

    def getStatesInRegion(self, boundingBox: dict):
        # bbox = (min latitude, max latitude, min longitude, max longitude)
        states = self.getResource("states/all", boundingBox)
        return StateParser(states)