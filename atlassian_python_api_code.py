#!/usr/bin/env python3
import os
import json
import requests
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

    # Fetch the file content from GitLab
    gitlab_token = os.environ.get('GITLAB_TOKEN')
    gitlab_file_url = f"https://gitlab.com/api/v4/projects/46187091/repository/files/README.md?private_token={gitlab_token}&ref=main"
    response = requests.get(gitlab_file_url)
    response.raise_for_status()
    gitlab_file_content = response.json()['content']

    # Decode the file content from base64
    import base64
    page_content = base64.b64decode(gitlab_file_content).decode('utf-8')

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

