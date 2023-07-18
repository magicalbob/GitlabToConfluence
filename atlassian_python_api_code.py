import os
from atlassian import Confluence

username = os.environ.get('CONFLUENCE_MAIL')
password = os.environ.get('CONFLUENCE_API')

try:
    confluence = Confluence(
        url='https://ellisbs.atlassian.net',
        username=username,
        password=password,
        cloud=True
    )

    # Connection successful
    print("Successfully connected to Confluence.")

    page_id = 393559  # ID of the page you want to update or create

    # Prepare the page content in Confluence Storage Format (e.g., Markdown)
    page_content = """
    <h2>New Page Title</h2>
    <p>This is the content of the new page.</p>
    """

    # Update or create the page
    result = confluence.update_or_create(
        parent_id = page_id,
        title='New Page Title',
        body=page_content,
        representation='storage',
        full_width = False
    )

    if result:
        print(f"Page with ID {result['id']} has been updated or created successfully.")
    else:
        print("Failed to update or create the page.")

except Exception as e:
    # Connection failed or other error occurred
    print(f"Failed to connect to Confluence or encountered an error. Error: {str(e)}")

