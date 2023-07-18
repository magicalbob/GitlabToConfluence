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
    # Perform further operations on Confluence if needed
    # ...
except Exception as e:
    # Connection failed
    print(f"Failed to connect to Confluence. Error: {str(e)}")

