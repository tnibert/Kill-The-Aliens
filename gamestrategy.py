class Strategy:
    """
    Manages the addition and removal of objects from the scene
    """
    def __init__(self, scene):
        self.scene = scene

    def run_game(self):
        self.scene.update_cycle()
        self.scene.render_cycle()
