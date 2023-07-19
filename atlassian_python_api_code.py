#!/usr/bin/env python3
import os
import json
import requests
from atlassian import Confluence


def convert_gitlab_to_confluence(input_file, output_file):
    with open(input_file, 'r') as file:
        gitlab_text = file.read()

    # Convert GitLab Markdown to Confluence markup
    confluence_text = gitlab_to_confluence(gitlab_text)

    with open(output_file, 'w') as file:
        file.write(confluence_text)


def gitlab_to_confluence(gitlab_text):
    # Perform the necessary conversions from GitLab Markdown to Confluence markup
    # Customize this function to implement the specific conversion rules you need
    # Example conversions:
    confluence_text = gitlab_text.replace('#', 'h1.').replace('##', 'h2.').replace('###', 'h3.')
    confluence_text = confluence_text.replace('**', '*').replace('__', '*')
    confluence_text = confluence_text.replace('_', '+').replace('`', '{{').replace('```', '{code}')

    return confluence_text


# Read the configuration from 'config.json'
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

confluence_url = config['confluence_url']
products = config['products']

username = os.environ.get('CONFLUENCE_MAIL')
password = os.environ.get('CONFLUENCE_API')

try:
    confluence = Confluence(
        url=confluence_url,
        username=username,
        password=password,
        cloud=True
    )

    # Connection successful
    print("Successfully connected to Confluence.")

    for product in products:
        product_id = product['productId']
        page_id = product['pageId']
        page_title = 'README.md'

        # Fetch the file content from GitLab
        gitlab_token = os.environ.get('GITLAB_TOKEN')
        gitlab_file_url = f"https://gitlab.com/api/v4/projects/{product_id}/repository/files/README.md?private_token={gitlab_token}&ref=main"
        response = requests.get(gitlab_file_url)
        response.raise_for_status()
        gitlab_file_content = response.json()['content']

        # Decode the file content from base64
        import base64
        page_content = base64.b64decode(gitlab_file_content).decode('utf-8')

        # Save the file in the ./work/ directory
        file_path = f"./work/README-{product_id}.md"
        with open(file_path, 'w') as file:
            file.write(page_content)

        print(f"README.md file downloaded and saved for product ID {product_id}.")

        # Convert GitLab Markdown to Confluence markup
        confluence_file_path = f"./work/README-{product_id}.txt"
        convert_gitlab_to_confluence(file_path, confluence_file_path)

        # Read the Confluence markup from the converted file
        with open(confluence_file_path, 'r') as file:
            confluence_content = file.read()

        # Update or create the page with the Confluence markup
        result = confluence.update_or_create(
            parent_id=page_id,
            title=page_title,
            body=confluence_content,
            representation='storage',
            full_width=False
        )

        if result:
            print(f"Page with ID {result['id']} has been updated or created successfully for product ID {product_id}.")
        else:
            print(f"Failed to update or create the page for product ID {product_id}.")

except Exception as e:
    # Connection failed or other error occurred
    print(f"Failed to connect to Confluence or encountered an error. Error: {str(e)}")

