import re
import sys


MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'
URL_PATH_REGEX = r'^\/[/.a-zA-Z0-9-]+$'

# borrowed from https://emailregex.com/
EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

api_name = '{{ cookiecutter.api_name }}'
api_base_url = '{{ cookiecutter.api_base_url }}'
author = '{{ cookiecutter.author }}'
author_email = '{{ cookiecutter.author_email }}'

# check api name
if not re.match(MODULE_REGEX, api_name):
    print(f'ERROR: {api_name} for "api_name" is not a valid Python module name!')
    # exits with status 1 to indicate failure
    sys.exit(1)

# check url path
if not re.match(URL_PATH_REGEX, api_base_url):
    print(f'ERROR: {api_base_url} for "api_base_url" is not a valid RFC3986 URL path')
    # exits with status 1 to indicate failure
    sys.exit(1)

# check email
if not re.match(EMAIL_REGEX, author_email):
    print(f'ERROR: {author_email} for "author_email" is not a valid email')
    # exits with status 1 to indicate failure
    sys.exit(1)