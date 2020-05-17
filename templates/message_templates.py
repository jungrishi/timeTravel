from flask import jsonify

class MessageTemplate:
    def __init__(self, message, time, *args, **kwargs):
        self.message = message
        self.time = time
    
    def get_template(self):
        get_block = self.__json__()
        print(get_block)
        response_template = get_block
        return response_template
    
    def __json__(self):
        return  {
            "blocks" : [
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
	            				"text": f"*When:(GMT)*\n{self.time} *+5:45*"
	            			}
	            		]
	            	}
	            ]}
        
