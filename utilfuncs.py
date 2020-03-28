import pygame


# from activestate cookbook recipe
# made a nice algorithm, then realized python has no switch/case
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


# divide an image into frames
def toframes(img, numframes, xstep):
    # img to divide up, number of frames to generate, step size on x axis to split on
    frames = []  # list of images
    for i in range(0, numframes):
        workimg = pygame.Surface((xstep, img.get_height()), pygame.SRCALPHA, 32)
        # workimg = workimg.convert_alpha()
        workimg.blit(img, (0, 0), area=pygame.Rect(xstep * i, 0, xstep, img.get_height()))
        frames.append(workimg.copy())
    return frames


def collide(spr1, spr2):
    return pygame.sprite.collide_rect(spr1, spr2)