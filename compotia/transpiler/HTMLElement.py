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

        if len(comps) == 0:
            comps = self.components

        if _components is not None:
            comps += _components

            for component in _component.components:
                comps += self.get_components(component, comps)
        
        return comps

    def get_html(self):
        _t = Template(self.html)

        content = ''

        for component in self.get_components():
            if component is self:
                continue

            content += component.get_html()

    def get_css(self):
        _css = ''

        for component in self.get_components():
            if component is self:
                continue

            _css += component.get_css()

        return _css

    def get_js(self):
        _js = ''

        for component in self.get_components():
            if component is self:
                continue

            _js += component.get_js()
        
        return _js
