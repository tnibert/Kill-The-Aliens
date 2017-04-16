import pygame
import random
import math

SCREENH = 600
SCREENW = 640
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3
BLACK = (0,0,0)
EXTIMELAPSE = 250
BOSSHEALTH = 2000				#default 2000
PLAYERHEALTH = 3				#default 3

#divide an image into frames
def toframes(img, numframes, xstep):
	#img to divide up, number of frames to generate, step size on x axis to split on
	frames = []	#list of images
	for i in range(0, numframes):
		workimg = pygame.Surface((xstep, img.get_height()), pygame.SRCALPHA, 32)
		#workimg = workimg.convert_alpha()
		workimg.blit(img, (0,0), area=pygame.Rect(xstep*i, 0, xstep, img.get_height()))
		frames.append(workimg.copy())
	return frames

explosion = toframes(pygame.image.load("explode1.png"), 5, 120)

#all sprites inherit from this class
class MoveableObject(pygame.sprite.Sprite):
	def __init__(self, x, y, img):
		pygame.sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.image = img
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.rect = self.image.get_rect()
		self.updatepos()
		self.exploding = -1
		self.timestack = []
		self.active = True
	def updatepos(self):	#this lets us play nice with pygame, collision detection
		self.pos = (self.x, self.y)
		self.rect.x = self.x
		self.rect.y = self.y
	def explode(self, time):		#yes, everything can explode
		self.timestack.append(time)
		self.speed = 0
		if(len(self.timestack) < 2):
			difftime = EXTIMELAPSE + 1
		elif(len(self.timestack) >= 2):
			newtime = self.timestack.pop()
			oldtime = self.timestack.pop()
			difftime = newtime - oldtime
			#print "newtime: " + str(newtime) + " oldtime: " + str(oldtime) + " diff: " + str(difftime)
			if(difftime <= EXTIMELAPSE): self.timestack.append(oldtime)
			else: self.timestack.append(newtime)
		if(self.exploding < len(explosion)-1 and difftime > EXTIMELAPSE):
			self.exploding += 1
			self.image = explosion[self.exploding]
		if(self.exploding >= len(explosion)-1): 
			#self.image.fill(BLACK)
			self.exploding += 1
			self.image = explosion[len(explosion)-1]
			self.active = False
			return True		#we're done
		return False
		#then return to main for cleanup
		#print self.active
		#print self.timestack

#from activestate cookbook recipe
#made a nice algorithm, then realized python has no switch/case
class switch(object):
	def __init__(self, value):
		self.value = value
		self.fall = False

	def __iter__(self):
		"""Return the match method once, then stop"""
		yield self.match
		raise StopIteration

	def match(self, *args):
		"""Indicate whether or not to enter a case suite"""
		if self.fall or not args:
			return True
		elif self.value in args:
			self.fall = True
			return True
		else:
			return False
	

#even good power ups may explode, but rarely

#power ups and downs, to be inherited from
class StatusModifier(MoveableObject):
	def __init__(self, img):
		MoveableObject.__init__(self, random.randrange(0, SCREENW), -100, img)
		self.degreeangle = random.randrange(100, 260)	#angle randomly ranges from 100 degrees to 260, 0 degrees is vertical axis
		self.speed = 3
	def payload(self, target):
		print("This payload is empty...")
		return 0
	def move(self):
		#screen edge checking

		if((self.x > SCREENW-self.width and self.degreeangle > 180) or random.randrange(0, 2000)==1467): 
			self.degreeangle = random.randrange(100, 160) #270 - (self.degreeangle - 90)
			#print "turn left"
		elif((self.x < 0 and self.degreeangle < 180) or random.randrange(0,2000)==200): 
			self.degreeangle = random.randrange(200,260) #90 + (270 - self.degreeangle) 
			#print "turn right"

		self.x -= (math.degrees(math.sin(math.radians(self.degreeangle)))*self.speed)/40
		self.y -= (math.degrees(math.cos(math.radians(self.degreeangle)))*self.speed)/40
		self.updatepos()
		#print "x = " + str(self.x) + ", y = " + str(self.y)
		#create movement trigonometrically like in Panzer Deathmatch

