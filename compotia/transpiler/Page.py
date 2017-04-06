from compotia.transpiler.HTMLElement import HTMLElement
from compotia.transpiler.Component import Component


class Page(HTMLElement):
    
    def __init__(self, config):
        super(HTMLElement, self).__init__()
        self.config = config
        self.components = []

        if 'components' in config:
            for comp_config in config['components']:
                self.components.append(Component(comp_config))

        with open('/tmp/compotia/layout.html') as layoutfile:
            self.html = layoutfile.read()
        layoutfile.close()

    def get_html(self):
        return ''
