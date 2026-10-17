import csv
import tempfile
import unittest
from pathlib import Path

from main import (
    parse_log_line,
    load_log_file,
    analyse_log_levels,
    analyse_device_events,
    analyse_ping_results,
    assess_health,
    build_health_summary,
    export_health_summary_to_csv

)


class TestParseLogLine(unittest.TestCase):

    def test_parse_valid_log_line(self):

        line = (
            "2026-09-17 13:55:46,561 | INFO | "
            "Localhost is UP. Return code: 0"
        )

        result = parse_log_line(line)

        self.assertIsNotNone(result)

        self.assertEqual(
            result["timestamp"],
            "2026-09-17 13:55:46,561"
        )

        self.assertEqual(
            result["level"],
            "INFO"
        )

        self.assertEqual(
            result["message"],
            "Localhost is UP. Return code: 0"
        )

    def test_parse_malformed_log_line(self):

        line = "This is not a valid log entry"

        result = parse_log_line(line)

        self.assertIsNone(result)


class TestLoadLogFile(unittest.TestCase):

    def test_load_existing_log_file(self):

        log_file = (
            "data/network_diagnostic_sample.log"
        )

        result = load_log_file(log_file)

        self.assertIsNotNone(result)

        self.assertGreater(len(result), 0)

    def test_load_missing_log_file(self):

        result = load_log_file(
            "data/does_not_exist.log"
        )

        self.assertIsNone(result)


class TestAnalyseLogLevels(unittest.TestCase):

    def test_analyse_log_levels(self):

        entries = [
            {
                "timestamp": "2026-09-17 10:00:00,000",
                "level": "INFO",
                "message": "Test message"
            },
            {
                "timestamp": "2026-09-17 10:01:00,000",
                "level": "ERROR",
                "message": "Something failed"
            },
            {
                "timestamp": "2026-09-17 10:02:00,000",
                "level": "WARNING",
                "message": "Something looks wrong"
            },
            {
                "timestamp": "2026-09-17 10:03:00,000",
                "level": "INFO",
                "message": "Another message"
            },
            {
                "timestamp": "2026-09-17 10:04:00,000",
                "level": "NOTICE",
                "message": "Unknown level"
            }
        ]

        result = analyse_log_levels(entries)

        self.assertEqual(result["INFO"], 2)
        self.assertEqual(result["WARNING"], 1)
        self.assertEqual(result["ERROR"], 1)
        self.assertEqual(result["CRITICAL"], 0)
        self.assertEqual(result["UNKNOWN"], 1)


class TestAnalyseDeviceEvents(unittest.TestCase):

    def test_analyse_device_events(self):

        entries = [
            {
                "timestamp": "2026-09-17 13:55:46,561",
                "level": "INFO",
                "message": "Localhost is UP. Return code: 0"
            },
            {
                "timestamp": "2026-09-17 13:55:56,629",
                "level": "WARNING",
                "message": "Test Device is DOWN. Return code: 1"
            }
        ]

        result = analyse_device_events(entries)

        self.assertEqual(len(result), 2)

        self.assertEqual(
            result[0]["device"],
            "Localhost"
        )

        self.assertEqual(
            result[0]["event"],
            "UP"
        )

        self.assertEqual(
            result[1]["device"],
            "Test Device"
        )

        self.assertEqual(
            result[1]["event"],
            "DOWN"
        )


class TestAnalysePingResults(unittest.TestCase):

    def test_analyse_ping_results(self):

        entries = [
            {
                "timestamp": "2026-09-17 13:55:45,000",
                "level": "INFO",
                "message": (
                    "Checking device: Google DNS (8.8.8.8)"
                )
            },
            {
                "timestamp": "2026-09-17 13:55:49,672",
                "level": "INFO",
                "message": (
                    "Ping test completed for 8.8.8.8. "
                    "Packet loss: 0%, "
                    "Average latency: 43 ms, "
                    "Return code: 0"
                )
            },
            {
                "timestamp": "2026-09-17 13:55:55,000",
                "level": "INFO",
                "message": (
                    "Checking device: Test Device "
                    "(192.0.2.1)"
                )
            },
            {
                "timestamp": "2026-09-17 13:55:56,629",
                "level": "INFO",
                "message": (
                    "Ping test completed for 192.0.2.1. "
                    "Packet loss: 100%, "
                    "Average latency: None ms, "
                    "Return code: 1"
                )
            }
        ]

        result = analyse_ping_results(entries)

        self.assertEqual(len(result), 2)

        self.assertEqual(
            result[0]["device"],
            "Google DNS"
        )

        self.assertEqual(
            result[0]["ip"],
            "8.8.8.8"
        )

        self.assertEqual(
            result[0]["packet_loss"],
            0
        )

        self.assertEqual(
            result[0]["average_latency"],
            43
        )

        self.assertEqual(
            result[0]["return_code"],
            0
        )

        self.assertEqual(
            result[1]["device"],
            "Test Device"
        )

        self.assertEqual(
            result[1]["packet_loss"],
            100
        )

        self.assertIsNone(
            result[1]["average_latency"]
        )

        self.assertEqual(
            result[1]["return_code"],
            1
        )


