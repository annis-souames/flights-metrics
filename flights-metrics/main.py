from api import OpenSkyClient

client = OpenSkyClient()

resp = client.getStatesInRegion({
    "min_lat": 49.7,
    "max_lat": 50.5,
    "min_long": 3.2,
    "max_long": 4.6,
})

print(resp)