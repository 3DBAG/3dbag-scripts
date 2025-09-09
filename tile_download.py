import argparse
from pathlib import Path
import logging
import sys
import flatgeobuf as fgb
from urllib.request import urlretrieve

"""
The script downloads 3DBAG tiles in the formats obj, cityjson and gpkg.
You can specify the output directory with the --outdir flag.
If not specified, the files will be downloaded in the current directory.
You can specify the bounding box with the --bbox flag in the format xmin, ymin, xmax, ymax.
If not specified, the script will download all tiles.
You can specify the formats you want to download with the flags --obj, --cityjson, --gpkg, and --ifc.
If not specified, the script will download all formats.

Examples:

Download all tiles in all formats in a specific directory:
    `python3 tile_download.py --outdir /path/to/directory`

Download tiles within a bbox in obj formats in the current directory:
    `python3 tile_download.py --bbox 84000 477000 86000 478000 --obj`

"""

def get_tile_index(bbox: tuple = None):
    tile_index = fgb.HTTPReader('https://data.3dbag.nl/latest/tile_index.fgb', bbox=bbox)    
    return tile_index

def download_obj(tile_id, tilesdir: Path) -> None:
    url = tile_id.properties['obj_download']
    filename = tilesdir / url.split('/')[-1]
    _ = urlretrieve(url, filename)

def download_cityjson(tile_id, tilesdir: Path) -> None:
    url = tile_id.properties['cj_download']
    filename = tilesdir / url.split('/')[-1]
    _ = urlretrieve(url, filename)

def download_gpkg(tile_id, tilesdir: Path) -> None:
    url = tile_id.properties['gpkg_download']
    filename = tilesdir / url.split('/')[-1]
    _ = urlretrieve(url, filename)

def download_ifc(tile_id, tilesdir: Path) -> None:
    url = tile_id.properties['ifc_download']
    filename = tilesdir / url.split('/')[-1]
    _ = urlretrieve(url, filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", help="Output dir", type=str)
    parser.add_argument("--bbox", help="bbox coordinates xmin, ymin, xman, ymax", nargs=4, type=float)
    parser.add_argument("--obj", help="Download  obj",   action='store_true')
    parser.add_argument("--cityjson", help="Download cityjson",  action='store_true')
    parser.add_argument("--gpkg", help="Download gpkg", action='store_true')
    parser.add_argument("--ifc", help="Download ifc", action='store_true')
    args = parser.parse_args()

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

    logging.info('getting tile ids...')
    tids = get_tile_index( (args.bbox) )

    pathname = Path(args.outdir) if args.outdir else Path.cwd()
    if args.outdir:
        logging.info('creating output directory...') 
        pathname.mkdir(parents=True, exist_ok=True)

    for tid in tids:
        logging.info(f"tile {tid.properties['tile_id']}...")

        if args.obj:
            logging.info('downloading obj...')
            tilesdir = pathname / 'obj'
            tilesdir.mkdir(exist_ok=True)
            fnames = download_obj(tid, tilesdir)
        if args.cityjson:
            logging.info('downloading cityjson...')
            tilesdir = pathname / 'cityjson'
            tilesdir.mkdir(exist_ok=True)
            fnames = download_cityjson(tid, tilesdir)
        if args.gpkg:
            logging.info('downloading gpkg...')
            tilesdir = pathname / 'gpkg'
            tilesdir.mkdir(exist_ok=True)
            fnames = download_gpkg(tid, tilesdir)
        if args.ifc:
            logging.info('downloading ifc...')
            tilesdir = pathname / 'ifc'
            tilesdir.mkdir(exist_ok=True)
            fnames = download_ifc(tid, tilesdir)
        if not args.obj and not args.cityjson and not args.gpkg and not args.ifc:
            logging.info('downloading all formats...')
            tilesdir = pathname / 'obj'
            tilesdir.mkdir(exist_ok=True)
            download_obj(tid, tilesdir)
            tilesdir = pathname / 'cityjson'
            tilesdir.mkdir(exist_ok=True)
            download_cityjson(tid, tilesdir)
            tilesdir = pathname / 'gpkg'
            tilesdir.mkdir(exist_ok=True)
            download_gpkg(tid, tilesdir)
            tilesdir = pathname / 'ifc'
            tilesdir.mkdir(exist_ok=True)
            download_ifc(tid, tilesdir)
