import pygame
pygame.init()

from scene import Scene
from moveableobject import MoveableObject
from loadstaticres import shipimg
import pytest


class MockScreen:
    pass


class MockGameObj(MoveableObject):
    def __init__(self, x, y, img):
        super().__init__(x, y, 0, img)
        self.testlist = []

    def on_collide(self, event):
        self.testlist.append(str(event))


@pytest.fixture
def PopulatedScene():
    s = Scene(MockScreen())
    g1 = MockGameObj(0, 0, shipimg)
    g2 = MockGameObj(g1.width - 1, g1.height - 1, shipimg)
    s.attach(g1)
    s.attach(g2)
    return s


def test_attach():
    s = Scene(MockScreen())
    g1 = MockGameObj(0, 0, shipimg)
    g2 = MockGameObj(g1.width - 1, g1.height - 1, shipimg)
    s.attach(g1)
    s.attach(g2)
    assert len(s.children) == 2
    assert s.receive_signals in g1.callbacks["remove"]


def test_remove(PopulatedScene):
    item = PopulatedScene.children[0]
    assert len(PopulatedScene.children) == 2
    PopulatedScene.remove(item)
    assert len(PopulatedScene.children) == 1
    assert PopulatedScene.receive_signals not in item.callbacks["remove"]


def test_check_collisions(PopulatedScene):
    PopulatedScene.check_collisions()
    assert len(PopulatedScene.children[0].testlist) == 1
    assert PopulatedScene.children[0].testlist[0] == "collision"
    assert len(PopulatedScene.children[1].testlist) == 1
    assert PopulatedScene.children[1].testlist[0] == "collision"
