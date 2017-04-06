from compotia.transpiler.HTMLElement import HTMLElement
from compotia.transpiler.Component import Component
from compotia.information import stdout_error
from compotia.utils import clean_str
from jinja2 import Template


class Page(HTMLElement):
    
    def __init__(self, *args, **kwargs):
        super(Page, self).__init__(*args, **kwargs)
        
        if 'title' not in self.config:
            stdout_error('Missing title for page.')
            quit()

        self.title = clean_str(self.config['title'])

        with open('/tmp/compotia/templates/layout.html') as layoutfile:
            self.html = layoutfile.read()
        layoutfile.close()

        self.stylesheets = ['style.css']
        self.scripts = ['main.js']

    def get_html(self):
        _t = Template(self.html)

        content = ''

        for component in self.get_components():
            if component is self:
                continue

            content += component.get_html()

        return _t.render(content=content,
                stylesheets=self.stylesheets,
                scripts=self.scripts
                )

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
