import os
import sys
from src.carwings import CarwingsStatus

CW = CarwingsStatus(
    username = os.environ['CARWINGS_USERNAME'],
    password = os.environ['CARWINGS_PASSWORD']
)

def request_update(event, context):
    return CW.request_update()

def request_update_status(event, context):
    return CW.is_update_available(event)
    
if __name__ == '__main__':
    ru_resp = request_update(None, None)
    rus_resp = request_update_status(ru_resp, None)
    print(rus_resp)
