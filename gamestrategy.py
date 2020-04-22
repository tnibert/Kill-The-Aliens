class Strategy:
    """
    Manages the addition and removal of objects from the scene.
    """
    def __init__(self, scene):
        self.scene = scene

    def setup(self):
        """
        Method to set up the level before run_game() is called.
        :return:
        """
        pass

    def run_game(self):
        """
        Do an update and render cycle for the scene.
        Called once every frame.
        :return:
        """
        self.scene.update_cycle()
        self.scene.render_cycle()
