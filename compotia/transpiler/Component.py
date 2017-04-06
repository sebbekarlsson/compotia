import compotia.transpiler
from compotia.information import stdout_warning
import os
from jinja2 import Template


class Component(compotia.transpiler.HTMLElement.HTMLElement):

    def __init__(self, *args, **kwargs):
        super(Component, self).__init__(*args, **kwargs)

        if 'path' not in self.config:
            stdout_warning('Missing path for component.')
        else:
            for comp in self.get_components():
                self.js += comp.js
                self.css += comp.css

            if 'internal/components' in self.config['path']:
                self.config['path'] = '/tmp/compotia/{}'.format(
                        self.config['path'].replace('internal/', ''))

            html_path = '{}/{}'.format(self.config['path'], 'component.html')
            if os.path.isfile(html_path):
                with open(html_path) as htmlfile:
                    self.html += htmlfile.read()
                htmlfile.close()

            css_path = '{}/{}'.format(self.config['path'], 'component.css')
            if os.path.isfile(css_path):
                with open('{}/{}'.format(self.config['path'], 'component.css')) as cssfile:
                    self.css += cssfile.read()
                cssfile.close()

            js_path = '{}/{}'.format(self.config['path'], 'component.js')
            if os.path.isfile(js_path):
                with open('{}/{}'.format(self.config['path'], 'component.js')) as jsfile:
                    self.js += jsfile.read()
                jsfile.close()

    def get_html(self):
        if 'args' in self.config:
            _t = Template(self.html)

            return _t.render(**self.config['args'])

        return self.html

    def get_css(self):
        if 'args' in self.config:
            _t = Template(self.css)

            return _t.render(**self.config['args'])
        
        return self.css

    def get_js(self):
        if 'args' in self.config:
            _t = Template(self.js)

            return _t.render(**self.config['args'])
        
        return self.js
