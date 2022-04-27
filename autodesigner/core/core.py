from pywinauto.application import Application


class Core:
    def __init__(self):
        self.app = Application(backend="uia")

