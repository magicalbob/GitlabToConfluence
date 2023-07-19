atlassian_python_api_code.py
============================

Takes a `./config.json` file like this:

``` 
{ 
  "confluence_url": "https://ellisbs.atlassian.net",
  "products": [
    { "productId": 46187091, "pageId": 393559 }
  ]
}
```

It downloads each of the gitlab.com products README.md file from branch main and uploads them to the corresponding Confluence page.

Requires confluence mail id in env var `CONFLUENCE_MAIL` and an API token in env var CONFLUENCE_API.
