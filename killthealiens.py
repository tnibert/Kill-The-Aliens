#! /usr/bin/env python
import pygame
# from pygame.locals import *
import sys
import obj
import random

# well, we added music but it makes the game hang :\

# these two lines before pygame.init() fix hang problem slightly, but don't completely fix
# may have to somehow run mixer in a separate process
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

pygame.init()

# speed of map scrolling
NORMSCROLLSPEED = 2
SCROLLSPEED = 2

speedupstarttime = -1
moregunsstarttime = -1

# set up window
screen = pygame.display.set_mode((obj.SCREENW, obj.SCREENH), pygame.DOUBLEBUF)
pygame.display.set_caption("KILL THE ALIENS")

# set text font
myfont = pygame.font.SysFont("monospace", 15)

# create singleton images for efficiency
shipimg = pygame.image.load("spaceship1.png")
saucerimg = pygame.image.load("saucer1.png")
bulletimg = pygame.image.load("bullet1.png").convert()
bossimg = pygame.image.load("invader2.png")

# status modifier images
# using same image for now, to change
oneupimg = pygame.image.load("plus102.png")
bombimg = pygame.image.load("bomb.png")
speedupimg = pygame.image.load("speed.png")
moregunsimg = pygame.image.load("guns.png")

# load up music
pygame.mixer.music.load("spectre.mp3");

# actually transparent square
blacksquare = pygame.Surface((obj.explosion[0].get_width() - 15, obj.explosion[0].get_height() - 15), pygame.SRCALPHA,
                             32)

# set up game objects
ship = obj.Player(shipimg)
# sprite groups
saucers = []
bullets = []
statmods = []  # for power ups and booby traps
# gone = False
# killed = pygame.sprite.Group()

# test power up
# statmods.append(obj.OneUp(oneupimg))

# create enemies
for x in range(0, 3):
    saucers.append(obj.Enemy(random.randrange(0, obj.SCREENW), random.randrange(0, 100), saucerimg))

# create boss
boss = obj.Boss(100, -1200, bossimg, 0)

# create boss explosions
# maybe move this later in the code and don't create it in memory until we need it
boom = []
boom.append(obj.MoveableObject(0, 0, pygame.Surface((1, 1))))

clock = pygame.time.Clock()
bg = pygame.image.load("map1.png").convert()
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

# for more precise keyboard input
goright = False
goleft = False
goup = False
godown = False

# print saucers
deadindex = -10

intro = 1
introscreen = pygame.image.load("intro1.png")

# opening screen
while (intro == 1):
    screen.fill(BLACK)
    screen.blit(introscreen, (0, 0))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if not hasattr(event, 'key'): continue
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_RETURN): intro = 0

# start music on endless loop
pygame.mixer.music.play(-1)