class TestAssessHealth(unittest.TestCase):

    def test_healthy_device(self):

        result = assess_health(
            packet_loss=0,
            average_latency=43,
            return_code=0
        )

        self.assertEqual(
            result,
            "Healthy"
        )

    def test_warning_device(self):

        result = assess_health(
            packet_loss=0,
            average_latency=150,
            return_code=0
        )

        self.assertEqual(
            result,
            "Warning"
        )

    def test_critical_device(self):

        result = assess_health(
            packet_loss=100,
            average_latency=None,
            return_code=1
        )

        self.assertEqual(
            result,
            "Critical"
        )


class TestBuildHealthSummary(unittest.TestCase):

    def test_build_health_summary(self):

        device_events = [
            {
                "timestamp": "2026-09-17 13:55:49,673",
                "level": "INFO",
                "device": "Google DNS",
                "event": "UP",
                "message": "Google DNS is UP. Return code: 0"
            }
        ]

        ping_results = [
            {
                "timestamp": "2026-09-17 13:55:49,672",
                "device": "Google DNS",
                "ip": "8.8.8.8",
                "packet_loss": 0,
                "average_latency": 43,
                "return_code": 0
            }
        ]

        result = build_health_summary(
            device_events,
            ping_results
        )

        self.assertEqual(len(result), 1)

        self.assertEqual(
            result[0]["device"],
            "Google DNS"
        )

        self.assertEqual(
            result[0]["status"],
            "UP"
        )

        self.assertEqual(
            result[0]["health"],
            "Healthy"
        )

class TestExportHealthReport(unittest.TestCase):
    def test_export_health_summary_to_csv(self):
        health_summary =[
            {
                "timestamp": "2026-09-17 13:55:49,672",
                "device": "Google DNS",
                "ip": "8.8.8.8",
                "status": "UP",
                "packet_loss": 0,
                "average_latency": 43,
                "return_code": 0,
                "health": "Healthy"
            },
            {
                "timestamp": "2026-09-17 13:55:56,629",
                "device": "Test Device",
                "ip": "192.0.2.1",
                "status": "DOWN",
                "packet_loss": 100,
                "average_latency": None,
                "return_code": 1,
                "health": "Critical"
            }
        ]
        #Use a temporary directory for the test report.
        with tempfile.TemporaryDirectory() as temp_dir:
            output_file =(
                Path(temp_dir)/ "test_health_report.csv"
            )

            success = export_health_summary_to_csv(

            health_summary,
            output_file

            )

            #Check the export succeeded and create the file.
            self.assertTrue(success)
            self.assertTrue(output_file.exists())

            #Open the generated CSV and read its contents.
            with output_file.open(
                "r",
                newline="",
                encoding="utf-8"
                ) as file:

                reader = csv.DictReader(file)
                rows = list(reader)

                self.assertEqual(
                    reader.fieldnames,
                    [
                         "timestamp",
                        "device",
                        "ip",
                        "status",
                        "packet_loss",
                        "average_latency",
                        "return_code",
                        "health"
                    ]
                )

                #Check that both records were exported
                self.assertEqual(len(rows), 2)

                # Check the successful device's data.
                self.assertEqual(rows[0]["device"],"Google DNS")
                self.assertEqual(rows[0]["status"], "UP")
                self.assertEqual(rows[0]["health"], "Healthy")
                self.assertEqual(rows[0]["average_latency"], "43")


                #Check the failed device's data.
                self.assertEqual(rows[1]["device"], "Test Device")
                self.assertEqual(rows[1]["status"], "DOWN")
                self.assertEqual(rows[1]["packet_loss"], "100")
                self.assertEqual(rows[1]["health"], "Critical")

                # CSV represents Python's None value as an empty field.
                self.assertEqual(rows[1]["average_latency"], "N/A")

                self.assertIsNone(health_summary[1]["average_latency"])

if __name__ == "__main__":
    unittest.main()