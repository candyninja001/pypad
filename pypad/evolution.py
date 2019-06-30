from collections import defaultdict

class Evolution:
    def __init__(self, raw_card):
        self.result_monster_id = raw_card[0]
        self.is_ultimate = raw_card[4] == 1
        self.base_monster_id = raw_card[40]
        self.materials = [raw_card[i] for i in range(41,46) if raw_card[i] != 0]
        self.reverse_materials = [raw_card[i] for i in range(46,51)]
    
    def to_json(self) -> dict:
        return {
            'base_monster_id': self.base_monster_id,
            'result_monster_id': self.result_monster_id,
            'materials': self.materials,
            'reverse_materials': self.reverse_materials,
            'is_ultimate': self.is_ultimate,
        }

class EvolutionManager:
    def __init__(self):
        # Map monster ids to the evolution that yields the monster
        self._evolution_to = {}
        # Map base monster ids to the set of possible evolution monster ids
        self._ids_from = defaultdict(set)

    def _register(self, evolution):
        # only add actual evolutions
        if evolution.base_monster_id != 0:
            from_id = evolution.base_monster_id
            to_id = evolution.result_monster_id
            self._evolution_to[to_id] = evolution
            self._ids_from[from_id].add(to_id)

    # Returns the evolution that reaches the monster
    def evolution_to_id(self, to_id):
        if to_id not in self._evolution_to:
            return None
        return self._evolution_to

    # Returns the possible evolutions for this monster
    def evolutions_from_id(self, from_id):
        if from_id not in self._ids_from:
            return set()
        return {self._evolution_to[to_id] for to_id in self._ids_from[from_id]}

    def to_json(self):
        return {str(to_id):evo.to_json() for to_id,evo in self._evolution_to.items()}

    def __len__(self):
        return len(self._evolution_to)