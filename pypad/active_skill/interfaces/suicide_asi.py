import abc

# Interface for active skills consisting of multiple active skill components
class SuicideASI(abc.ABC):
    def is_suicide(self) -> bool:
        return True

    # What percentage of player HP remains after the suicide
    def get_suicide_percentage(self) -> float:
        return 1.0