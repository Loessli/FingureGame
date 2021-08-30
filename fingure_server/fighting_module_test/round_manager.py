from .heros import Hero


class RoundManger(object):
    winner = None

    def __init__(self, _player1, _player2):
        self.player1 = _player1
        self.player2 = _player2
        self.round = 1
        self.result = False

    def start_fight(self):
        while not self.winner:
            self.execute_round()
        if isinstance(self.winner, str):
            msg = f"winner is {self.winner}, total round is {self.round}"
        else:
            msg = f"winner is {self.winner.name}, total round is {self.round}"
        print(msg)
        print('player1 hp -> ', self.player1.hero.hero_info.hp, 'player2 hp -> ', self.player2.hero.hero_info.hp)

    def execute_round(self):
        if not self.fighting_single_round():
            self.round += 1

    def fighting_single_round(self):
        """单回合fight"""
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
        if _hero1.is_skill2():
            _hero1.attacked(_hero2, 1)
        elif _hero1.is_skill1():
            _hero1.attacked(_hero2, 2)
        else:
            _hero1.attacked(_hero2)
        return self.check_result()

    def check_result(self):
        state1 = self.player1.hero.check_state()
        state2 = self.player2.hero.check_state()

        if state1 and state2:
            self.winner = "?????????"
        elif not state1 and state2:
            self.winner = self.player1
        elif state1 and state2:
            self.winner = self.player2