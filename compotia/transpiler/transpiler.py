from compotia.information import stdout_error
from compotia.transpiler.Page import Page
from compotia.transpiler.Component import Component
from compotia.utils import clean_str
from jinja2 import Template
import json
import os
import shutil
import requests


class Transpiler(object):

    def __init__(self):
        print('Initialized Transpiler')
        self.config = {}

    def get_pages(self):
        pages = []
        for page_conf in self.config['pages']:
            pages.append(Page(page_conf))

        return pages

    def transpile(self, in_path, out_path):
        if not os.path.exists(in_path):
            stdout_error('{} does not exists.'.format(in_path))
            
            return False

        json_content = ''

        with open(in_path) as jfile:
            json_content = jfile.read()
        jfile.close()

        try:
            conf = json.loads(json_content)
        except ValueError:
            stdout_error('Could not parse json configuration.')
            conf = {}

        self.config = conf

        required_fields = [
            'title'
        ]

        for field in required_fields:
            if field not in conf:
                stdout_error('missing field: "{}" in configuration.'.format(
                    field))
                quit()

        self.config['title'] = clean_str(self.config['title'])
        
        out_path += '/{}'.format(self.config['title'])

        if os.path.isdir(out_path):
            shutil.rmtree(out_path)
            os.makedirs(out_path)
        else:
            os.makedirs(out_path)

        css = """
            * {
                margin: 0;
                padding: 0;
            }
        """
        js = ''
        header_html = ''
        footer_html = ''

        # -- deps -- #
        dep_src = ''
        if 'css' in self.config:
            for dep in self.config['css']:
                if 'http' in dep:
                    dep_src = requests.get(dep)
                    dep_src = dep_src.text if hasattr(dep_src, 'text') else ''
                else:
                    with open(dep) as depfile:
                        dep_src = depfile.read()
                    depfile.close()

                css += dep_src

        dep_src = ''
        if 'js' in self.config:
            for dep in self.config['js']:
                if 'http' in dep:
                    dep_src = requests.get(dep)
                    dep_src = dep_src.text if hasattr(dep_src, 'text') else ''
                else:
                    with open(dep) as depfile:
                        dep_src = depfile.read()
                    depfile.close()

                js += dep_src

        # -- header -- #
        if 'header' in self.config:
            if 'components' in self.config['header']:
                for comp_conf in self.config['header']['components']:
                    comp = Component(comp_conf)
                    css += comp.get_css()
                    js += comp.get_js()
                    header_html += comp.get_html()

        # -- footer -- #
        if 'footer' in self.config:
            if 'components' in self.config['footer']:
                for comp_conf in self.config['footer']['components']:
                    comp = Component(comp_conf)
                    css += comp.get_css()
                    js += comp.get_js()
                    footer_html += comp.get_html()

        # -- pages -- #
        pages = self.get_pages()

        for page in pages:
            with open(
                '{}/{}'.format(out_path, '{}.html'.format(page.title)),
                'w+'
            ) as htmlfile:
                _t = Template(page.get_html())
                htmlfile.write(_t.render(
                    content_header=header_html,
                    content_footer=footer_html
                    ))
            htmlfile.close()

            page_css = page.get_css()
            if page_css not in css:
                css += page_css

            page_js = page.get_js()
            if page_js not in js:
                js += page_js

        if '#ONCE' in js and '#ENDONCE' in js:
            once_parts = js.split('#ONCE')

            once_map = {}

            for part in once_parts:
                part = part.split('#ENDONCE')[0]

                if part not in once_map:
                    once_map[part] = 1
                else:
                    once_map[part] += 1
           
            
            for k, v in once_map.items():
                if v > 1:
                    js = js.replace(k, '')
                    js += k

            js = js.replace('#ONCE', '').replace('#ENDONCE', '')

        with open(
            '{}/{}'.format(out_path, '{}.css'.format('style')),
            'w+'
        ) as cssfile:
            cssfile.write(css)
        cssfile.close()

        with open(
            '{}/{}'.format(out_path, '{}.js'.format('main')),
            'w+'
        ) as jsfile:
            jsfile.write(js)
        jsfile.close()
