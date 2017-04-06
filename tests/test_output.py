from compotia.transpiler.transpiler import Transpiler


transpiler = Transpiler()
transpiler.transpile('tests/test_project/main.json', 'tests/test_project/output')

def test_components():
    content = ''
    with open('tests/test_project/output/template/Startpage.html') as _file:
        content = _file.read()
    _file.close()

    assert content.count('123') == 2

def test_http_styles():
    content = ''
    with open('tests/test_project/output/template/style.css') as _file:
        content = _file.read()
    _file.close()

    assert 'Bootstrap' in content
