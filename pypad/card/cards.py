from ..region import Region
from ..data import get_raw_file
from . import Card

class Cards:
    _qualified_version = 1250
    _loaded_versions = {}
    _loaded_cards = {}

    def __new__(cls, region=Region.NA, dev=False):
        if region not in cls._loaded_cards:
            raw_card_json = get_raw_file('download_card_data.json', region)
            cls._loaded_versions[region] = raw_card_json['v']
            if dev:
                if cls._loaded_versions[region] != cls._qualified_version:
                    print(f'Mismatched parsing version and raw data version ({cls._qualified_version} vs {cls._loaded_versions[region]})')
            cls._loaded_cards[region] = {}
            for raw_card in raw_card_json['card']:
                card = Card(raw_card, region)
                cls._loaded_cards[region][card.id] = card
        cards = object.__new__(cls)
        cards._cards = cls._loaded_cards[region]
        return cards
    
    def __getitem__(self, id_):
        return self._cards[id_]

    def __iter__(self):
        return iter(self._cards.values())
