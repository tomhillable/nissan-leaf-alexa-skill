import logging
import pycarwings2
import sys

from datetime import date
from pycarwings2.responses import CarwingsBatteryStatusResponse


class CarwingsStatus:
    def __init__(self, username, password):
        self._leaf = None
        self.log = logging.getLogger()
        self.log.setLevel(logging.INFO)
        self.session = pycarwings2.Session(username, password, 'NE')

    def _login(self):
        if not self.session.logged_in:
            self.log.info('Logging in to carwings')
            try:
                result = self.session.connect()
            except pycarwings2.pycarwings2.CarwingsError:
                raise CarwingsLoginException('Unable to log in to car wings')
            return result

    def request_update(self):
        self.log.info('Requesting update from Nissan')
        result_key = self.leaf().request_update()
        return {"resultKey": result_key}

    def is_update_available(self, event):
        rk = event['resultKey']
        self.log.info('Checking if update available')
        self.log.info('Input event was: ')
        self.log.info(event)
        ret = isinstance(self.leaf().get_status_from_update(rk),
                         CarwingsBatteryStatusResponse)
        result = {'updateAvailable': ret}
        if ret:
            result.update(self._collate_data())
        self.log.info('Result was: ')
        self.log.info(result)
        return result
    
    def leaf(self):
        if self._leaf:
            return self._leaf
        self._login()
        self.log.info('Getting car information')
        return self.session.get_leaf()
        
    def _collate_data(self):
        dicts = []
        res = {}
        month = date.today().strftime('%Y%m')
        self.log.info('Collecting date from update')
        dicts.append(self.leaf().get_driving_analysis())
        dicts.append(self.leaf().get_latest_battery_status())
        dicts.append(self.leaf().get_electric_rate_simulation(month))
        dicts.append(self.leaf().get_climate_control_schedule())
        for d in dicts:
            if d:
                res.update(d)
        self.log.info('Collected data:')
        self.log.info(res)
        return res


class CarwingsLoginException(Exception):
    '''Raise when unable to log in to car wings'''


if __name__ == '__main__':
    print(CarwingsStatus(
        username=sys.argv[1], password=sys.argv[2]).request_update())
