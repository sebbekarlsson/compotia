def clean_str(the_str):
    return the_str.replace(' ', '_')\
            .replace('"', '-')\
            .replace("'", '-')
