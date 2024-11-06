# 3dbag-scripts
Small scripts for various functionalities related to 3DBAG data


## From 3DBAG-API to a city.json file

Script: api_to_cityjson.py

This script fetches a single building from the 3DBAG API and saves it directly 
in a CityJSON file.


It requires an installation of cjio. Preferably in a virtual environment you can install `cjio` with:

```bash
pip install cjio
```

Then, in the script, you need to substitute the BUILDING_ID with the id of the building you want to fetch.

Then you can run the script from your terminal with:
```
python3 api_to_cityjson.py
```

The script will first download the `city.jsonl` file and then convert it to `city.jsonl`, using as filename the BUILDING_ID

## Download 3DBAG Tiles

The script downloads 3DBAG tiles in the formats obj, cityjson and gpkg.
You can specify the output directory with the `--outdir` flag.
If not specified, the files will be downloaded in the current directory.
You can specify the bounding box with the `--bbox` flag in the format xmin, ymin, xmax, ymax.
If not specified, the script will download all tiles.
You can specify the formats you want to download with the flags `--obj`, `--cityjson` and `--gpkg`.
If not specified, the script will download all formats.

Examples:

Download all tiles in all formats in a specific directory:
```bash
python3 tile_downloader.py --outdir /path/to/directory
```

Download tiles within a bbox in obj formats in the current directory:
```bash
python3 tile_downloader.py --bbox 84000 477000 86000 478000 --obj
```
