import urllib.request
import json
import os 
import glob

"""
This script fetches data from the 3DBAG API and saves it in a cityjson file.
It also takes care of pagination. If the result is paginated, it will save
each page in a separate file and then then merge them into a single CityJSON file.

It needs an installation of cjio. Install with `pip install cjio`

You should first structure the API request to get the data you want and 
then set the BASE_API_REQUEST variable to that request. 

The file will save first the results in CityJSONSeq (city.jsonl) format and then
convert it to CityJSON (city.json) format. 

Make sure to set the OUTPUT_FILE_NAME variable to the desired output filename.

Examples:
Single building:
https://api.3dbag.nl/collections/pand/items/NL.IMBAG.Pand.0503100000032914

Small bounding box:
https://api.3dbag.nl//collections/pand/items?bbox=85000.00,446700.034,85300.011,447000.00&limit=50
"""
BASE_API_REQUEST = "https://api.3dbag.nl//collections/pand/items?bbox=85000.00,446700.034,85300.011,447000.0&limit=50"
OUTPUT_FILE_NAME = "output"


def fetch_data(api_request):
    with urllib.request.urlopen(api_request) as response:
        return json.loads(response.read().decode('utf-8'))

def save_data(data, file):
    if "feature" in data:
        file.write(json.dumps(data["feature"]) + "\n")
    if "features" in data:
        for f in data["features"]:
            file.write(json.dumps(f) + "\n")

def main():
    api_request = BASE_API_REQUEST
    page = 1
    while api_request:
        filename = f"{OUTPUT_FILE_NAME}_page{page}.city.jsonl"
        with open(filename, "w") as my_file:
            data = fetch_data(api_request)
            my_file.write(json.dumps(data["metadata"]) + "\n")
            save_data(data, my_file)
            
        print(f"Saved page {page} to {filename}")

        next_link = None
        if "links" in data:
            for link in data["links"]:
                if link.get("rel") == "next":
                    next_link = link.get("href")
                    break
        if next_link:
            print(next_link)
            api_request = next_link
            page += 1
        else:
            api_request = None

    # Convert all the city.jsonl files to city.json files
    for file in glob.glob(f"{OUTPUT_FILE_NAME}_page*.city.jsonl"):
        os.system(f"cat {file} | cjio stdin info save {file.replace('.city.jsonl', '.city.json')}")
    
    # Merge all the city.json files into one
    os.system(f"cjio {OUTPUT_FILE_NAME}_page1.city.json merge '{OUTPUT_FILE_NAME}_page*.city.json' save {OUTPUT_FILE_NAME}.city.json")

    # Remove all the merged files
    for f in glob.glob(f"{OUTPUT_FILE_NAME}_page*.city.json*"):
        os.remove(f)

if __name__ == "__main__":
    main()