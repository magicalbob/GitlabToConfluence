import os
import requests

username = os.environ.get('CONFLUENCE_MAIL')
password = os.environ.get('CONFLUENCE_API')

#def get_page_space(page_id):
#    url = f'https://ellisbs.atlassian.net/wiki/rest/api/content/{page_id}?expand=space'
#    response = requests.get(url, auth=(username, password))
#    response.raise_for_status()
#    data = response.json()
#    space_key = data.get('space', {}).get('key')
#    return space_key

def get_page_space(page_id):
    url = f'https://ellisbs.atlassian.net/wiki/rest/api/content/{page_id}?expand=space'
    response = requests.get(url, auth=('ellisiana@gmail.com', 'UajJaS/f5I+X+dIZpDzusREyf4Rfiyk/oJKcn/uKse37'))
    response.raise_for_status()
    data = response.json()
    space_key = data.get('space', {}).get('key')
    return space_key

page_id = 393559
try:
    space_key = get_page_space(page_id)
    print(f'Space Key: {space_key}')
except requests.exceptions.HTTPError as e:
    print(f'Error: {e}')

