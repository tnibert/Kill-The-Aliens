class Scene:
    def __init__(self, eventqueue, screen):
        self.eventqueue = eventqueue
        self.children = []              # objects renderable in the scene
        self.screen = screen

    def attach(self, obj):
        """
        Attach a GameObject into the scene
        :param obj:
        :return:
        """
        self.children.append(obj)

    def remove(self, obj):
        """
        Remove a GameObject from the scene
        :param obj:
        :return:
        """
        self.children.remove(obj)

    def update_cycle(self):
        for child in self.children:
            child.update()

    def draw_cycle(self):
        for child in self.children:
            child.draw(self.screen)
