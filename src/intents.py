class Intent:
    def __init__(self, event):
        self.event = event
    
    def process(self):
        raise NotImplementedError

class GetChargeStatus(Intent):
    def process(self):
        resp = {
            'response': {},
            'version': '1.0'
        }
        return resp

