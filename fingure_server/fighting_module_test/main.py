from fighting_module_test.heros import Hero
from fighting_module_test.hero_info import HeroInfo
from fighting_module_test.round_manager import RoundManger
from fighting_module_test.lib import loading_hero_info_config_by_id, loading_csv_config


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


if __name__ == '__main__':
    csv_data = loading_csv_config("hero_info.csv")
    hero_info1 = loading_hero_info_config_by_id(csv_data, 1)
    hero_info2 = loading_hero_info_config_by_id(csv_data, 2)
    player1 = Player('player 1', Warrior(hero_info1))
    player2 = Player('player 2', Magic(hero_info2))
    RoundManger(player1, player2).start_fight()