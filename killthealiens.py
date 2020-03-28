#! /usr/bin/env python
from moveableobject import MoveableObject
from enemy import Enemy
from bullet import Bullet
from player import Player
from statusmodifiers import *
from boss import Boss
from utilfuncs import switch, toframes, collide
from constants import *
from loadstaticres import *
from queue import Queue
import pygame
import sys
import random


# queues for input events
player_input_queue = Queue()
game_mgmt_queue = Queue()

# well, we added music but it makes the game hang :\
# these two lines before pygame.init() fix hang problem slightly, but don't completely fix
# may have to somehow run mixer in a separate process
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

pygame.init()

speedupstarttime = -1
moregunsstarttime = -1

# set up window
screen = pygame.display.set_mode((SCREENW, SCREENH), pygame.DOUBLEBUF)
pygame.display.set_caption("KILL THE ALIENS")

# image conversions
map_bg = background.convert()
bulletimg = bulletimg.convert()     # todo: change name

# set text font
myfont = pygame.font.SysFont("monospace", 15)

# load up music
pygame.mixer.music.load(BG_MUSIC_FNAME)

# actually transparent square
blacksquare = pygame.Surface((explosion[0].get_width() - 15, explosion[0].get_height() - 15), pygame.SRCALPHA, 32)

# set up game objects
ship = Player(shipimg, player_input_queue)
# sprite groups
saucers = []
bullets = []
statmods = []  # for power ups and booby traps
# gone = False
# killed = pygame.sprite.Group()

# test power up
# statmods.append(OneUp(oneupimg))

# create enemies
for x in range(0, 3):
    saucers.append(Enemy(random.randrange(0, SCREENW), random.randrange(0, 100), saucerimg))

# create boss
boss = Boss(100, -1200, bossimg, 0)

# create boss explosions
# maybe move this later in the code and don't create it in memory until we need it
boom = []
boom.append(MoveableObject(0, 0, pygame.Surface((1, 1))))

clock = pygame.time.Clock()

bgoffset = 0
FPS = 30

# flags
# 0 means play, 1 means user exit, 2 means death, 3 means victory
endgame = 0
# 0 means no boss, 1 means clear out shop for boss, 2 means boss entering,
# 3 means boss is out, 4 means dying, 5 means dead
BEASTMODE = 0

# most saucers that can be in play before boss comes out
MAXENEMIES = 10  # default 10

BLACK = (0, 0, 0)
blacksquare.fill(BLACK)

score = 0
time = 0  # total play time
endtime = 0

changeover = 0  # for scroll change over
ychng = 0

# print saucers
deadindex = -10

intro = 1

# opening screen
while intro == 1:
    screen.fill(BLACK)
    screen.blit(introscreen, (0, 0))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if not hasattr(event, 'key'): continue
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN: intro = 0

# start music on endless loop
pygame.mixer.music.play(-1)

