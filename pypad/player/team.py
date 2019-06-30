

class Team:
    def __init__(self, raw_team):
        self.leader = raw_team[0]
        self.subs = raw_team[1:5]
        self.badge = raw_team[5] # TODO create Badge enum
        self.helper = raw_team[6]
        # 7 - 8 unknown, one should be orb skin