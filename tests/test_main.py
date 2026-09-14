import unittest

import main


class TestDeviceValidation(unittest.TestCase):

    def test_valid_devices(self):

        devices = [
            {
                "name": "Router",
                "ip": "192.168.1.1"
            }
        ]

        self.assertTrue(main.validate_devices(devices))

    def test_empty_device_list(self):

        devices = []

        self.assertFalse(main.validate_devices(devices))

    def test_missing_ip(self):

        devices = [
            {
                "name": "Router"
            }
        ]

        self.assertFalse(main.validate_devices(devices))

    def test_invalid_ip(self):

        devices = [
            {
                "name": "Router",
                "ip": "hello"
            }
        ]

        self.assertFalse(main.validate_devices(devices))


class TestPingParser(unittest.TestCase):

    def test_parse_ping_output(self):

        output = """
        Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
        Approximate round trip times in milli-seconds:
            Minimum = 10ms, Maximum = 20ms, Average = 15ms
        """

        packet_loss, latency = main.parse_ping_output(output)

        self.assertEqual(packet_loss, 0)
        self.assertEqual(latency, 15)

    def test_parse_packet_loss(self):

        output = """
        Packets: Sent = 4, Received = 3, Lost = 1 (25% loss),
        Approximate round trip times in milli-seconds:
            Minimum = 10ms, Maximum = 40ms, Average = 20ms
        """

        packet_loss, latency = main.parse_ping_output(output)

        self.assertEqual(packet_loss, 25)
        self.assertEqual(latency, 20)


class TestHealthAssessment(unittest.TestCase):

    def test_healthy_device(self):

        result = main.assess_health(0, 20)

        self.assertEqual(result, "Healthy")

    def test_warning_device(self):

        result = main.assess_health(25, 150)

        self.assertEqual(result, "Warning")

    def test_critical_device(self):

        result = main.assess_health(75, 300)

        self.assertEqual(result, "Critical")


if __name__ == "__main__":
    unittest.main()