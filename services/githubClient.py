from decorators.logging import with_logging
from bot import Bot

from templates.deploye_stage import get_deploy_message, get_PR_message
from utils.util_functions import pluck_payloads
@with_logging
def send_message(payload):
    message_template = parse_github_request(payload)
    bot = Bot(message_template)
    return bot.send_status_message()
    
def parse_github_request(payload):
    print(payload)
    if 'is_pull_request' in payload and payload['is_pull_request']:
        state, title, body, repo_name, target_branch, app_url = pluck_payloads(payload, 'state', 'title', 'body', 'repo_name', 'target_branch', 'app_url')
        return get_PR_message(state, title, target_branch, repo_name, body, app_url)
    else:
        state, repo_name, deployed_to, app_url =  pluck_payloads(payload, 'state', 'repo_name', 'deployed_to', 'app_url')  
        return get_deploy_message(state, deployed_to, repo_name, app_url)