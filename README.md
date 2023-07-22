atlassian_python_api_code.py
============================

This is a tool for where you have people, like Product Owners, who need to see README.md files - but you don't want to pay for them to have a gitlab license! It copies README.md files to your Confluence.

Takes a `./config.json` file like this:

``` 
{ 
  "confluence_url": "https://ellisbs.atlassian.net",
  "products": [
    { "product": "Dynamic365", "productId": 46187091, "pageId": 393559 }
  ]
}
```

It downloads each of the gitlab.com products README.md file from branch main and uploads them to the corresponding Confluence page.

Requires confluence mail id in env var `CONFLUENCE_MAIL` and an API token in env var CONFLUENCE_API.

Testing
=======

A unit test module is provided, along with a Dockerfile making it easy to run and a few scripts and things.

To build the docker image:

	docker build -t test:GitlabToConfluence .

And to run it:

	docker run -tiv ${PWD}:/opt/pwd \
	       -e "GITLAB_TOKEN=$GITLAB_TOKEN" \
	       -e "CONFLUENCE_MAIL=$CONFLUENCE_MAIL" \
	       -e "CONFLUENCE_API=$CONFLUENCE_API" \
	       test:GitlabToConfluence
