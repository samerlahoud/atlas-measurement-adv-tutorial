from ripe.atlas.cousteau import AtlasStopRequest

msm_id_list = []

ATLAS_STOP_API_KEY = ""

for msm_id in msm_id_list:
    atlas_request = AtlasStopRequest(msm_id=msm_id, key=ATLAS_STOP_API_KEY)
    (is_success, response) = atlas_request.create()
    print(is_success)