#+1 life
class OneUp(StatusModifier):
	def payload(self, target):
		#add some sort of happy animation
		target.health += 1
		return 0

#bomb booby trap, -1 life
#we'll have to make sure that the payload does not happen multiple times
class Bomb(StatusModifier):
	def payload(self, target):
		target.die()		#initiate explosion
		return 0

#double background and ship speed, need a way to undo after time
class SpeedUp(StatusModifier):
	def payload(self, target):
		target.speed = 10
		return 1
		
#shoot from 3 locations, need a way to undo after time
class MoreGuns(StatusModifier):
	def payload(self, target):
		#print "MOAR GUNS"
		target.bamfmode = True
		return 2

class Player(MoveableObject):
	def __init__(self, img):
		MoveableObject.__init__(self, SCREENW/2, 450, img)
		self.health = PLAYERHEALTH
		self.spawnX = self.x
		self.spawnY = self.y
		self.speed = 5
		self.bamfmode = False
	def fire(self, img, turret=UP):
		if turret == UP:
			return Bullet(self.x+(self.image.get_width()/2), self.y - 10, img, UP)
		if turret == LEFT:
			return Bullet(self.x+15, self.y + 40, img, UP)
		if turret == RIGHT:
			return Bullet(self.x+self.image.get_width()-15, self.y + 40, img, UP)
		#so, in order to implement bamf mode, we need bullets to come out from side turrets
		#but currently our fire method can only return one bullet
		#so we either return a list of bullets when we fire (a cool bit of modification to the game loop)
		#or we can check in the game loop and if bamfmode call fire two more times, I think this is better
		#we should also add something in the main loop that prevents a bullet moving upward from harming the ship
	def die(self):
		print ("player dead")
		if self.active == True:
			self.active = False
			self.health -= 1
	def respawn(self, img):
		self.exploding = -1
		self.active = True
		if(self.health <= 0):
			self.x = -2000
			self.y = -2000
			self.speed = 0
		else:
			self.x = self.spawnX
			self.y = self.spawnY
			self.speed = 5
			self.image = img
		self.updatepos()

#so, for the player to explode
#make die() method decrement health*
#make all areas that currently decrement health call die() instead*
#and make them all check for explosion happening
#make self.active == False trigger explosion unless explosion already happening
#once we are exploding and frame has reached last explosion frame
#	respawn() ship at start coordinates

class Enemy(MoveableObject):
	def __init__(self, x, y, img):
		MoveableObject.__init__(self, x, y, img)
		#0 means left, 1 means right
		self.dir = random.randrange(0, 2)
		self.xspeed = random.randrange(1, 4)
		self.yspeed = random.randrange(1, 4)
	def move(self, beast):
		#check direction -- these don't match to the predefines
		if(self.dir == 0):
			self.x -= self.xspeed
			self.y += self.yspeed
			self.updatepos()
		else:
			self.x += self.xspeed
			self.y += self.yspeed
			self.updatepos()
		#check horizontal border
		if(self.x < 0): self.dir = 1
		elif(self.x > SCREENW-50): self.dir = 0

		#check going off bottom of screen
		if(self.y > SCREENH and beast != 1): 
			self.__init__(random.randrange(0, SCREENW), 0, self.image)
		elif(self.y > SCREENH and beast == 1):	#do not init again, go cleanly off screen
			return beast

		self.updatepos()
		#print self.rect
		return 0
	def respawn(self):
		self.active = True
		self.__init__(random.randrange(0, SCREENW), random.randrange(-200,-50), self.image)
		

