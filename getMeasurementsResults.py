import glob
import os
import ntpath
import json
from ripe.atlas.cousteau import AtlasResultsRequest

failed_measurements = list()

for filepath in glob.iglob('measurements/*.json'):
    file_name = os.path.splitext(ntpath.basename(filepath))[0]
    folder_name = "measurements/data/{}/".format(file_name)
    os.makedirs(os.path.dirname(folder_name), exist_ok=True)
    with open(filepath) as f:
        data = json.load(f)
    for k, v in data.items():
        folder_name = "measurements/data/{}/{}/".format(file_name, k)
        os.makedirs(os.path.dirname(folder_name), exist_ok=True)
        for elt in v:
            try:
                for measurement in elt['measurement_id']:
                    kwargs = {"msm_id": measurement}
                    (is_success, results) = AtlasResultsRequest(**kwargs).create()
                    try:
                        with open("measurements/data/{}/{}/{}.json".format(file_name, k, measurement), "w") as f:
                            json.dump(results, f, indent=4, sort_keys=True)
                    except Exception as e:
                        failed_measurements.append(measurement)
            except KeyError:
                pass

with open('measurements-failed-to-download.txt', 'w') as f:
    for elt in failed_measurements:
        f.write("%s\n" % elt)