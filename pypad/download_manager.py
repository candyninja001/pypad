from .region import Region
import os
import json

class DownloadManager:
    def __init__(self, region: Region):
        self._region = region

    # Requires Google Cloud SDK
    # https://cloud.google.com/storage/docs/gsutil_install
    # Downloads the latest published game files
    def update(self):
        module_dir,_ = os.path.split(__file__)
        region_name = self._region.name()
        raw_region_dir = os.path.join(module_dir, "data", "raw", region_name)
        if not os.path.exists(raw_region_dir):
            os.mkdir(raw_region_dir)
        os.popen(f'gsutil -m rsync -d -r gs://pypad-data/raw/{region_name} {raw_region_dir}')

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