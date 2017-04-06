from compotia.transpiler.HTMLElement import HTMLElement


class Component(HTMLElement):

    def __init__(self, config):
        super(HTMLElement, self).__init__()
        self.config = config
