class Monsters:
    _data = {}

    @classmethod
    def _load(cls, parsed_json: dict):
        cls._data = parsed_json

    @classmethod
    def get_monster_by_id(cls, monster_id: int):
        if monster_id not in cls._data:
            raise ValueError("Monster id does not exist")
        