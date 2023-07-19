curl "https://gitlab.com/api/v4/projects/46187091/repository/files/README.md?private_token=$GITLAB_TOKEN&ref=main"|jq .content|cut -d\" -f2|base64 --decode> README.md

python atlassian_python_api_code.py
