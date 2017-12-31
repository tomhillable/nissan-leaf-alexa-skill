import jsonschema
from pycarwings2.responses import CarwingsBatteryStatusResponse, CarwingsLoginResponse
from pycarwings2.pycarwings2 import CarwingsError, Leaf
from datetime import date
import src.carwings
import unittest
from unittest.mock import MagicMock


class RequestUpdateTestCase(unittest.TestCase):
    def setUp(self):
        self.cw = src.carwings.CarwingsStatus('', '')
        self.cw.session.connect = MagicMock(return_value=CarwingsLoginResponse(APP_RESP))
        self.leaf = Leaf(self.cw.session, CarwingsLoginResponse(APP_RESP).leafs[0])
        self.leaf.request_update = MagicMock(return_value='AAAAAAAAAAAA')
        self.leaf.get_driving_analysis = MagicMock(return_value={'a': 1})
        self.leaf.get_latest_battery_status = MagicMock(return_value={'b': 1})
        self.leaf.get_electric_rate_simulation = MagicMock(return_value={'c': 1})
        self.leaf.get_climate_control_schedule = MagicMock(return_value=None)
        self.cw.session.get_leaf = MagicMock(return_value=self.leaf)

    def test_login(self):
        self.assertIsInstance(self.cw._login(), CarwingsLoginResponse)
        self.cw.session.connect = MagicMock(side_effect=CarwingsError('Boom!'))
        self.assertRaises(src.carwings.CarwingsLoginException, self.cw._login)

    def test_request_update_schema(self):
        schema = {
            "type": "object",
            "properties": {
                "resultKey": {"type": "string"}
            },
            "required": ["resultKey"]
        }
        response = self.cw.request_update()
        self.assertIsNone(jsonschema.validate(response, schema))

    def test_is_update_available(self):
        event = {'resultKey': 'foo'}
        schema = {
            "type": "object",
            "properties": {
                "updateAvailable": {"type": "boolean"},
            },
            "required": ["updateAvailable"]
        }
        self.leaf.get_status_from_update = MagicMock(return_value=None)
        response = self.cw.is_update_available(event)
        self.assertIsNone(jsonschema.validate(response, schema))
        self.assertFalse(response.get('updateAvailable'))

        self.leaf.get_status_from_update = MagicMock(
            return_value=CarwingsBatteryStatusResponse(BATTERY_RESP))
        response = self.cw.is_update_available(event)
        self.assertIsNone(jsonschema.validate(response, schema))
        self.assertTrue(response.get('updateAvailable'))
        self.leaf.get_status_from_update.assert_called_with('foo')
    
    def test_collate_data(self):
        expected = { 'a': 1, 'b': 1, 'c': 1 }
        self.assertEqual(expected, self.cw._collate_data())
        
        self.leaf.get_driving_analysis.assert_called_once()
        self.leaf.get_latest_battery_status.assert_called_once()
        month = date.today().strftime('%Y%m')
        self.leaf.get_electric_rate_simulation.assert_called_once_with(month)
        self.leaf.get_climate_control_schedule.assert_called_once()

APP_RESP = {
    "status": 200,
    "vehicleInfo": [
        {
            "vin": "AAAAAAAA0A0000000",
            "nickname": "Leaf",
            "charger20066": "false",
            "telematicsEnabled": "true",
            "custom_sessionid": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        }
    ],
    "vehicle": {
        "profile": {
            "vin": "AAAAAAAA0A0000000",
            "gdcUserId": "",
            "gdcPassword": "",
            "encAuthToken": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
            "dcmId": "000000000000",
            "status": "true",
            "statusDate": "2017/02/16 23:00",
            "nickname": "Leaf"
        }
    },
    "EncAuthToken": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "CustomerInfo": {
        "UserId": "foobar",
        "Language": "en_GB",
        "Timezone": "Europe/Paris",
        "RegionCode": "NE",
        "OwnerId": "0000000000",
        "EMailAddress": "foo@bar.com",
        "Nickname": "Leaf",
        "Country": "GB",
        "VehicleImage": "/content/language/default/images/img/ph_car.jpg",
        "UserVehicleBoundDurationSec": "946771200",
        "VehicleInfo": {
            "VIN": "AAAAAAAA0A0000000",
            "DCMID": "000000000000",
            "SIMID": "00000000000000000000",
            "NAVIID": "000000000000",
            "EncryptedNAVIID": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
            "MSN": "000000000000000",
            "LastVehicleLoginTime": "",
            "UserVehicleBoundTime": "2017-02-17T18:53:30Z",
            "LastDCMUseTime": "2017/12/28 13:08"
        }
    },
    "UserInfoRevisionNo": "1"
}

BATTERY_RESP = {
    "status": 200,
    "message": "success",
    "responseFlag": "1",
    "operationResult": "START",
    "timeStamp": "2016-01-02 17:17:38",
    "cruisingRangeAcOn": "115328.0",
    "cruisingRangeAcOff": "117024.0",
    "currentChargeLevel": "0",
    "chargeMode": "220V",
    "pluginState": "CONNECTED",
    "charging": "YES",
    "chargeStatus": "CT",
    "batteryDegradation": "10",
    "batteryCapacity": "12",
    "timeRequiredToFull": {
        "hours": "",
        "minutes": ""
    },
    "timeRequiredToFull200": {
        "hours": "",
        "minutes": ""
    },
    "timeRequiredToFull200_6kW": {
        "hours": "",
        "minutes": ""
    }
}

if __name__ == '__main__':
    unittest.main()
