from datetime import time

def get_deploy_message(status, deployed_to, repo_name, url, created_at):
    return [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "<!here> DEV Deployment Progress"
			}
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": f"*Status:*\n{status}"
				},
				{
					"type": "mrkdwn",
					"text": f"*Environment:*\n{deployed_to}"
				},
				{
					"type": "mrkdwn",
					"text": f"*Created At:*\n{created_at}"
				},
				{
					"type": "mrkdwn",
					"text": f"*Repo:*\n{repo_name}"
				},
				{
					"type": "mrkdwn",
					"text": f"*Web URl:*\n{url}"
				}
			]
		}
	]

def get_PR_message(status,title, target_branch, repo_name,body, url, created_at):
    return [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"<!here> New Pull request Created\n*Title*: {title}"
			}
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": f"*Status:*\n{status}"
				},
				{
					"type": "mrkdwn",
					"text": f"*Target Branch:*\n {target_branch}"
				},
				{
					"type": "mrkdwn",
					"text": f"*Created At:*\n{created_at}"
				},
				{
					"type": "mrkdwn",
					"text": f"*Repo:*\n{repo_name}"
				},
				{
					"type": "mrkdwn",
					"text": f"*Body:*\n{body}"
				},
				{
					"type": "mrkdwn",
					"text": f"*Web URl:*\n{url}"
				}
			]
		}
	]