# begin main game loop
# this should have all been put in a function T_T
while (endgame == 0):
    ticktime = clock.tick(FPS)  # update time in milliseconds
    time += ticktime

    # add more saucers to increase difficulty as time goes on
    # number of saucers is a function of time
    if (len(saucers) - 3 < time / 12000 and BEASTMODE == 0):
        # print len(saucers)
        # print time/6000
        saucers.append(obj.Enemy(random.randrange(0, obj.SCREENW), random.randrange(-200, -50), saucerimg))
    # if(time >= 8000 and len(saucers) < 5):
    # saucers.append(obj.Enemy(random.randrange(0, obj.SCREENW), random.randrange(-200, -50), saucerimg))

    # determine if we should have a status modifier
    # so apparently there's no switch/case in python >_>
    # choose a random number, determine which powerup based on number, if not 1 - 6 just continue on w/ no stat mod
    for case in obj.switch(random.randrange(0, 2201)):  # figure out the right number for this, maybe 2201
        if case(1):
            statmods.append(obj.OneUp(oneupimg))
        elif case(90):
            statmods.append(obj.Bomb(bombimg))
        elif case(1337) or case(219):  # to make it more likely
            statmods.append(obj.SpeedUp(speedupimg))
        elif case(511) or case(2000):
            statmods.append(obj.MoreGuns(moregunsimg))
        # moregunsstarttime = time

    # ENTER THE BOSS
    if (len(saucers) > MAXENEMIES):  # change that number for max saucers on screen - default 10
        BEASTMODE = 1
    # del saucers[:]		#this removes the whole list

    # user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT: endgame = 1
        if not hasattr(event, 'key'): continue
        if event.key == pygame.K_ESCAPE: endgame = 1

        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_LEFT and ship.x >= 0):
                goleft = True
            elif (event.key == pygame.K_RIGHT and ship.x + ship.width <= obj.SCREENW):
                goright = True
            elif (event.key == pygame.K_UP and ship.y >= 0):
                goup = True
            elif (event.key == pygame.K_DOWN and ship.y + ship.height <= obj.SCREENH):
                godown = True

        if (event.type == pygame.KEYUP):
            if (event.key == pygame.K_LEFT):
                goleft = False
            elif (event.key == pygame.K_RIGHT):
                goright = False
            elif (event.key == pygame.K_UP):
                goup = False
            elif (event.key == pygame.K_DOWN):
                godown = False

        if (event.key == pygame.K_SPACE and ship.active):
            bullets.append(ship.fire(bulletimg))
            if (ship.bamfmode):
                bullets.append(ship.fire(bulletimg, obj.LEFT))
                bullets.append(ship.fire(bulletimg, obj.RIGHT))

    # for smoothness and border checks
    if (goright == True and ship.x + ship.width <= obj.SCREENW):
        ship.x += ship.speed
    elif (goleft == True and ship.x >= 0):
        ship.x -= ship.speed
    if (goup == True and ship.y >= 0):
        ship.y -= ship.speed
    elif (godown == True and ship.y + ship.height <= obj.SCREENH):
        ship.y += ship.speed

    ship.updatepos()

    if (BEASTMODE == 3):  # if boss is out
        if (boss.infirerange(ship) > 0):
            if (random.randrange(0, 10) == 1 and ship.exploding == -1):  # and if ship is not exploding
                bullets.append(boss.fire(bulletimg, obj.LEFT))
            if (random.randrange(0, 10) == 1 and ship.exploding == -1):
                bullets.append(boss.fire(bulletimg, obj.RIGHT))
            # elif(random.randrange(0,20) == 1):
            #	bullets.append(boss.fire(bulletimg, obj.LEFT))
            #	bullets.append(boss.fire(bulletimg, obj.RIGHT))

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
        # print "DEAD " + str(deadindex)

    # print "DEAD " + str(deadindex)
    # print "LEN " + str(len(saucers))

    # move bullets, check for collisions with player or boss or off screen
    # explosions as well
    # just an iteration through all bullets
    for bullet in bullets:
        bullet.move()
        # -60 to go a little off screen, for high up explosions
        if (bullet.y < -60 or bullet.y > obj.SCREENH): bullet.active = False
        if (obj.collide(ship, bullet) and bullet.dir != obj.UP):
            ship.die()
            bullet.active = False
        elif (BEASTMODE == 3 and obj.collide(boss, bullet)):
            boss.health -= 5
            if (boss.health <= 0):
                boss.die()
                BEASTMODE += 1
            bullet.active = False
        if (-1 < bullet.exploding < 4): bullet.explode(time)
        if (bullet.active == False): bullets.remove(bullet)

    # maybe it would be best to have a section just to handle explosions across the board
    # perhaps an explosion object, eg just kill the sprite and have explosion obj take over

    # print "Boss Health: " + str(boss.health)
    # just for kicks
    # inefficient collision detection
    # but it works for now
    for saucer in saucers:
        if (obj.collide(saucer, ship) and saucer.exploding == -1):
            ship.die()
            saucer.explode(time)
        # saucer.respawn()
        # if ship.health <= 0: endgame = 0	#change to 2 for kill
        elif (-1 < saucer.exploding < 4):
            if (saucer.explode(time)):
                # if we are finished exploding, reset
                saucer.respawn()
                saucer.image = saucerimg
                saucer.exploding = -1
                saucer.active = True
            # print "done exploding"

        # print saucer.exploding

        for bullet in bullets:
            if (obj.collide(saucer, bullet)):
                bullet.x = saucer.x
                bullet.y = saucer.y
                bullet.updatepos()
                # respawn saucer off screen and increment score
                if (BEASTMODE != 1):
                    saucer.respawn()
                else:
                    deadindex = saucers.index(saucer)
                    dietest = 1
                bullet.explode(time)
                # saucers.remove(saucer)		#this removes the actual object from the list
                score += 5
        if (saucer.active == False): saucer.respawn()

    # handle status modifiers
    modRMindex = []
    for mod in statmods:
        if (obj.collide(ship, mod)):  # if we collect the modifier
            modID = mod.payload(ship)
            if modID == 1:
                speedupstarttime = time
                SCROLLSPEED = 7
            elif modID == 2:
                moregunsstarttime = time
            modRMindex.append(statmods.index(mod))
        mod.move()
        if (mod.y > obj.SCREENH):  # if the modifier goes off screen
            modRMindex.append(statmods.index(mod))
    # remove obtained status modifiers
    for index in modRMindex: statmods.pop(index)
    modRMindex = []

    # this is so that we don't mess up the previous for iteration
    # remove saucers from array
    # I wonder if that bug is caused because only one saucer can die an iteration...
    if (dietest == 1):
        saucers.pop(deadindex)
        dietest = 0
        # print "LEN " + str(len(saucers))
        if (len(saucers) == 0):
            BEASTMODE = 2
            boss.inittime = time

    # for final player death
    if (ship.health <= 0 and endtime == 0):
        endtime = time

    if (ship.active == False):
        doneExploding = ship.explode(time)
        # print doneExploding
        if (doneExploding):
            ship.respawn(shipimg)
            SCROLLSPEED = NORMSCROLLSPEED
            ship.bamfmode = False

        #		if(endtime == 0):
        #			endtime = time
    # for time delay after death
    if (time >= endtime + 4000 and endtime != 0):
        # print "game over"
        endgame = 2

    # if boss got killed make Sonic style boss death explosion
    # explode is called multiple times over several main loops to advance the explosion frame
    if (BEASTMODE == 4):
        for splat in boom:
            # if first pass, initialize explosion sequence
            if (len(boom) == 1 and splat.exploding == -1):
                splat.x = random.randrange(boss.x, boss.x + boss.width - obj.explosion[
                    0].get_width())  # subtract explosion width
                splat.y = random.randrange(boss.y, boss.y + boss.height - obj.explosion[0].get_height())
                obj.explosion.append(blacksquare)  # to take chunks out of boss
            splat.explode(time)
        if (boom[-1].exploding == 2 and len(boom) < 8):
            boom.append(obj.MoveableObject(random.randrange(boss.x, boss.x + boss.width - obj.explosion[0].get_width()),
                                           random.randrange(boss.y,
                                                            boss.y + boss.height - obj.explosion[0].get_height()),
                                           pygame.Surface((1, 1))))
        # if boss is done exploding
        if (len(boom) == 8 and boom[-1].exploding == len(obj.explosion)):
            BEASTMODE = 5
            score += 1000
            endtime = time
        # print "BEASTMODE 5"

    # if(boom[7].exploding == 4):
    #	endtime = time
    #	BEASTMODE = 5
    # meh inefficient
    # this may have to be reexamined, testing beastmode < 3
    if (boss.y > 0 and BEASTMODE < 3): BEASTMODE = 3

    # if boss is displayed
    if (4 > BEASTMODE >= 2):
        boss.move(ship, time)
        # if ship collides with boss, lose life
        if (obj.collide(ship, boss)):
            # print "boss collision"
            ship.die()  # evaluation of death is earlier in the code

    # power up (speed) deactivation
    # print time
    # print speedupstarttime
    # print time - speedupstarttime
    if (speedupstarttime > 0 and ((time - speedupstarttime) > 15000)):  # or ship exploding
        # print "Speed Reset"
        ship.speed = 5
        SCROLLSPEED = NORMSCROLLSPEED
        speedupstarttime = -1
    # more guns deactivation
    if (moregunsstarttime > 0 and ((time - moregunsstarttime) > 15000)):
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
    if (changeover == 0):
        screen.blit(bg, (0, 0), (0, 2000 - obj.SCREENH - bgoffset, obj.SCREENW, 2000 - bgoffset))
    elif (changeover == 1):
        # print "ychng: " + str(ychng)
        # print "bgoffset: " + str(bgoffset)
        screen.blit(bg, (0, 0), (0, bg.get_height() - ychng, obj.SCREENW, 2000))
        screen.blit(bg, (0, ychng), (0, 0, obj.SCREENW, obj.SCREENH - ychng))

    if (BEASTMODE >= 2): screen.blit(boss.image, (boss.x, boss.y))
    screen.blit(ship.image, (ship.x, ship.y))  # this should probably be rendered last for overlap reasons
    for saucer in saucers:
        screen.blit(saucer.image, (saucer.x, saucer.y))

    # power up rendering
    for mod in statmods:
        screen.blit(mod.image, (mod.x, mod.y))

    for bullet in bullets:
        screen.blit(bullet.image, (bullet.x, bullet.y))
    if (BEASTMODE >= 4):
        # if(boom[-1].exploding == 2):
        # print "blacksquare"
        # boss.image.blit(blacksquare, (boom[-1].x, boom[-1].y))
        for splat in boom:
            screen.blit(splat.image, (splat.x, splat.y))
    # screen.blit(explosion[explframe], (obj.SCREENW/2, obj.SCREENH/2))
    screen.blit(healthlbl, (obj.SCREENW - 100, 20))
    screen.blit(scorelbl, (obj.SCREENW - 100, 35))
    if (BEASTMODE >= 3): screen.blit(bosslbl, (obj.SCREENW / 2, 20))

    # for i in range(0,5):
    # screen.blit(obj.explosion[i], (i*120, 300))

    pygame.display.flip()  # apply double buffer

    # if(explframe > 3): explframe=0
    # else: explframe += 1

    # change offset for vertical scroll
    if (bgoffset > 2000):
        bgoffset = 0
        changeover = 0
        ychng = 0
    else:
        bgoffset += SCROLLSPEED

    if (2000 >= bgoffset > 2000 - obj.SCREENH):
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
if (BEASTMODE == 5):
    disp = pygame.image.load("victory1.png")
else:
    disp = pygame.image.load("dead1.png")

# add loop to get input, continue to high scores, etc
cont = 0
while (cont == 0):
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
