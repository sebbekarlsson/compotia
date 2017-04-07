from compotia.transpiler.Page import Page
from compotia.transpiler.Component import Component


def test_get_components():
    el = Page(config={
        "title": "test",
        "components": [
            {
                "path": "internal/components/navbar",
                "args": {
                    "buttons": [
                        {"text": "123", "href": "/"}
                        ]
                    }
                }
            ]
        })

    for comp in el.get_components():
        assert '<a' in comp.get_html()

def test_count_get_components():
    el = Page(config={
        "title": "test",
        "components": [
            {
                "path": "internal/components/navbar",
                "args": {
                    "buttons": [
                        {"text": "123", "href": "/"}
                        ]
                    }
                },
            {
                "path": "internal/components/navbar",
                "args": {
                    "buttons": [
                        {"text": "123", "href": "/"}
                        ]
                    }
                }
            ]
        })

    assert(len(el.get_components()) == 2)

def test_count_zero_components():
    el = Page(config={
        "title": "test",
        "components": [
            ]
        })

    assert(len(el.get_components()) == 0)
