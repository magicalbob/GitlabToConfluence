import os
import json
from atlassian import Confluence

username = os.environ.get('CONFLUENCE_MAIL')
password = os.environ.get('CONFLUENCE_API')

# Read the configuration from 'config.json'
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

confluence_url = config['confluence_url']

try:
    confluence = Confluence(
        url=confluence_url,
        username=username,
        password=password,
        cloud=True
    )

    # Connection successful
    print("Successfully connected to Confluence.")

    page_id = 393559  # ID of the page you want to update or create
    page_title = 'README.md'

    # Read the contents of the local file 'README.md'
    with open('README.md', 'r') as file:
        page_content = file.read()

    # Update or create the page
    result = confluence.update_or_create(
        parent_id=page_id,
        title=page_title,
        body=page_content,
        representation='storage',
        full_width=False
    )

    if result:
        print(f"Page with ID {result['id']} has been updated or created successfully.")
    else:
        print("Failed to update or create the page.")

except Exception as e:
    # Connection failed or other error occurred
    print(f"Failed to connect to Confluence or encountered an error. Error: {str(e)}")

