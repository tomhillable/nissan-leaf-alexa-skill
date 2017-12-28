import pycarwings2
import sys

from pycarwings2.responses import CarwingsBatteryStatusResponse


class CarwingsStatus:
    def __init__(self, username, password):
        self.session = pycarwings2.Session(username, password, 'NE')

    def _login(self):
        if not self.session.logged_in:
            try:
                result = self.session.connect()
            except pycarwings2.pycarwings2.CarwingsError:
                raise CarwingsLoginException('Unable to log in to car wings')
            return result

    def request_update(self):
        self._login()
        leaf = self.session.get_leaf()
        result_key = leaf.request_update()
        return {"resultKey": result_key}

    def is_update_available(self, event):
        rk = event['resultKey']
        self._login()
        l = self.session.get_leaf()
        ret = isinstance(l.get_status_from_update(rk),
                         CarwingsBatteryStatusResponse)
        return {'updateAvailable': ret}


class CarwingsLoginException(Exception):
    '''Raise when unable to log in to car wings'''


if __name__ == '__main__':
    print(CarwingsStatus(
        username=sys.argv[1], password=sys.argv[2]).request_update())