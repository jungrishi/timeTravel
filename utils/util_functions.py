from urllib.parse import quote_plus
from config import Config

quote_payload = lambda dict: { k : quote_plus(str(v)) for k,v in dict.items()}
pluck_payloads = lambda dict, *args: (dict[arg] for arg in args) #destructing the payloads to get required values from dict


VERBS = {
    Config.COMMAND: ["send", "after", "in"]    
}

global_mentions = ['@channel', '@here', '@everyone']

time_period ={
    "second": {
        "mul_factor": 1
    }, 
    "minute": {
        "mul_factor": 60
    },
    "hour": {
        "mul_factor": 60*60
    }
}