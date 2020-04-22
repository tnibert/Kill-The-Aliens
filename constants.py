from pygame import font

SCREENH = 800
SCREENW = 640
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3
BLACK = (0, 0, 0)

BOSSHEALTH = 300
PLAYERHEALTH = 3

# speed of map scrolling
SCROLLSPEED = 30
MAXSCROLLSPEED = 180

STATMOD_DURATION = 15   # seconds

PLAYERSPEED = 150
PLAYERMAXSPEED = 270

BULLETSPEED = 300
STATMOD_SPEED = 90

EXPLOSION_FRAME_UPDATE_WAIT = 0.2       # time between explosion frames in seconds

NEW_SAUCER_IVAL = 15
# most saucers that can be in play before boss comes out
# todo: if this value is set to 3, then boss appears from bottom and no saucers appear on seconds level
SAUCER_THRESHOLD = 10

BOSS_SPEED = 70
NUM_BOSS_EXPLOSIONS = 10

VAL_TEXT_SIZE = 20

SAUCER_DEATH_SCORE_INC = 5

# todo: improve font and color
VAL_FONT = font.SysFont("monospace", VAL_TEXT_SIZE)

TEXTCOLOR = (255, 255, 0)

VAL_X_LOC = 10
VAL_Y_LOC_START = 20
