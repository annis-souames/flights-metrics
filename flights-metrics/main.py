from api.OpenSky import OpenSkyClient

client = OpenSkyClient()

resp = OpenSkyClient().getResource("states/all")

print(resp)