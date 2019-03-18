from .card_parser import CardParser
from .skill_parser import SkillParser
from .enemy_skill_parser import EnemySkillParser
from .dungeon_parser import DungeonParser
import json

class Parser:
    _parser_classes = [CardParser, SkillParser, EnemySkillParser, DungeonParser]

    def _get_json_from_file(self, filename: str) -> dict:
        with open(filename, 'r') as input_file:
            return json.loads(input_file)
        return {}

    def _save_json_to_file(self, parsed_json: dict, filename: str, pretty=False):
        with open(filename, 'w') as output_file:
            if pretty:
                output_file.write(json.dumps(parsed_json, indent=4, sort_keys=True))
            else:
                output_file.write(json.dumps(parsed_json, sort_keys=True))
    
    def _parse(self, raw_data: dict, report=False, report_dev=False) -> dict:
        for parser_class in Parser._parser_classes:
            parser_instance = parser_class()
            if parser_instance.parsable(raw_data):
                parsed_json = parser_instance.parse(raw_data)
                tag = parser_instance.get_tag()
                for line in parser_instance.get_reports:
                    print(f'[{tag}] {line}')
                for line in parser_instance.get_reports_dev:
                    print(f'[{tag}] {line}')
                return parsed_json
        return None

    # output can be a filename to export to
    def parse(self, input_value: 'filename or dict', output_path=None, pretty=False, report=False, report_dev=False):
        if type(input_value) == str:
            input_value = self._get_json_from_file(input_value)
        if type(input_value) != dict:
            raise ValueError('input_value must be a dict or a valid json file path')
        
        parsed_json = self._parse(input_value, report, report_dev)

        if output_path == None:
            return parsed_json

        self._save_json_to_file(parsed_json, output_path, pretty)
        



            
    

    