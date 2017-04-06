import compotia.transpiler


class HTMLElement(object):

    def __init__(self, config):
        self.html = ''
        self.css = ''
        self.js = ''
        self.components = []
        self.config = config

        if 'components' in self.config:
            for comp_config in self.config['components']:
                self.components.append(compotia.transpiler.Component.Component(comp_config))
        
    def get_components(self, _component=0, _components=None):
        comps = []
        if _components is not None:
            comps += _components

        if _component == 0:
            _component = self
        
        if _component is not None:
            comps.append(_component)
            for component in _component.components:
                comps += self.get_components(component, comps)
        
        return comps
