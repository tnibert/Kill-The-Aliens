import pygame


# from activestate cookbook recipe
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match

        # this was raise StopIteration before
        # but apparently as of python 3.7, that causes a RuntimeError
        return

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
    :param img: the pygame image to divide
    :param numframes: the number of frames to divide into
    :param xstep: the number of pixels wide each frame should be
    :return: list of images
    """
    frames = []  # list of images
    for i in range(0, numframes):
        workimg = pygame.Surface((xstep, img.get_height()), pygame.SRCALPHA, 32)
        # workimg = workimg.convert_alpha()
        workimg.blit(img, (0, 0), area=pygame.Rect(xstep * i, 0, xstep, img.get_height()))
        frames.append(workimg.copy())
    return frames


def collide(rect1, rect2):
    """
    Detect sprite collision
    :param rect1: a GameObject
    :param rect2: a GameObject
    :return: True if the sprites have collided, False if not
    """
    return rect1.x < rect2.x + rect2.width and rect1.x + rect1.width > rect2.x and rect1.y < rect2.y + rect2.height and rect1.y + rect1.height > rect2.y
