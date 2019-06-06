from . import ActiveSkill 
from ..skill_loader import SkillLoader
from ..region import Region

class RecoverAS(ActiveSkill):
    _handle_types = {7,8,117,145,179}

    def parse_args(self):
        self.card_bind = 0
        self.awoken_bind = 0
        self.hp = 0
        self.percentage_max_hp = 0.0
        self.rcv_multiplier_as_hp = 0.0
        self.team_rcv_multiplier_as_hp = 0.0
        self.auto_recover_buff_duration = 0
        self.auto_recover_buff_percentage_max_hp = 0.0

        if self.internal_skill_type == 7:
            self.rcv_multiplier_as_hp = self.args[0] / 100

        elif self.internal_skill_type == 8:
            self.hp = self.args[0]

        elif self.internal_skill_type == 117:
            self.card_bind = self.args[0]
            self.rcv_multiplier_as_hp = self.args[1] / 100
            self.hp = self.args[2]
            self.percentage_max_hp = self.args[3] / 100
            self.awoken_bind = self.args[4]

        elif self.internal_skill_type == 145:
            self.team_rcv_multiplier_as_hp = self.args[0] / 100

        elif self.internal_skill_type == 179:
            self.auto_recover_buff_duration = self.args[0]
            # self.args[1] unused?
            self.auto_recover_buff_percentage_max_hp = self.args[2] / 100
            self.card_bind = self.args[3]
            self.awoken_bind = self.args[4]

    def args_to_json(self):
        return {
            'card_bind': self.card_bind,
            'awoken_bind': self.awoken_bind,
            'hp': self.hp,
            'percentage_max_hp': self.percentage_max_hp,
            'rcv_multiplier_as_hp': self.rcv_multiplier_as_hp,
            'team_rcv_multiplier_as_hp': self.team_rcv_multiplier_as_hp,
            'auto_recover_buff_duration': self.auto_recover_buff_duration,
            'auto_recover_buff_percentage_max_hp': self.auto_recover_buff_percentage_max_hp,
        }

    def localize(self):
        recovers = []
        if self.auto_recover_buff_duration > 0: # TODO rework wording
            recovers.append(f"{self.auto_recover_buff_percentage_max_hp*100}% max HP for {'1 turn' if self.auto_recover_buff_duration == 1 else f'{self.auto_recover_buff_duration} turns'}")
        if self.card_bind > 0:
            recovers.append(f"{'1 turn' if self.card_bind == 1 else str(self.card_bind)+' turns'} of card binds")
        if self.awoken_bind > 0:
            recovers.append(f"{'1 turn' if self.awoken_bind == 1 else str(self.awoken_bind)+' turns'} of awoken skill binds")
        if self.hp > 0:
            recovers.append(f"{self.hp} HP")
        if self.percentage_max_hp > 0.0:
            recovers.append(f"{self.percentage_max_hp}% max HP")
        if self.rcv_multiplier_as_hp > 0.0:
            recovers.append(f"{self.rcv_multiplier_as_hp}x RCV as HP")
        if self.team_rcv_multiplier_as_hp > 0.0:
            recovers.append(f"{self.team_rcv_multiplier_as_hp}x team RCV as HP")
        return f"Recover {', '.join(r for r in recovers)}"
        
    @property
    def active_skill_type(self):
        return 'recover'


# Register the active skill
SkillLoader._register_active_skill_class(RecoverAS)