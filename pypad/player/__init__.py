from ..dev import Dev
from .friend import Friend
from .monster_box import MonsterBox
from .team import Team
from ..region import Region
from ..data import get_json,get_time

class Player:
    def __init__(self, player_download_json_path, region=Region.NA):
        self.region = region

        player_json = get_json(player_download_json_path)

        if (player_json['res'] != 0):
            Dev.log(f"Player download json has bad response code: {player_json['res']}")

        self.max_friend_count = player_json['friendMax']
        self.friends = {friend_raw[1]:Friend(friend_raw, self.region) for friend_raw in player_json['friends']}
        #for friend_id,timestamp in zip(*[player_json['fridt']]*2): # iterate over pairs of values, source: https://stackoverflow.com/a/5389547
        #    self.friends[friend_id].date_registered = get_time(timestamp)

        self._pal_points = player_json['plp']
        # player_json['ndun'] - dungeon clear data?
        # player_json['msg'] - unknown
        # player_json['gmsg'] - url for getting 'msg' above
        # player_json['egatya3'] - some collab rem data
        # player_json['dcnt'] - unknown
        self._mail_notifications = player_json['mails']
        # player_json['pback'] - unknown
        self.login_streak = player_json['lstreaks']
        self.logins = player_json['logins']
        # player_json['litems'] - unknown
        # player_json['litemT'] - unknown

        # player_json['cver'] - guess is version for other jsons
        # player_json['sver'] - guess is version for other jsons
        # player_json['dver'] - guess is version for other jsons
        # player_json['pver'] - guess is version for other jsons
        # player_json['msver'] - guess is version for other jsons
        # player_json['dsver'] - guess is version for other jsons
        # player_json['psver'] - guess is version for other jsons
        # player_json['alver'] - guess is version for other jsons
        # player_json['mever'] - guess is version for other jsons

        self.box_capacity = player_json['cardMax']
        self.monster_box = MonsterBox(self.box_capacity, player_json['card'])
        self.name = player_json['name']
        self.rank = player_json['lv']
        self.experience = player_json['exp']
        # player_json['camp'] - unknown
        self.max_team_cost = player_json['cost']
        self.stamina = player_json['sta']
        self.max_stamina = player_json['sta_max']
        self.full_stamina_time = get_time(player_json['sta_time'], self.region)
        self._stones = player_json['gold']
        self.coins = player_json['coin']
        self._monster_points = player_json['mp']
        self.max_teams = player_json['max_decks']
        self.current_team = player_json['curDeck']
        # player_json['decksb']['fmt'] - unknown
        self.teams = [Team(team_raw) for team_raw in player_json['decksb']['decks']]
        # player_json['decksb']['bg'] - unknown
        # player_json['fripnt'] - unknown
        # player_json['fp_by_frd'] - unknown
        # player_json['fp_by_non_frd'] - unknown
        # player_json['fripntadd'] - unknown
        # player_json['pbflg'] - unknown
        self.previous_rank_experience = player_json['curLvExp']
        self.next_rank_experience = player_json['nextLvExp']
        # player_json['sr'] - unknown
        # player_json['cs'] - unknown
        self._best_friend_selection_available = player_json['bf']
        # player_json['tm'] - unknown
        # player_json['exc'] - unknown
        # player_json['skdr'] - unknown
        # player_json['skdg'] - unknown
        # player_json['us'] - unknown
        # player_json['caf'] - unknown
        # player_json['r'] - unknown


class PlayerManager:
    def __init__(self):
        self._players = {}

    def _regisiter(self, player):
        self._players[player.id] = player

    def __iter__(self):
        return iter(self._players.values())

    def __contains(self, player_id):
        return player_id in self._players

    def __getitem(self, player_id):
        return self._players[player_id]