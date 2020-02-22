import glob
import os
import ntpath
import json
from datetime import datetime

from ripe.atlas.cousteau import (
    Ping,
    Traceroute,
    AtlasSource,
    AtlasCreateRequest
)

ATLAS_API_KEY = ""

for filepath in glob.iglob('measurements/*.json'):
    source_country_code = os.path.splitext(ntpath.basename(filepath))[0]
    measurement_dict = dict()
    with open(filepath) as f:
        data = json.load(f)
    for destination_network, measurements in data.items():
        measurement_dict[destination_network] = []
        for elt in measurements[:]:
            if elt['is_success'] is False:
                measurements.remove(elt)

                ping = Ping(af=4, target=elt['host'],
                            description="From {} to {}".format(source_country_code, destination_network),
                            interval=10800, tags=["retry-test-code-esib"])
                traceroute = Traceroute(
                    af=4,
                    target=elt['host'],
                    description="From {} to {}".format(source_country_code, destination_network),
                    protocol="ICMP",
                    interval=10800, 
                    tags=["retry-test-code-esib"]
                )
                source = AtlasSource(type="country", value=source_country_code, requested=3)
                atlas_request = AtlasCreateRequest(
                    start_time=datetime.utcnow(),
                    key=ATLAS_API_KEY,
                    measurements=[ping, traceroute],
                    sources=[source],
                    is_oneoff=False
                )
                (is_success, response) = atlas_request.create()
                if is_success:
                    measurement_dict[destination_network].append(
                        {"host": elt['host'], "is_success": is_success,
                         "measurement_id": response['measurements']})
                else:
                    measurement_dict[destination_network].append(
                        {"host": elt['host'], "is_success": is_success,
                         "reason": response})
            else:
                measurement_dict[destination_network].append(
                        {"host": elt['host'], "is_success": elt['is_success'],
                         "measurement_id": elt['measurement_id']})


    filename = "measurements/{}.json".format(source_country_code)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        json.dump(measurement_dict, f, indent=4, sort_keys=True)
