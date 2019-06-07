from .dev import Dev
from .region import Region
from .download_manager import DownloadManager
from .player import Player, PlayerManager
from .evolution import Evolution, EvolutionManager
from .card import CardData, MonsterBook
from .enemy import EnemyData, EnemyMonsterBook
from .active_skill import ActiveSkill, ActiveSkillBook
from .leader_skill import LeaderSkill, LeaderSkillBook
from .skill_loader import SkillLoader
from .dungeon import DungeonBook
EnemySkill = type(None) # from .enemy_skill import EnemySkill



class Game:
    _qualified_card_version = 1600
    _qualified_skill_version = 1220
    _qualified_enemy_skill_version = 0
    _qualified_dungeon_version = 6

    _loaded_regions = {}

    def __init__(self, region=Region.NA):
        self._region = region
        if self._region not in self.__class__._loaded_regions:
            self.__class__._loaded_regions[self._region] = {}
            self.__class__._loaded_regions[self._region]['download_manager'] = DownloadManager(self._region)
            self.__class__._loaded_regions[self._region]['player_manager'] = PlayerManager()
            self._reload()
        
    # Updates the game to match the current version
    def update(self):
        self.__class__._loaded_regions[self._region]['download_manager'].update()
        self._reload()

    def _reload(self):
        # Active Skill and Leader Skill data
        self.__class__._loaded_regions[self._region]['active_skill_book'] = ActiveSkillBook()
        self.__class__._loaded_regions[self._region]['leader_skill_book'] = LeaderSkillBook()

        Dev.log('Starting to parse skills')

        raw_skill_json = self.__class__._loaded_regions[self._region]['download_manager'].get_game_file('download_skill_data.json')

        raw_skill_version = raw_skill_json['v']
        if self._qualified_skill_version < raw_skill_version:
            Dev.log(f'Skill parsing version outdated ({self._qualified_skill_version} vs {raw_skill_version})')

        Dev.timer_start()
        for skill_id,raw_skill in enumerate(raw_skill_json['skill']):
            self.__class__._loaded_regions[self._region]['active_skill_book']._register(SkillLoader.load_active_skill(skill_id,raw_skill,self._region))
            self.__class__._loaded_regions[self._region]['leader_skill_book']._register(SkillLoader.load_leader_skill(skill_id,raw_skill,self._region))
        Dev.timer_end()
        
        Dev.log(f'Finished parsing skills, took {Dev.timer_read():2f} seconds')


        # Enemy Skill data
        self.__class__._loaded_regions[self._region]['enemy_skill_data'] = None


        # Card, Enemy, and Evolution data
        self.__class__._loaded_regions[self._region]['monster_book'] = MonsterBook()
        self.__class__._loaded_regions[self._region]['enemy_monster_book'] = EnemyMonsterBook()
        self.__class__._loaded_regions[self._region]['evolution_manager'] = EvolutionManager()

        Dev.log('Starting to parse cards')

        raw_card_json = self.__class__._loaded_regions[self._region]['download_manager'].get_game_file('download_card_data.json')

        raw_card_version = raw_card_json['v']
        if self._qualified_card_version < raw_card_version:
            Dev.log(f'Card parsing version outdated ({self._qualified_card_version} vs {raw_card_version})')

        Dev.timer_start()
        for raw_card in raw_card_json['card']:
            self.__class__._loaded_regions[self._region]['monster_book']._register(CardData(raw_card))
            self.__class__._loaded_regions[self._region]['enemy_monster_book']._register(EnemyData(raw_card))
            self.__class__._loaded_regions[self._region]['evolution_manager']._register(Evolution(raw_card))
        Dev.timer_end()
        
        Dev.log(f'Finished parsing cards, took {Dev.timer_read():2f} seconds')


        # Dungeon data
        self.__class__._loaded_regions[self._region]['dungeon_book'] = DungeonBook()

        Dev.log('Starting to parse dungeons')

        raw_dungeon_json = self.__class__._loaded_regions[self._region]['download_manager'].get_game_file('download_dungeon_data.json')

        raw_dungeon_version = raw_dungeon_json['v']
        if self._qualified_dungeon_version < raw_dungeon_version:
            Dev.log(f'Dungeon parsing version outdated ({self._qualified_dungeon_version} vs {raw_dungeon_version})')

        Dev.timer_start()
        self.__class__._loaded_regions[self._region]['dungeon_book']._load(raw_dungeon_json['dungeons'])
        Dev.timer_end()
        
        Dev.log(f'Finished parsing dungeons, took {Dev.timer_read():2f} seconds')

    
    # Adds a player by their download data
    def add_player_by_json(self, file_path: str):
        player_json = self.__class__._loaded_regions[self._region]['download_manager'].open_file_as_json(file_path)
        self.__class__._loaded_regions[self._region]['player_manager']._register(Player(player_json))

    @property
    def region(self):
        return self._region

    @property
    def players(self) -> PlayerManager:
        return self.__class__._loaded_regions[self._region]['player_manager']

    @property
    def active_skill_book(self) -> ActiveSkillBook:
        return self.__class__._loaded_regions[self._region]['active_skill_book']

    @property
    def leader_skill_book(self) -> LeaderSkillBook:
        return self.__class__._loaded_regions[self._region]['leader_skill_book']

    @property
    def monster_book(self) -> MonsterBook:
        return self.__class__._loaded_regions[self._region]['monster_book']

    @property
    def enemy_monster_book(self) -> EnemyMonsterBook:
        return self.__class__._loaded_regions[self._region]['enemy_monster_book']

    @property
    def evolutions(self) -> EvolutionManager:
        return self.__class__._loaded_regions[self._region]['evolution_manager']

    @property
    def dungeons(self) -> DungeonBook:
        return self.__class__._loaded_regions[self._region]['dungeon_book']

    def to_json(self) -> dict:
        return {
            'cards': self.__class__._loaded_regions[self._region]['monster_book'].to_json(),
            'enemies': self.__class__._loaded_regions[self._region]['enemy_monster_book'].to_json(),
            'evolutions': self.__class__._loaded_regions[self._region]['evolution_manager'].to_json(),
            'active_skills': self.__class__._loaded_regions[self._region]['active_skills_book'].to_json(),
            'leader_skills': self.__class__._loaded_regions[self._region]['leader_skills_book'].to_json(),
            'dungeons': self.__class__._loaded_regions[self._region]['dungeon_book'].to_json(),
        }


# workaround for circular imports
from .skill_loader import _register_special_active_skill_classes
_register_special_active_skill_classes()
from .skill_loader import _register_special_leader_skill_classes
_register_special_leader_skill_classes()