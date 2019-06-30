import abc

# Interface for leader skills consisting of multiple leader skill components
class MultiSkillLSI(abc.ABC):
    @abc.abstractmethod
    def get_sub_skills(self) -> 'tuple of skill_id':
        pass