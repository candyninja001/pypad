import os
import json
import urllib.request
from datetime import datetime
from ..region import Region

def get_time(timestamp, region=Region.NA):
    tz_offsets = {
        Region.NA: '-0800',
        Region.JP: '+0900',
    }
    return datetime.strptime(f'{timestamp} {tz_offsets[region]}', '%y%m%d%H%M%S %z')

def get_json(file_path: str):
    with open(file_path, 'r') as input_file:
        return json.load(input_file)

def get_raw_file(filename: str, region=Region.NA):
    module_dir,_ = os.path.split(__file__)
    file_path = os.path.join(module_dir, 'raw', region.name(), filename)
    with open(file_path, 'r') as input_file:
        return json.load(input_file)

# Requires Google Cloud SDK
# https://cloud.google.com/storage/docs/gsutil_install
def update_game_files():
    module_dir,_ = os.path.split(__file__)
    raw_dir = os.path.join(module_dir, "raw")
    if not os.path.exists(raw_dir):
        os.mkdir(raw_dir)
    os.popen(f'gsutil -m rsync -d -r gs://pypad-data/raw {raw_dir}')