import time
import inflect

from utils.util_functions import pluck_payloads, quote_payload, VERBS, global_mentions, time_period
from exceptions.custom_exception import CommandParserException, UserMentionException

inflect_engine = inflect.engine()

def command_parser(payload):
    try:
        parts = payload["text"].split(" ")
        verb = VERBS[payload['command']]
        whom = parts[1]
        message = parts[2:]
        whom_mentions = ''

        if whom[0] != '@':
            raise UserMentionException()

        if whom in global_mentions:
            whom_mentions = '!' + whom[1:]
        else:
            whom_mentions = whom

        find_index = 0
        count = 1
        for i in range(len(message)-1, 0, -1):
            if message[i] in verb:
                find_index = i
                count = 0
                break
        if count == 1:
            raise CommandParserException

        text_message = message[:find_index]
        time_ = message[find_index+1:]
        message_to_send = f'<{whom_mentions}>' + " " + " ".join(i for i in text_message)
        timestamp = -1
        error = 0
        for k, v in time_period.items():
            if time_[1] in k or time_[1] in inflect_engine.plural(k):
                time_in_second = int(time_[0]) * int(v['mul_factor'])
                timestamp = time.time() + int(time_in_second)
                break
        if timestamp < 0 :
            raise CommandParserException

        payload['timestamp'] = timestamp
        payload['message'] = message_to_send
        return payload
    except CommandParserException as err:
        raise CommandParserException #command Parser Error
    