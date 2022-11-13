import datetime
from django.utils import timezone

def get_test_status(context: dict) -> str:
    at_start = context.get('test').at_start
    at_finish = context.get('test').at_finish
    time_now = datetime.datetime.now(at_start.tzinfo)

    status = None
    if at_start < time_now < at_finish:
        status = 'open'
    elif time_now < at_start:
        status = 'wait'
    else:
        status = 'close'

    return status
    