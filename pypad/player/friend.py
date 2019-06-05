from ..data import get_time

class Friend:
    def __init__(self, friend_raw, region):
        self.region = region

        # 0 unknown
        self.id = friend_raw[1]
        self.name = friend_raw[2]
        self.rank = friend_raw[3]
        # 4 unknown
        self.last_played = get_time(friend_raw[5], self.region)
        # 6 - 13 unknown
        self.best_friend = friend_raw[14] == 1
        # 15 might be leaders, might be friend data
        # rest, leader/helper data
        self.leaders = (friend_raw[16],friend_raw[31],friend_raw[46]) if self.best_friend else (friend_raw[16],friend_raw[31])

    def __eq__(self, other):
        if type(other) == Friend:
            return self.id == other.id and self.region == self.region
        if type(other) == int:
            return self.id == other
        return NotImplemented