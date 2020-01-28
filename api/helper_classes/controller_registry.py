class ControllerRegistry:
    def add_controller(self, controller):
        name = controller.__name__
        setattr(self, name, controller)
