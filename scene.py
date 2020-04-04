from observe import Observable, Event
from moveableobject import MoveableObject
from utilfuncs import collide
from timer import Timer


class Scene:
    def __init__(self, eventqueue, screen):
        # todo: implement handling of the game event queue
        self.eventqueue = eventqueue
        self.children = []              # objects renderable in the scene
        self.screen = screen
        self.clock = Timer(owner=self)

    def attach(self, obj):
        """
        Attach a GameObject into the scene
        :param obj:
        :return:
        """
        if isinstance(obj, Observable):
            obj.subscribe("remove", self.receive_signals)
        self.clock.subscribe("tick", obj.on_tick)
        self.children.append(obj)
        # todo: optimize this for insert, don't resort list every time
        self.children = sorted(self.children, key=lambda g: g.layer)

    def remove(self, obj):
        """
        Remove a GameObject from the scene
        :param obj:
        :return:
        """
        self.children.remove(obj)

    def update_cycle(self):
        self.clock.tick()
        self.check_collisions()
        for child in self.children:
            child.update()

    def render_cycle(self):
        for child in self.children:
            child.render(self.screen)

    def receive_signals(self, event):
        """
        Receive notifications from observables
        :return:
        """
        if event.name == "remove":
            self.remove(event.source)
            print("gameobject removed")

    def check_collisions(self):
        for c1 in filter(lambda c: isinstance(c, MoveableObject), self.children):
            for c2 in filter(lambda c: isinstance(c, MoveableObject), self.children):
                if c1 != c2:
                    if collide(c1, c2):
                        # print("Collision between {} and {}".format(c1, c2))
                        c1.notify(Event("collision"), who=c2)
