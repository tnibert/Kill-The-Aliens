from gamestrategy import Strategy
from enemy import Enemy
from gamemap import GameMap
from statusmodifiers import OneUp, Bomb, SpeedUp, MoreGuns
from utilfuncs import switch
from player import Player
from loadstaticres import *
import random


class Level(Strategy):
    def __init__(self, scene, inputqueue):
        super().__init__(scene)
        # set up game objects
        self.ship = Player(shipimg, inputqueue)
        self.scene.attach(self.ship)
        # enable firing of bullets
        self.ship.subscribe("fire", lambda ev: self.scene.attach(ev.kwargs.get("bullet")))

        # set up map
        map_bg = background.convert()
        self.game_map = GameMap(map_bg)
        self.scene.attach(self.game_map)

    def run_game(self):
        # determine if we should have a status modifier
        # so apparently there's no switch/case in python >_>
        # choose a random number, determine which powerup based on number, if not 1 - 6 just continue on w/ no stat mod
        for case in switch(random.randrange(0, 10000)):
            statmod = None
            if case(1):
                statmod = OneUp(oneupimg)
            elif case(90):
                statmod = Bomb(bombimg)
            elif case(1337):
                statmod = SpeedUp(speedupimg)
                statmod.subscribe("collision", self.game_map.receive_signals)
            elif case(511):
                statmod = MoreGuns(moregunsimg)
            if statmod is not None:
                # todo: make the receiving function more specific
                print("statmod created")
                statmod.subscribe("collision", self.ship.receive_signals)
                self.scene.attach(statmod)
        super().run_game()
