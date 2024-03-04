#!/usr/bin/env python3
import os
import json
import requests
import markdown
from atlassian import Confluence

def process_line(input_line):
    output_line = markdown.markdown(input_line)
    return output_line

def convert_gitlab_to_confluence(input_file, output_file, product_id):
    with open(input_file, 'r') as file:
        gitlab_text = file.readlines()

    code_block_opening = False
    confluence_lines = []
    image_attachments = []

    for line in gitlab_text:
        line = line.strip()
        if line.startswith('```'):
            if code_block_opening:
                confluence_lines.append('</code>')
            else:
                confluence_lines.append('<code class="language-" style="white-space: pre;">')
            code_block_opening = not code_block_opening
        else:
            # Check for image references and download/upload them
            if line.startswith('!['):
                # Extract image URL from Markdown syntax
                image_url = line.split('](')[1].split(')')[0]
                image_name = os.path.basename(image_url)
                
                # Download the image from GitLab
                response = requests.get(image_url)
                response.raise_for_status()
                image_data = response.content
                
                # Upload the image to Confluence and get attachment ID
                attachment_id = confluence.attachments.upload(
                    page_id=page_id,
                    file=image_data,
                    title=image_name
                )['results'][0]['id']
                
                # Replace the image reference with Confluence macro
                line = f'!custom:com.atlassian.confluence.macro.core:image|src=/download/attachments/{product_id}/{attachment_id}|align=center|width=500!'

                # Store attachment ID for later use (if needed)
                image_attachments.append(attachment_id)
            
            confluence_lines.append(process_line(line))

    # Check if there is an unclosed code block at the end
    if code_block_opening:
        confluence_lines.append('</code>')

    # Convert the processed lines to a single string
    confluence_text = '\n'.join(confluence_lines)

    with open(output_file, 'w') as file:
        file.write(confluence_text)

    return image_attachments

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

    # Fetch the branch from the config or default to 'main'
    branch = config.get('branch', 'main')

    for product in products:
        product_name = product['product']
        product_id = product['productId']
        page_id = product['pageId']
        page_title = f'{product_name} README.md'

        # Fetch the file content from GitLab using the specified branch
        gitlab_token = os.environ.get('GITLAB_TOKEN')
        gitlab_file_url = f"https://gitlab.com/api/v4/projects/{product_id}/repository/files/README.md?private_token={gitlab_token}&ref={branch}"
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
        image_attachments = convert_gitlab_to_confluence(file_path, confluence_file_path, product_id)

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
