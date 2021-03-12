import json
from unittest import TestCase
from unittest.mock import Mock, patch

from core.message.from_message import SmartAppFromMessage
from core.utils.utils import current_time_ms
from smart_kit.configs import set_config_defaults


def patch_get_app_config(mock_get_app_config):
    result = Mock(spec=[], name='app_config')
    set_config_defaults(result)
    mock_get_app_config.return_value = result


class TestFromMessage(TestCase):
    def test_1(self):
        input_msg = {
            "messageId": 2,
            "uuid": {"userChannel": "B2C", "userId": "userId", "sub": "sub"},
            "payload": {
                "message": {
                    "original_text": "сверни приложение"
                },
                "device": {
                    "platformType": "android",
                    "platformVersion": "9",
                    "surface": "STARGATE",
                    "surfaceVersion": "1.56.20200828144304",
                    "features": {"appTypes": ["APK", "WEB_APP", "DIALOG"]},
                    "capabilities": {"mic": {"available": True},
                                     "screen": {"available": True},
                                     "speak": {"available": True}},
                    "deviceId": "34534545345345",
                    "deviceManufacturer": "SberDevices",
                    "deviceModel": "stargate",
                    "additionalInfo": {}
                }
            },
            "messageName": "MESSAGE_TO_SKILL"
        }
        json_input_msg = json.dumps(input_msg, ensure_ascii=False)
        topic = "test"
        headers = []
        current_time = current_time_ms()
        message = SmartAppFromMessage(value=json_input_msg, topic_key=topic, headers=headers, creation_time=current_time)

        self.assertAlmostEqual(message.creation_time, current_time)
        self.assertEqual(2, message.incremental_id)
        self.assertEqual(input_msg["uuid"]["userChannel"], message.channel)
        self.assertEqual(input_msg["messageName"], message.type)
        self.assertEqual(input_msg["uuid"]["userId"], message.uid)
        self.assertEqual(json_input_msg, message.value)
        self.assertEqual("sub_userId_B2C", message.db_uid)
        self.assertDictEqual(input_msg["uuid"], message.uuid)
        self.assertDictEqual(input_msg["payload"], message.payload)
        device = input_msg["payload"]["device"]
        self.assertEqual(device["platformType"], message.device.platform_type)
        self.assertEqual(device["platformVersion"], message.device.platform_version)
        self.assertEqual(device["surface"], message.device.surface)
        self.assertEqual(device["surfaceVersion"], message.device.surface_version)
        self.assertEqual(device["features"], message.device.features)
        self.assertEqual(device["capabilities"], message.device.capabilities)
        self.assertEqual(device["additionalInfo"], message.device.additional_info)
        self.assertEqual(topic, message.topic_key)

    @patch('smart_kit.configs.get_app_config')
    def test_valid_true(self, mock_get_app_config):
        patch_get_app_config(mock_get_app_config)
        input_msg = {
            "messageId": 2,
            "sessionId": 234,
            "uuid": {"userChannel": "web", "userId": 99, "chatId": 80},
            "payload": {"key": "some payload"},
            "messageName": "some_type"
        }
        json_input_msg = json.dumps(input_msg, ensure_ascii=False)
        headers = [('test_header', 'result')]
        message = SmartAppFromMessage(json_input_msg, headers=headers)
        self.assertTrue(message.validate())

    @patch('smart_kit.configs.get_app_config')
    def test_valid_false(self, mock_get_app_config):
        patch_get_app_config(mock_get_app_config)
        input_msg = {
            "uuid": {"userChannel": "web", "userId": 99, "chatId": 80},
            "payload": "some payload"
        }
        headers = [('test_header', 'result')]
        json_input_msg = json.dumps(input_msg, ensure_ascii=False)

        message = SmartAppFromMessage(json_input_msg, headers=headers)
        self.assertFalse(message.validate())
