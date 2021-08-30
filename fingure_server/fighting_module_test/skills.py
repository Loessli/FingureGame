
class Skill(object):
    skill_type: int = None
    """1 -> physics; 2-> magic"""

    skill_num: int = None
    """1 -> small skill, 2 -> ultimate skill"""

    skill_rate: float = None
    """rate for skill 1"""

    skill_range: int = None
    """how many enemies hit"""

    skill_effect: float = None
    """skill damage multiply"""

    def __init__(self, skill_type, skill_num, skill_rate, skill_range, skill_effect):
        self.skill_type = int(skill_type)
        self.skill_num = int(skill_num)
        self.skill_rate = float(skill_rate)
        self.skill_range = int(skill_range)
        self.skill_effect = float(skill_effect)
