import math
import unittest
from unittest.mock import patch

from .. import misc_utils


class TestMiscUtils(unittest.TestCase):
    @patch('settings.TWILIO_FROM_NUMBER', '0123')
    @patch('settings.WHATSAPP_TO_NUMBER', '4567')
    @patch('utils.misc_utils.twilio_client.messages.create')
    def test_send_twilio_test_message(self, create_mock):
        misc_utils.send_twilio_test_message('a', 'b')
        create_mock.assert_called_once_with(from_='whatsapp:0123', to='whatsapp:4567', body='Your a code is b')

    @patch('settings.CANDLE_GRADIENT_THRESHOLDS', [0.006, 0.005])
    @patch('settings.CANDLE_GRADIENT_THRESHOLDS_DEFAULT', 0.003)
    def test_calculate_gradient_weight_function(self):
        self.assertTrue(math.isclose(misc_utils.calculate_gradient_weight_function(0), 0.006))
        self.assertTrue(math.isclose(misc_utils.calculate_gradient_weight_function(1), 0.005))
        self.assertTrue(math.isclose(misc_utils.calculate_gradient_weight_function(2), 0.003))
        self.assertTrue(math.isclose(misc_utils.calculate_gradient_weight_function(10), 0.003))
