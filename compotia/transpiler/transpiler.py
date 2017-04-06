from compotia.information import stdout_error
from compotia.transpiler.Page import Page
from compotia.utils import clean_str
import json
import os
import shutil


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

        # -- pages -- #
        pages = self.get_pages()

        css = ''
        js = ''

        for page in pages:
            with open(
                '{}/{}'.format(out_path, '{}.html'.format(page.title)),
                'w+'
            ) as htmlfile:
                htmlfile.write(page.get_html())
            htmlfile.close()

            css += page.get_css()
            js += page.get_js()

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
