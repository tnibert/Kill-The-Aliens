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


def toframes(img, numframes, xstep):
    """
    Divide an image into frames
    :param img:
    :param numframes:
    :param xstep:
    :return:
    """
    # img to divide up, number of frames to generate, step size on x axis to split on
    frames = []  # list of images
    for i in range(0, numframes):
        workimg = pygame.Surface((xstep, img.get_height()), pygame.SRCALPHA, 32)
        # workimg = workimg.convert_alpha()
        workimg.blit(img, (0, 0), area=pygame.Rect(xstep * i, 0, xstep, img.get_height()))
        frames.append(workimg.copy())
    return frames


def collide(spr1, spr2):
    """
    Detect sprite collision
    :param spr1: a GameObject
    :param spr2: a GameObject
    :return: True if the sprites have collided, False if not
    """
    # spr1 is a, spr2 is b
    wa = spr1.x + spr1.width
    ha = spr1.y + spr1.height
    wb = spr2.x + spr2.width
    hb = spr2.y + spr2.height
    bx = 5
    by = 5

    if inside(spr1.x, spr1.y, spr2.x+bx, spr2.y+by, wb-bx, hb-by) \
            or inside(spr1.x, ha, spr2.x+bx, spr2.y + by, wb-bx, hb-by) \
            or inside(wa, spr1.y, spr2.x+bx, spr2.y+by, wb-bx, hb-by) \
            or inside(wa, ha, spr2.x+bx, spr2.y+by, wb-bx, hb-by):
        return True
    else:
        return False


def inside(x, y, left, top, right, bottom):
    if x > left and x < right and y > top and y < bottom:
        return True
    else:
        return False
