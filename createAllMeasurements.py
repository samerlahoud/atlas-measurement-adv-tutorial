import json
import os
from datetime import datetime, timedelta
from random import shuffle
from ripe.atlas.cousteau import (
    Ping,
    Traceroute,
    AtlasSource,
    AtlasCreateRequest
)

# Put your API key here from atlas.ripe.net
ATLAS_API_KEY = ""

with open('destinationNetworks.json', 'r') as f:
    networks = json.load(f)

with open('countries.json', 'r') as f:
    countries = json.load(f)

for source_country, source_country_code in countries.items():
    measurements = dict()
    for destination_network, destination_servers in networks.items():
        measurements[destination_network] = list()
        # Select randomly 3 servers from each network
        shuffle(destination_servers)
        for index, server in enumerate(destination_servers):
            if index == 3:
                break
            ping = Ping(af=4, target=server['host'],
                        description="From {} to {}".format(source_country_code, destination_network),
                        interval=10800, tags=["test_code_esib"])
            traceroute = Traceroute(
                af=4,
                target=server['host'],
                description="From {} to {}".format(source_country_code, destination_network),
                protocol="ICMP",
                interval=10800,
                tags=["test_code_esib"]
            )
            # Request 3 probes
            source = AtlasSource(type="country", value=source_country_code, requested=3)
            atlas_request = AtlasCreateRequest(
                start_time=datetime.utcnow() + timedelta(seconds=60),
                key=ATLAS_API_KEY,
                measurements=[ping, traceroute],
                sources=[source],
                is_oneoff=False
            )
            (is_success, response) = atlas_request.create()
            if is_success:
                measurements[destination_network].append(
                    {"host": server['host'], "is_success": is_success,
                     "measurement_id": response['measurements']})
            else:
                measurements[destination_network].append(
                    {"host": server['host'], "is_success": is_success, "reason": response})

    filename = "measurements/{}.json".format(source_country_code)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        json.dump(measurements, f, indent=4, sort_keys=True)
