curl "https://gitlab.com/api/v4/projects/46187091/repository/files/README.md?private_token=$GITLAB_TOKEN&ref=main"|jq .content|cut -d\" -f2|base64 --decode> README.md

curl -vvvu $CONFLUENCE_MAIL:$CONFLUENCE_API -X POST -H "X-Atlassian-Token: nocheck" -H "Content-Type: application/json" -F "file=@README.md" "https://ellisbs.atlassian.net/rest/api/content/393559/child/attachment" 2>/dev/null # | jq -r '.id'

