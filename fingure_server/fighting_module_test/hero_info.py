from .skills import Skill


def change_type_int(before):
    return int(before)


class HeroInfo(object):
    hero_type: int = None
    """1 -> physics, 2 -> magic"""

    lv: int = None
    """hero level"""

    att: int = None
    """hero physical attack number"""

    magic_att: int = None
    """hero magic attack number"""

    defence: int = None
    """hero physical defence number"""

    magic_defence: int = None

    hp: int = None

    mp: int = None

    speed: int = None

    skill1: Skill = None
    """ small skill"""

    skill2: Skill = None
    """ ultimate skill """

    def __init__(self, ctor_data: dict):
        self.hero_type = change_type_int(ctor_data["hero_type"])
        self.lv = change_type_int(ctor_data["lv"])
        self.att = change_type_int(ctor_data["att"])
        self.magic_att = change_type_int(ctor_data["magic_att"])
        self.defence = change_type_int(ctor_data["defence"])
        self.magic_defence = change_type_int(ctor_data["magic_defence"])
        self.hp = change_type_int(ctor_data["hp"])
        self.mp = change_type_int(ctor_data["mp"])
        self.speed = change_type_int(ctor_data["speed"])
        self.skill1: Skill = ctor_data["skill1"]
        self.skill2: Skill = ctor_data["skill2"]
