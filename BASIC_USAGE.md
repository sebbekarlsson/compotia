# Using the CLI-app

## The commandline
> This is the basic command:

        compotia -i <path_to_json> -o <output_path>

> The first argument `-i` is the path to your json config.

> The second argument `-o` is where you want the output files to be placed.

## The json file
> The important fields:
* `title` - The title of your template
* `css` - css dependencies (will be bundled into a single main.js file)
* `js` - javascript dependencies (will be bundled into a single style.css file)
* `header` - the head of your template, supports components.
* `pages` - the pages of your template, will be generated into separate files.
* `footer` - the footer of your template, supports components.

> Below is an example:

        {
            "title": "CoolTemplate",
            "css": [
                "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
            ],
            "js": [
                "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"
            ],
            "header": {
                "components": [
                    {
                        "path": "components/navbar",
                        "args": {
                            "buttons": [
                                {
                                    "text": "Home",
                                    "href": "/"
                                },
                                {
                                    "text": "About",
                                    "href": "about.html"
                                }
                            ]    
                        }
                    }
                ]    
            },
            "pages": [
                {
                    "title": "index",
                    "components": [
                        {
                            "path": "components/textbox",
                            "args": {
                                "text": "Lorem ipsum"    
                            }
                        }
                    ]
                }
            ],
            "footer": {
                "components": [
                    {
                        "path": "components/footer"
                    }
                ]
            }
        }

## Components
> As you can see in the example, in the header column of our json file; we have
> a component that has a `path` to `components/navbar`.

> This is where we would have a folder called `components` and another folder
> inside called `navbar`.
> In this case, the `navbar` is a component.

> A component can have the following files:
* `component.html` - The markup
* `component.js` - The javascript (will be bundled into a single main.js file)
* `component.css` - The css (will be bundled into a single style.css file)
* `component.scss` - The css (will be bundled into a single style.css file

> The important fields:
* `path` - The path to the component
* `args` - Arguments passed into the component.

> An example of the json:

        {
            "path": "components/navbar",
            "args": {
                "buttons": [
                    {
                        "text": "Home",
                        "href": "/"
                    },
                    {
                        "text": "About",
                        "href": "about.html"
                    }
                ]    
            }
        }

> In the example, the navbar component.html probably looked like this:
        
        <nav class='navbar'>
            <ul>
                {% for button in buttons %}
                    <li><a href='{{ button.href }}'>{{ button.text }}</a></li>
                {% endfor %}
            </ul>
        </nav>

> As you can se, we are iterating through the `buttons` value, passed into
> the `args`.
