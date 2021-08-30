from random import randint
from .hero_info import HeroInfo


class Hero(object):
    def __init__(self, hero_info: HeroInfo):
        self.hero_info = hero_info

    def attacked(self, target_hero, hit_type: int = 3):
        """hit_type. 1->skill2, 2->skill1, 3->normal att"""
        damage = -1
        if self.hero_info.hero_type == 1:
            if hit_type == 1:
                damage = self.hero_info.att * self.hero_info.skill2.skill_effect - target_hero.hero_info.defence
            elif hit_type == 2:
                damage = self.hero_info.att * self.hero_info.skill1.skill_effect - target_hero.hero_info.defence
            elif hit_type == 3:
                damage = self.hero_info.att - target_hero.hero_info.defence
        elif self.hero_info.hero_type == 2:
            if hit_type == 1:
                damage = self.hero_info.magic_att * self.hero_info.skill2.skill_effect - \
                         target_hero.hero_info.magic_defence
            elif hit_type == 2:
                damage = self.hero_info.magic_att * self.hero_info.skill1.skill_effect - \
                         target_hero.hero_info.magic_defence
            elif hit_type == 3:
                damage = self.hero_info.magic_att - target_hero.hero_info.magic_defence
        if damage >= 0:
            target_hero.get_damage(damage)

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