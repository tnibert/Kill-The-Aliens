from moveableobject import MoveableObject
from enemy import Enemy
from bullet import Bullet
from player import Player
from statusmodifiers import *
from boss import Boss
from utilfuncs import switch, toframes, collide
from constants import *
from loadstaticres import explosion


# so, for the player to explode
# make die() method decrement health*
# make all areas that currently decrement health call die() instead*
# and make them all check for explosion happening
# make self.active == False trigger explosion unless explosion already happening
# once we are exploding and frame has reached last explosion frame
#	respawn() ship at start coordinates
