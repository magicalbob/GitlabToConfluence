# GitlabToConfluence

GitlabToConfluence is a tool designed to streamline the process of syncing README.md files from GitLab projects to Confluence pages, eliminating the need for additional licenses for users like Product Owners.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/magicalbob/GitlabToConfluence.git
   cd GitlabToConfluence
   ```

2. Install the required dependencies:
   ```
   pip install atlassian python-markdown markdown
   ```

3. Update the `config.json` file with your Confluence details and product information.

4. Ensure you have the necessary environment variables set up:
   - `CONFLUENCE_MAIL`: Confluence email ID
   - `CONFLUENCE_API`: Confluence API token
   - `GITLAB_TOKEN`: GitLab private token

## Usage

Run the tool by executing the following command in the project directory:
```
python src/GitlabToConfluence.py
```

The tool will download the README.md file for each product specified in the configuration, convert it to Confluence-friendly markup, and update the corresponding Confluence pages.

## Configuration
The `./config.json` file contains details about the Confluence URL, product information, and branch to fetch README.md files from GitLab.

``` 
{ 
  "confluence_url": "https://yourcompany.atlassian.net",
  "products": [
    { "product": "Dynamic365", "productId": your_project_id, "pageId": your_page_id }
  ]
}
```

## Testing

Unit tests are provided in the project, allowing you to validate the functionality. You can build a Docker image for testing and run it with the provided scripts.

Build the Docker image:
```
docker build -t test:GitlabToConfluence .
```

Run the Docker container:
```
docker run -tiv ${PWD}:/opt/pwd \
       -e "GITLAB_TOKEN=$GITLAB_TOKEN" \
       -e "CONFLUENCE_MAIL=$CONFLUENCE_MAIL" \
       -e "CONFLUENCE_API=$CONFLUENCE_API" \
       test:GitlabToConfluence
```

## Notes

- Ensure proper environment variables are set before running the tool.
- The tool supports fetching README.md files from GitLab branches, defaulting to `main`.
- Images referenced in README.md are downloaded and uploaded to Confluence as attachments.
- The tool automates the process of syncing README.md contents to Confluence pages efficiently.
