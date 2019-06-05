from collections import defaultdict
from ...common import defaultlist

class FloorRestriction:
    _handle_type = -1

    def __init__(self, args):
        self.args = args
        self.parse_args()

    def parse_args(self):
        pass

    def to_json(self, localize=False) -> dict:
        skill_json = {
            'type': self.floor_restriction_type,
            'args': self.args_to_json(),
        }
        if localize:
            skill_json['localization'] = self.localize()
        return skill_json

    def args_to_json(self) -> dict:
        return {'args': self.args}

    def localize(self) -> str:
        return ''

    @property
    def floor_restriction_type(self):
        return 'default_floor_restriction_type'
    

class FloorRestrictionLoader:
    _registered_floor_restriction_classes = {}

    @classmethod
    def _register_floor_restriction_class(cls, floor_restriction_class):
        if floor_restriction_class._handle_type in cls._registered_floor_restriction_classes:
            print(f'[Warning] Duplicate floor restriction type attempted to register ({floor_restriction_class._handle_type})')
        cls._registered_floor_restriction_classes[floor_restriction_class._handle_type] = floor_restriction_class

    @classmethod
    def load_floor_restriction(cls, restriction_type, args):
        if restriction_type in cls._registered_floor_restriction_classes:
            return cls._registered_floor_restriction_classes[restriction_type](defaultlist(int,args))
        print(f'[Warning] Floor restriction type={restriction_type} not handled, skipping')
        return None


from .attributes_required_fr import AttributesRequiredFR
from .max_team_rarity_fr import MaxTeamRarityFR
from .max_team_cost_fr import MaxTeamCostFR
from .max_team_size_fr import MaxTeamSizeFR
from .monster_required_fr import MonsterRequiredFR
from .no_dupes_fr import NoDupesFR
from .roguelike_fr import RoguelikeFR
from .type_restriction_fr import TypeRestrictionFR