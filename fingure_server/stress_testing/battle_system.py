from random import randint


class Skill(object):
    def __init__(self, skill_type, skill_num, skill_rate, skill_round, skill_effect):
        self.skill_type = skill_type
        self.skill_num = skill_num
        self.skill_rate = skill_rate
        self.skill_round = skill_round
        self.skill_effect = skill_effect


class HeroInfo(object):

    def __init__(self, hero_type, lv, att, magic_att, defence, magic_defence, hp, mp, speed, skill1, skill2):
        self.hero_type = hero_type
        self.lv = lv
        self.att = att
        self.magic_att = magic_att
        self.defence = defence
        self.magic_defence = magic_defence
        self.hp = hp
        self.mp = mp
        self.speed = speed
        self.skill1: Skill = skill1
        self.skill2: Skill = skill2


class Hero(object):
    def __init__(self, hero_info: HeroInfo):
        self.hero_info = hero_info

    def be_attacked(self, _hero):
        if _hero.hero_type == 1:
            if _hero.is_skill2():
                damage = _hero.hero_info.att * _hero.hero_info.skill2.skill_effect - self.hero_info.defence
            elif _hero.is_skill1():
                damage = _hero.hero_info.att * _hero.hero_info.skill1.skill_effect - self.hero_info.defence
            else:
                damage = _hero.hero_info.att - self.hero_info.defence
            if damage >= 0:
                self.get_damage(damage)
        elif _hero.hero_type == 2:
            if _hero.is_skill2():
                damage = _hero.hero_info.magic_att * _hero.hero_info.skill2.skill_effect - self.hero_info.magic_defence
            elif _hero.is_skill1():
                damage = _hero.hero_info.magic_att * _hero.hero_info.skill1.skill_effect - self.hero_info.magic_defence
            else:
                damage = _hero.hero_info.magic_att - self.hero_info.magic_defence
            if damage >= 0:
                self.get_damage(damage)

    def get_damage(self, damage: int):
        self.hero_info.hp -= damage

    def check_state(self):
        return self.hero_info.hp <= 0

    def is_skill1(self):
        return (randint(0, 10000) / 10000) >= self.hero_info.skill1.skill_rate

    def is_skill2(self):
        if self.hero_info.mp >= 100:
            # 清空能量
            self.hero_info.mp = 0
            return True


class Warrior(Hero):
    def __int__(self, hero_info: HeroInfo):
        super().__init__(hero_info)
        self.hero_info.hero_type = 1


class Magic(Hero):
    def __int__(self, hero_info: HeroInfo):
        super().__init__(hero_info)
        self.hero_info.hero_type = 2


class Player(object):
    def __init__(self, name: str, hero: Hero):
        self.name = name
        self.hero = hero


class RoundManger(object):
    winner = None

    def __init__(self, _player1: Player, _player2: Player):
        self.player1 = _player1
        self.player2 = _player2
        self.round = 1
        self.result = False

    def start_fight(self):
        while not self.winner:
            self.execute_round()
        print(self.winner.name, self.round)

    def execute_round(self):
        if not self.fighting():
            self.round += 1

    def fighting(self):
        hero1 = self.player1.hero
        hero2 = self.player2.hero
        if hero1.hero_info.speed >= hero2.hero_info.speed:
            if self.player_fight(hero1, hero2):
                return True
            if self.player_fight(hero2, hero1):
                return True
        else:
            if self.player_fight(hero2, hero1):
                return True
            if self.player_fight(hero1, hero2):
                return True

    def player_fight(self, _hero1: Hero, _hero2: Hero):
        if _hero1.hero_info.hero_type == 1:
            if _hero1.is_skill2():
                damage = _hero1.hero_info.att * _hero1.hero_info.skill2.skill_effect - _hero2.hero_info.defence
            elif _hero1.is_skill1():
                damage = _hero1.hero_info.att * _hero1.hero_info.skill1.skill_effect - _hero2.hero_info.defence
            else:
                damage = _hero1.hero_info.att - _hero2.hero_info.defence
            if damage >= 0:
                _hero2.get_damage(damage)
        elif _hero1.hero_info.hero_type == 2:
            if _hero1.is_skill2():
                damage = _hero1.hero_info.magic_att * _hero1.hero_info.skill2.skill_effect - _hero2.hero_info.magic_defence
            elif _hero1.is_skill1():
                damage = _hero1.hero_info.magic_att * _hero1.hero_info.skill1.skill_effect - _hero2.hero_info.magic_defence
            else:
                damage = _hero1.hero_info.magic_att - _hero2.hero_info.magic_defence
            if damage >= 0:
                _hero2.get_damage(damage)
        return self.check_result()

    def check_result(self):
        state1 = self.player1.hero.check_state()
        state2 = self.player2.hero.check_state()

        if state1 and state2:
            self.winner = Player("???", None)
        elif not state1 and state2:
            self.winner = self.player1
        elif state1 and state2:
            self.winner = self.player2


if __name__ == '__main__':
    player1 = Player('player1', Warrior(HeroInfo(
        hero_type=1, lv=1, att=2, magic_att=1, defence=1, magic_defence=1, hp=100, mp=1, speed=5,
        skill1=Skill(
            skill_type=2,
            skill_num=1,
            skill_rate=0.75,
            skill_round=1,
            skill_effect=1.3
        ),
        skill2=Skill(
            skill_type=2,
            skill_num=1,
            skill_rate=0.75,
            skill_round=1,
            skill_effect=5.3
        )
    )))
    player2 = Player('player2', Magic(HeroInfo(
        hero_type=2, lv=1, att=1, magic_att=3, defence=1, magic_defence=1, hp=100, mp=1, speed=3,
        skill1=Skill(
            skill_type=2,
            skill_num=1,
            skill_rate=0.75,
            skill_round=1,
            skill_effect=3.3
        ),
        skill2=Skill(
            skill_type=2,
            skill_num=1,
            skill_rate=0.75,
            skill_round=1,
            skill_effect=5.3
        )
    )))

    print(player1.hero.hero_info.hero_type)

    round_manager = RoundManger(player1, player2)
    round_manager.start_fight()