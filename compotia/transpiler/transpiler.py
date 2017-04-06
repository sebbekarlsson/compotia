from compotia.information import stdout_error
from compotia.transpiler.Page import Page
import json
import os


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

        pages = self.get_pages()
