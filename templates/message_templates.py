from flask import jsonify

class MessageTemplate:
    def __init__(self, message, time, *args, **kwargs):
        self.message = message
        self.time = time
    
    def get_template(self):
        get_block = self.__dict__()
        print(get_block)
        response_template = jsonify(get_block)
        return response_template
    
    def __dict__(self):
        blocks = [
	            	{
	            		"type": "section",
	            		"text": {
	            			"type": "mrkdwn",
	            			"text": f"You have a new Scheduled Message:\n* <{self.message}>*"
	            		}
	            	},
	            	{
	            		"type": "section",
	            		"fields": [
	            			{
	            				"type": "mrkdwn",
	            				"text": "*Type:*\nScheduled Message"
	            			},
	            			{
	            				"type": "mrkdwn",
	            				"text": f"*When:*\n{self.time}"
	            			}
	            		]
	            	}
	            ]
        return blocks