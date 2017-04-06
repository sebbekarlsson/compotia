import compotia.transpiler
from compotia.information import stdout_warning
import os
from jinja2 import Template
import json


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

            # -- reformat args -- #
            if 'args' in self.config:
                args_str = json.dumps(self.config)
                _m_keys = args_str.split('>{')

                if len(_m_keys) > 0:
                    _m_keys.pop(0)

                for m_k in _m_keys:
                    m_k = '>{' + m_k.split('}')[0] + '}'
                    k = m_k.split(':')[0].replace(' ', '').replace('>{', '')
                    v = m_k.split(':')[1].replace(' ', '').replace('}', '')

                    if v == 'component':
                        if m_k in self.config['args']:
                            comp_conf = self.config['args'][m_k]
                            comp = compotia.transpiler.Component.Component(comp_conf)
                            
                            self.js += comp.get_js()
                            self.css += comp.get_css()

                            args_str = args_str.replace(m_k, k)
                            self.config = json.loads(args_str)

                            self.config['args'][k] = comp.get_html()

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
