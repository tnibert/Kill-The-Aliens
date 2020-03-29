from observe import Observable, Event
from utilfuncs import collide


class Scene:
    def __init__(self, eventqueue, screen):
        # todo: implement handling of the game event queue
        self.eventqueue = eventqueue
        self.children = []              # objects renderable in the scene
        self.screen = screen

    def attach(self, obj):
        """
        Attach a GameObject into the scene
        :param obj:
        :return:
        """
        if isinstance(obj, Observable):
            obj.subscribe("remove", self.receive_signals)
        self.children.append(obj)

    def remove(self, obj):
        """
        Remove a GameObject from the scene
        :param obj:
        :return:
        """
        self.children.remove(obj)

    def update_cycle(self):
        self.check_collisions()
        for child in self.children:
            child.update()

    def draw_cycle(self):
        for child in self.children:
            child.draw(self.screen)

    def receive_signals(self, event):
        """
        Receive notifications from observables
        :return:
        """
        if event.name == "remove":
            self.remove(event.source)
            print("gameobject removed")

    def check_collisions(self):
        for c1 in self.children:
            for c2 in self.children:
                if c1 != c2:
                    if collide(c1, c2):
                        print("Collision between {} and {}".format(c1, c2))
                        c1.notify(Event("collision"))
