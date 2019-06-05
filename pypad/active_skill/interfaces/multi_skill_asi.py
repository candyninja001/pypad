import abc

# Interface for active skills consisting of multiple active skill components
class MultiSkillASI(abc.ABC):
    @abc.abstractmethod
    def get_sub_skills(self) -> 'tuple of skill_id':
        pass