# begin main game loop
# this should have all been put in a function T_T
while endgame == 0:
    ticktime = clock.tick(FPS)  # update time in milliseconds
    time += ticktime

    # add more saucers to increase difficulty as time goes on
    # number of saucers is a function of time
    if len(saucers) - 3 < time / 12000 and BEASTMODE == 0:
        # print len(saucers)
        # print time/6000
        saucers.append(Enemy(random.randrange(0, SCREENW), random.randrange(-200, -50), saucerimg))
    # if(time >= 8000 and len(saucers) < 5):
    # saucers.append(Enemy(random.randrange(0, SCREENW), random.randrange(-200, -50), saucerimg))

    # determine if we should have a status modifier
    # so apparently there's no switch/case in python >_>
    # choose a random number, determine which powerup based on number, if not 1 - 6 just continue on w/ no stat mod
    for case in switch(random.randrange(0, 2201)):  # figure out the right number for this, maybe 2201
        if case(1):
            statmods.append(OneUp(oneupimg))
        elif case(90):
            statmods.append(Bomb(bombimg))
        elif case(1337) or case(219):  # to make it more likely
            statmods.append(SpeedUp(speedupimg))
        elif case(511) or case(2000):
            statmods.append(MoreGuns(moregunsimg))
        # moregunsstarttime = time

    # ENTER THE BOSS
    if len(saucers) > MAXENEMIES:  # change that number for max saucers on screen - default 10
        BEASTMODE = 1
    # del saucers[:]		#this removes the whole list

    for event in pygame.event.get():
        if event.type == pygame.QUIT: endgame = 1
        elif not hasattr(event, 'key'): continue
        elif event.key == pygame.K_ESCAPE: endgame = 1
        elif event.key == pygame.K_SPACE and ship.active:
            bullets.append(ship.fire(bulletimg))
            if ship.bamfmode:
                bullets.append(ship.fire(bulletimg, LEFT))
                bullets.append(ship.fire(bulletimg, RIGHT))
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            player_input_queue.put(event)

    ship.update()

    if BEASTMODE == 3:  # if boss is out
        if boss.infirerange(ship) > 0:
            if random.randrange(0, 10) == 1 and ship.exploding == -1:  # and if ship is not exploding
                bullets.append(boss.fire(bulletimg, LEFT))
            if random.randrange(0, 10) == 1 and ship.exploding == -1:
                bullets.append(boss.fire(bulletimg, RIGHT))
            # elif(random.randrange(0,20) == 1):
            #	bullets.append(boss.fire(bulletimg, LEFT))
            #	bullets.append(boss.fire(bulletimg, RIGHT))

            # potentially better collision detection
            # for bullet in bullets:
            # bullet.move()
            # pygame.sprite.spritecollide(bullet, saucers, 1)
            # if killed:
            # print killed
            # print saucers
    # this may be movable to the next iteration through the saucers
    for saucer in saucers:
        dietest = saucer.move(BEASTMODE)
        if dietest == 1:
            deadindex = saucers.index(saucer)

    # move bullets, check for collisions with player or boss or off screen
    # explosions as well
    # just an iteration through all bullets
    for bullet in bullets:
        bullet.move()
        # -60 to go a little off screen, for high up explosions
        if bullet.y < -60 or bullet.y > SCREENH: bullet.active = False
        if collide(ship, bullet) and bullet.dir != UP:
            ship.die()
            bullet.active = False
        elif BEASTMODE == 3 and collide(boss, bullet):
            boss.health -= 5
            if boss.health <= 0:
                boss.die()
                BEASTMODE += 1
            bullet.active = False
        if -1 < bullet.exploding < 4: bullet.explode(time)
        if bullet.active == False: bullets.remove(bullet)

    # maybe it would be best to have a section just to handle explosions across the board
    # perhaps an explosion object, eg just kill the sprite and have explosion obj take over

    # print "Boss Health: " + str(boss.health)
    # just for kicks
    # inefficient collision detection
    # but it works for now
    for saucer in saucers:
        if collide(saucer, ship) and saucer.exploding == -1:
            ship.die()
            saucer.explode(time)
        # saucer.respawn()
        # if ship.health <= 0: endgame = 0	#change to 2 for kill
        elif -1 < saucer.exploding < 4:
            if saucer.explode(time):
                # if we are finished exploding, reset
                saucer.respawn()
                saucer.image = saucerimg
                saucer.exploding = -1
                saucer.active = True
            # print "done exploding"

        # print saucer.exploding

        for bullet in bullets:
            if collide(saucer, bullet):
                bullet.x = saucer.x
                bullet.y = saucer.y
                bullet.updatepos()
                # respawn saucer off screen and increment score
                if BEASTMODE != 1:
                    saucer.respawn()
                else:
                    deadindex = saucers.index(saucer)
                    dietest = 1
                bullet.explode(time)
                # saucers.remove(saucer)		#this removes the actual object from the list
                score += 5
        if saucer.active == False: saucer.respawn()

    # handle status modifiers
    modRMindex = []
    for mod in statmods:
        if collide(ship, mod):  # if we collect the modifier
            modID = mod.payload(ship)
            if modID == 1:
                speedupstarttime = time
                SCROLLSPEED = 7
            elif modID == 2:
                moregunsstarttime = time
            modRMindex.append(statmods.index(mod))
        mod.move()
        if mod.y > SCREENH:  # if the modifier goes off screen
            modRMindex.append(statmods.index(mod))
    # remove obtained status modifiers
    for index in modRMindex: statmods.pop(index)
    modRMindex = []

    # this is so that we don't mess up the previous for iteration
    # remove saucers from array
    # I wonder if that bug is caused because only one saucer can die an iteration...
    if dietest == 1:
        saucers.pop(deadindex)
        dietest = 0
        # print "LEN " + str(len(saucers))
        if len(saucers) == 0:
            BEASTMODE = 2
            boss.inittime = time

    # for final player death
    if ship.health <= 0 and endtime == 0:
        endtime = time

    if ship.active == False:
        doneExploding = ship.explode(time)
        # print doneExploding
        if doneExploding:
            ship.respawn(shipimg)
            SCROLLSPEED = NORMSCROLLSPEED
            ship.bamfmode = False

        #		if(endtime == 0):
        #			endtime = time
    # for time delay after death
    if time >= endtime + 4000 and endtime != 0:
        # print "game over"
        endgame = 2

    # if boss got killed make Sonic style boss death explosion
    # explode is called multiple times over several main loops to advance the explosion frame
    if BEASTMODE == 4:
        for splat in boom:
            # if first pass, initialize explosion sequence
            if (len(boom) == 1 and splat.exploding == -1):
                splat.x = random.randrange(boss.x, boss.x + boss.width - explosion[
                    0].get_width())  # subtract explosion width
                splat.y = random.randrange(boss.y, boss.y + boss.height - explosion[0].get_height())
                explosion.append(blacksquare)  # to take chunks out of boss
            splat.explode(time)
        if boom[-1].exploding == 2 and len(boom) < 8:
            boom.append(MoveableObject(random.randrange(boss.x, boss.x + boss.width - explosion[0].get_width()),
                                           random.randrange(boss.y,
                                                            boss.y + boss.height - explosion[0].get_height()),
                                           pygame.Surface((1, 1))))
        # if boss is done exploding
        if len(boom) == 8 and boom[-1].exploding == len(explosion):
            BEASTMODE = 5
            score += 1000
            endtime = time
        # print "BEASTMODE 5"

    # if(boom[7].exploding == 4):
    #	endtime = time
    #	BEASTMODE = 5
    # meh inefficient
    # this may have to be reexamined, testing beastmode < 3
    if boss.y > 0 and BEASTMODE < 3: BEASTMODE = 3

    # if boss is displayed
    if 4 > BEASTMODE >= 2:
        boss.move(ship, time)
        # if ship collides with boss, lose life
        if collide(ship, boss):
            # print "boss collision"
            ship.die()  # evaluation of death is earlier in the code

    # power up (speed) deactivation
    # print time
    # print speedupstarttime
    # print time - speedupstarttime
    if speedupstarttime > 0 and ((time - speedupstarttime) > 15000):  # or ship exploding
        # print "Speed Reset"
        ship.speed = 5
        SCROLLSPEED = NORMSCROLLSPEED
        speedupstarttime = -1
    # more guns deactivation
    if moregunsstarttime > 0 and ((time - moregunsstarttime) > 15000):
        # print "Gun Reset"
        ship.bamfmode = False
        moregunsstarttime = -1

    # text rendering
    healthlbl = myfont.render("Health: " + str(ship.health), 1, (255, 255, 0))
    scorelbl = myfont.render("Score: " + str(score), 1, (255, 255, 0))
    bosslbl = myfont.render("Boss Health: " + str(boss.health), 1, (255, 255, 0))

    # render images

    screen.fill(BLACK)

    # for seamless vertical scrolling
    if changeover == 0:
        screen.blit(map_bg, (0, 0), (0, 2000 - SCREENH - bgoffset, SCREENW, 2000 - bgoffset))
    elif changeover == 1:
        # print "ychng: " + str(ychng)
        # print "bgoffset: " + str(bgoffset)
        screen.blit(map_bg, (0, 0), (0, map_bg.get_height() - ychng, SCREENW, 2000))
        screen.blit(map_bg, (0, ychng), (0, 0, SCREENW, SCREENH - ychng))

    if BEASTMODE >= 2: screen.blit(boss.image, (boss.x, boss.y))
    screen.blit(ship.image, (ship.x, ship.y))  # this should probably be rendered last for overlap reasons
    for saucer in saucers:
        screen.blit(saucer.image, (saucer.x, saucer.y))

    # power up rendering
    for mod in statmods:
        screen.blit(mod.image, (mod.x, mod.y))

    for bullet in bullets:
        screen.blit(bullet.image, (bullet.x, bullet.y))
    if BEASTMODE >= 4:
        # if(boom[-1].exploding == 2):
        # print "blacksquare"
        # boss.image.blit(blacksquare, (boom[-1].x, boom[-1].y))
        for splat in boom:
            screen.blit(splat.image, (splat.x, splat.y))
    # screen.blit(explosion[explframe], (SCREENW/2, SCREENH/2))
    screen.blit(healthlbl, (SCREENW - 100, 20))
    screen.blit(scorelbl, (SCREENW - 100, 35))
    if BEASTMODE >= 3: screen.blit(bosslbl, (SCREENW / 2, 20))

    # for i in range(0,5):
    # screen.blit(explosion[i], (i*120, 300))

    pygame.display.flip()  # apply double buffer

    # if(explframe > 3): explframe=0
    # else: explframe += 1

    # change offset for vertical scroll
    if bgoffset > 2000:
        bgoffset = 0
        changeover = 0
        ychng = 0
    else:
        bgoffset += SCROLLSPEED

    if 2000 >= bgoffset > 2000 - SCREENH:
        ychng += SCROLLSPEED
        changeover = 1
    # print "time: " + str(time)
    # print "health: " + str(ship.health)
    # print "score: " + str(score)

    # debug messages
    # print "ship speed = " + str(ship.speed)
    # print "SCROLLSPEED = " + str(SCROLLSPEED)

# end game loop

# display end screens
if BEASTMODE == 5:
    disp = pygame.image.load("victory1.png")
else:
    disp = pygame.image.load("dead1.png")

# add loop to get input, continue to high scores, etc
cont = 0
while cont == 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: cont = 1
        if not hasattr(event, 'key'): continue
        if event.key == pygame.K_ESCAPE: cont = 1
    screen.blit(disp, (0, 0))
    pygame.display.flip()
# elif(endgame == 1): continue

# update and view high scores
# open file
# scores = []
# f = open('scores', 'rw')
# for line in f:
#	scores.append(line)
# print scores
# read scores into list
# compare score to list
# display high scores


pygame.quit()
sys.exit()
