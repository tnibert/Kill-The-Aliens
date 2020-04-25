from observe import Observable
import pytest


EV_NAME = "test"


class DummyReceiver:
    def __init__(self):
        self.test = []

    def my_callback(self, event):
        self.test.append(str(event))


@pytest.fixture
def my_observable():
    return Observable()


@pytest.fixture
def my_receiver():
    return DummyReceiver()


def test_subscribe(my_observable, my_receiver):
    my_observable.subscribe(EV_NAME, my_receiver.my_callback)
    my_observable.subscribe(EV_NAME, my_receiver.my_callback)
    assert len(my_observable.callbacks[EV_NAME]) == 2


def test_unsubscribe(my_observable, my_receiver):
    my_observable.subscribe(EV_NAME, my_receiver.my_callback)
    my_observable.subscribe(EV_NAME, my_receiver.my_callback)
    my_observable.unsubscribe(EV_NAME, my_receiver.my_callback)
    assert len(my_observable.callbacks[EV_NAME]) == 1
    my_observable.unsubscribe(EV_NAME, my_receiver.my_callback)
    assert len(my_observable.callbacks[EV_NAME]) == 0


def test_remove_event(my_observable, my_receiver):
    assert EV_NAME not in my_observable.callbacks.keys()
    my_observable.subscribe(EV_NAME, my_receiver.my_callback)
    assert EV_NAME in my_observable.callbacks.keys()
    my_observable.remove_event(EV_NAME)
    assert EV_NAME not in my_observable.callbacks.keys()


def test_notify(my_observable, my_receiver):
    my_observable.subscribe(EV_NAME, my_receiver.my_callback)
    my_observable.subscribe(EV_NAME, my_receiver.my_callback)
    my_observable.notify(EV_NAME)
    assert len(my_receiver.test) == 2
    for ev in my_receiver.test:
        assert ev == EV_NAME
