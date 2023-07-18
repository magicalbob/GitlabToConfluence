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
    print(confluence.__dir__())

    # Connection successful
    print("Successfully connected to Confluence.")

    print(confluence.get_page_space(page_id=393559))

#    # Get all pages
#    pages = confluence.get_all_pages()
#
#    # Iterate over the pages and print their titles
#    for page in pages:
#        print(page['title'])

except Exception as e:
    # Connection failed or other error occurred
    print(f"Failed to connect to Confluence or encountered an error. Error: {str(e)}")