class Boss(MoveableObject):
	def __init__(self, x, y, img, time):
		MoveableObject.__init__(self, x, y, img)
		self.health = BOSSHEALTH
		self.inittime = time

		#state indicator for boss
		#0 is still, 1 is aimless moving
		#2 is chase ship, 3 is fire at ship
		self.mode = 0

		#counts number of steps in a given direction
		self.step = 0
		self.maxstep = 4
		self.stepdist = 4
		#initial direction
		self.dir = random.randrange(0,4)
		self.active = True
		#for mode 2
		self.alreadygoing = 0
	def move(self, foe, time):
		#so this is going to need a little AI
		#and maybe some smoothing of the movement
		#and tracking of foe
		#and discrimination of shooting

		#update mode based on timer
		if(time-self.inittime > 1000):
			self.inittime = time
			if(self.mode < 3): self.mode += 1
			else: self.mode = 0

		if(self.mode == 0): return

		elif(self.mode == 1):
			if(self.step < self.maxstep):
				self.step += 1
			else:
				self.dir = random.randrange(0,4)
				self.step = 0
				self.maxstep = random.randrange(2,6)

		elif(self.mode == 2):
			test = self.infirerange(foe)
			if(test == -3 and self.alreadygoing == 0):		#if ship is in middle
				self.dir = random.randrange(0,2)
				self.alreadygoing = 1
			elif(test == -1 and self.alreadygoing == 0):
				self.dir = LEFT
				self.alreadygoing = 1
			elif(test == -2 and self.alreadygoing == 0):
				self.dir = RIGHT
				self.alreadygoing = 1
			elif(test > 0):
				self.mode = 0
				self.alreadygoing = 0

		#MODE 3 HAS NOT BEEN IMPLEMENTED

		
		#check for screen boundaries
		if(self.y+self.height > foe.y-60): 
			self.dir = UP
			self.step = 0
		if(self.y < 0): 
			self.dir = DOWN
			self.step = 0
		if(self.x < -50):
			self.dir = RIGHT
			self.step = 0
		if(self.x+self.width-50 > SCREENW):
			self.dir = LEFT
			self.step = 0

		#self.dir = random.randrange(2,4)
		if(self.dir == DOWN):		#move down
			self.y += self.stepdist
		elif(self.dir == UP): 		#move up
			self.y -= self.stepdist
		elif(self.dir == LEFT):		#move left
			self.x -= self.stepdist
		elif(self.dir == RIGHT):		#move right
			self.x += self.stepdist

		self.updatepos()
	def fire(self, img, side):
		if(side == LEFT): return Bullet(self.x, self.y+self.height, img, DOWN)
		else: return Bullet(self.x+self.width, self.y+self.height, img, DOWN)
	def infirerange(self, foe):
		#self.x is left turret, self.x+self.width is right turret
		#return 1 if left turret, return 2 if right
		#return -1 if too far left, -2 if too far right, -3 if in center
		if(foe.x+foe.width > self.x and foe.x < self.x): return 1
		if(foe.x+foe.width > self.x+self.width and foe.x < self.x+self.width): return 2
		if(foe.x+foe.width < self.x): return -1
		if(foe.x > self.x + self.width): return -2
		if(foe.x+foe.width < self.x+self.width and foe.x > self.x): return -3
	def die(self):
		#print "dead"
		self.active = False

class Bullet(MoveableObject):
	def __init__(self, x, y, img, dir):
		MoveableObject.__init__(self, x, y, img)
		self.dir = dir
		#self.active = True
		self.speed = 13		#was 10, is now 13 for statmod speed up
	def move(self):
		# dir 0 for up, anything else for down
		if(self.dir == UP): self.y -= self.speed
		else: self.y += self.speed
		self.updatepos()

def collide(spr1, spr2):
	return pygame.sprite.collide_rect(spr1, spr2)
		#print("spr1 type = " + str(type(spr1)) + " x = " + str(spr1.x) + " y = " + str(spr1.y))
		#print("spr2 type = " + str(type(spr2)) + " x = " + str(spr2.x) + " y = " + str(spr2.y))
		#print " " 
		#return True
	#return False
