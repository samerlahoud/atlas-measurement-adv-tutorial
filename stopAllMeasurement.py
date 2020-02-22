import glob
import json
from ripe.atlas.cousteau import AtlasStopRequest

ATLAS_STOP_API_KEY = ""

failed_measurements = list()

for filepath in glob.iglob('measurements/*.json'):
    with open(filepath) as f:
        data = json.load(f)
    for k, v in data.items():
        for elt in v:
            try:
                for measurement in elt['measurement_id']:
                    atlas_request = AtlasStopRequest(msm_id=measurement, key=ATLAS_STOP_API_KEY)
                    (is_success, response) = atlas_request.create()
                    if not is_success:
                        failed_measurements.append(measurement)
            except KeyError:
                pass

with open('measurements-failed-to-stop.txt', 'w') as file:
    for elt in failed_measurements:
        file.write("%i\n" % elt)
