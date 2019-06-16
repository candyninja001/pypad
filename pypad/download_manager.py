from .dev import Dev
from .region import Region
import os
import subprocess
import json

class DownloadManager:
    def __init__(self, region: Region):
        self._region = region

    # Requires Google Cloud SDK
    # https://cloud.google.com/storage/docs/gsutil_install
    # Downloads the latest published game files
    def update(self):
        Dev.log('Starting to download latest game files')
        module_dir,_ = os.path.split(__file__)
        region_name = self._region.name()
        raw_region_dir = os.path.join(module_dir, "data", "raw", region_name)
        if not os.path.exists(raw_region_dir):
            os.mkdir(raw_region_dir)
        Dev.timer_start()
        subprocess.Popen(f'gsutil -m rsync -d -r gs://pypad-data/raw/{region_name} {raw_region_dir}', shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL).wait()
        Dev.timer_end()
        Dev.log(f'Finished download, took {Dev.timer_read():2f} seconds')

    # Returns the json game data
    def get_game_file(self, filename: str):
        module_dir,_ = os.path.split(__file__)
        file_path = os.path.join(module_dir, 'data', 'raw', self._region.name(), filename)
        with open(file_path, 'r') as input_file:
            return json.load(input_file)

    # Opens a json file outside the module
    def open_file_as_json(self, file_path: str):
        with open(file_path, 'r') as input_file:
            return json.load(input_file)