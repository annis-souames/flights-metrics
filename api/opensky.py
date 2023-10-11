"""
For now this API is down, please use FlightRadarClient in flightradar

"""

import requests
from requests.auth import HTTPBasicAuth
import urllib.parse
import pdb
import time
from loguru import logger
from .state import StateParser


class OpenSkyClient:
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
        # pdb.set_trace()
        try:
            resp = requests.get(
                url, params=parameters, auth=HTTPBasicAuth(self.username, self.password)
            )
        except requests.exceptions.HTTPError as errh:
            logger.error("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            logger.error("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            logger.error("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            logger.error("OOps: Something Else", err)
        else:
            print(resp.content)
            print(resp.request.url)
            self.updateLimitInformation(resp)
            if (
                resp.status_code == 429
            ):  # In case of too many requests, wait for X seconds then retry
                # TODO : Add logging here to inform
                logger.error("States is null, retrying after one minute")
                time.sleep(self.retry_after)
                self.getResource(endpoint, parameters)
            if resp.content.states == None:
                logger.error("States is null, retrying after one minute")
                print("States is null, retrying after one minute")
                time.sleep(60)
                self.getResource(endpoint, parameters)
            return resp.json()

    def updateLimitInformation(self, response: requests.Response):
        if "X-Rate-Limit-Remaining" in response.headers:
            self.credits = response.headers["X-Rate-Limit-Remaining"]
        if "X-Rate-Limit-Retry-After-Seconds" in response.headers:
            self.retry_after = response.headers["X-Rate-Limit-Retry-After-Seconds"]
        logger.info(
            f'You have {response.headers["X-Rate-Limit-Remaining"]} credits left'
        )
        # print(response.headers['X-Rate-Limit-Retry-After-Seconds'])

    def getFlightsInRegion(self, boundingBox: dict):
        # bbox = (min latitude, max latitude, min longitude, max longitude)
        states = self.getResource("states/all", boundingBox)
        return StateParser(states)
