import logging
import os
import sys
from src.carwings import CarwingsStatus
from src.intents import GetChargeStatus

logging.basicConfig(level=logging.DEBUG)
CW = CarwingsStatus(
    username = os.environ.get('CARWINGS_USERNAME'),
    password = os.environ.get('CARWINGS_PASSWORD')
)

def alexa(event, context):
    logging.debug(event)
    return GetChargeStatus(event).process()
    
def request_update(event, context):
    return CW.request_update()

def request_update_status(event, context):
    return CW.is_update_available(event)
    
if __name__ == '__main__':
    ru_resp = request_update(None, None)
    rus_resp = request_update_status(ru_resp, None)
    print(rus_resp)
