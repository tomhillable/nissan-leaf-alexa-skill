import jsonschema
import unittest
from src.intents import GetChargeStatus
from unittest.mock import MagicMock


class IntentsTestCase(unittest.TestCase):
    def setUp(self):
        self.event = EVENT

    def test_get_charge_status(self):
        intent = GetChargeStatus(self.event)
        response = intent.process()
        self.assertIsNone(jsonschema.validate(response, RESPONSE_SCHEMA))



EVENT = {
   "session":{
      "new": True,
      "sessionId":"SessionId.xxx",
      "application":{
         "applicationId":"amzn1.ask.skill.xxx"
      },
      "attributes":{

      },
      "user":{
         "userId":"amzn1.ask.account.xxx"
      }
   },
   "request":{
      "type":"IntentRequest",
      "requestId":"EdwRequestId.xxx",
      "intent":{
         "name":"GetChargeStatus",
         "slots":{

         }
      },
      "locale":"en-GB",
      "timestamp":"2017-12-28T21:38:48Z"
   },
   "context":{
      "AudioPlayer":{
         "playerActivity":"IDLE"
      },
      "System":{
         "application":{
            "applicationId":"amzn1.ask.skill.xxx"
         },
         "user":{
            "userId":"amzn1.ask.account.xxx"
         },
         "device":{
            "supportedInterfaces":{

            }
         }
      }
   },
   "version":"1.0"
}

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "response": {
            "type": "object",
            "properties": {
                "card": {
                    "type": "object",
                    "properties": {
                        "content": {"type": "string"},
                        "image": {"type": "object"},
                        "text": {"type": "string"},
                        "title": {"type": "string"},
                        "type": {
                            "type": "string",
                            "enum": ["Simple", "Standard", "LinkAccount"]
                        }
                    },
                    "required": ["type"]
                },
                "directives": {"type": "array"},
                "outputSpeech": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string"},
                        "type": {
                            "type": "string",
                            "enum": ["PlainText", "SSML"]
                        },
                        "ssml": {"type": "string"}
                    },
                    "required": ["type"],
                    "anyOf": [
                        {"required": ["text"]},
                        {"required": ["ssml"]}
                    ]
                },
                "reprompt": {
                    "type": "object",
                    "properties": {
                        "outputSpeech": {
                            "type": "object",
                            "properties": {
                                "text": {"type": "string"},
                                "type": {
                                    "type": "string",
                                    "enum": ["PlainText", "SSML"]
                                },
                                "ssml": {"type": "string"}
                            },
                            "required": ["type"],
                            "anyOf": [
                                {"required": ["text"]},
                                {"required": ["ssml"]}
                            ]
                        }
                    }
                },
                "shouldEndSession": {"type": "boolean"}
            }
        },
        "sessionAttributes": {"type": "object"},
        "version": {"type": "string"}
    },
    "required": ["response", "version"]
}

if __name__ == '__main__':
    unittest.main()
