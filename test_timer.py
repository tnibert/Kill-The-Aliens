import pygame
pygame.init()

from loadstaticres import shipimg
from timer import Timer
from test_scene import MockGameObj
import time


def test_tick():
    """
    NB: timer does not send tick events from owner
    """
    g = MockGameObj(0, 0, shipimg)
    t = Timer()
    t.subscribe("tick", g.on_tick)
    t.tick()
    assert len(g.testlist) == 1
    assert g.testlist[0] is t


def test_timeout_timer_own():
    testlist = []

    t = Timer()
    t.subscribe("timeout", lambda e: testlist.append(e.source))
    t.startwatch(1)
    time.sleep(1)
    t.tick()

    assert len(testlist) == 1
    assert testlist[0] is t


def test_timeout_obj_own():
    testlist = []

    g = MockGameObj(0, 0, shipimg)
    t = Timer(owner=g)
    g.subscribe("timeout", lambda e: testlist.append(e.source))
    t.startwatch(1)
    time.sleep(1)
    t.tick()

    assert len(testlist) == 1
    assert testlist[0] is g


def test_is_timing():
    t = Timer()
    t.startwatch(1)
    assert t.is_timing()
    t.tick()
    assert t.is_timing()
    t.stopwatch()
    assert not t.is_timing()
    t.startwatch(1)
    time.sleep(1.1)
    t.tick()
    assert not t.is_timing()
