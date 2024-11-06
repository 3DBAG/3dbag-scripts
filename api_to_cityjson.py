import urllib.request
import json
import os 

"""
This script fetches a single building from the 3DBAG API and saves it directly 
in a CityJSON file.


It requires an installation of cjio. Preferably in a virtual environment,
you can install `cjio` with:

    `pip install cjio`

Then, in the script, you need to substitute the BUILDING_ID
with the id of the building you want to fetch.
Then you can run the script from your terminal with:

    `python3 api_to_cityjson.py`

The script will first download the `city.jsonl` file and then convert it
to `city.jsonl`, using as filename the BUILDING_ID
"""

BUILDING_ID = "NL.IMBAG.Pand.0503100000033172"

request = f"https://api.3dbag.nl/collections/pand/items/{BUILDING_ID}"

with urllib.request.urlopen(request) as response:

    j = json.loads(response.read().decode('utf-8'))
    with open(f"{BUILDING_ID}.city.jsonl", "w") as my_file:
        my_file.write(json.dumps(j["metadata"]) + "\n")
        if "feature" in j:
            my_file.write(json.dumps(j["feature"]) + "\n")
        if "features" in j:
            for f in j["features"]:
                my_file.write(json.dumps(f) + "\n")

os.system(f"cat {BUILDING_ID}.city.jsonl | cjio stdin info save {BUILDING_ID}.city.json")

