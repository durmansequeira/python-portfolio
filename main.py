import subprocess
import csv
import json
import sys
import ipaddress
import re
import logging


# Configure logging
logging.basicConfig(
    filename="network_diagnostic.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# Load device configuration from JSON
def load_devices():
    logger.info("Loading device configuration.")

    try:
        with open("devices.json", "r") as file:
            devices = json.load(file)

        logger.info("Device configuration loaded successfully.")
        return devices

    except FileNotFoundError:
        logger.error("devices.json was not found.")
        print("ERROR: devices.json was not found.")
        return None

    except json.JSONDecodeError:
        logger.error("devices.json contains invalid JSON.")
        print("ERROR: devices.json contains invalid JSON.")
        return None

    except OSError as error:
        logger.error(f"Could not read devices.json: {error}")
        print(f"ERROR: Could not read devices.json: {error}")
        return None


# Validate device configuration
def validate_devices(devices):

    logger.info("Validating device configuration.")

    if not isinstance(devices, list):
        logger.error("Device configuration is not a list.")
        print("ERROR: Device configuration must be a list.")
        return False

    if not devices:
        logger.error("Device configuration is empty.")
        print("ERROR: Device configuration is empty.")
        return False

    for device in devices:

        if not isinstance(device, dict):
            logger.error("A device entry is not a dictionary.")
            print("ERROR: Each device must be a dictionary.")
            return False

        if "name" not in device:
            logger.error("A device is missing the 'name' field.")
            print("ERROR: A device is missing the 'name' field.")
            return False

        if "ip" not in device:
            logger.error("A device is missing the 'ip' field.")
            print("ERROR: A device is missing the 'ip' field.")
            return False

        if not isinstance(device["name"], str) or not device["name"].strip():
            logger.error("A device has an invalid name.")
            print("ERROR: Device name must be a non-empty string.")
            return False

        if not isinstance(device["ip"], str):
            logger.error(
                f"IP address for {device['name']} is not a string."
            )
            print(
                f"ERROR: IP address for {device['name']} must be a string."
            )
            return False

        try:
            ipaddress.ip_address(device["ip"])

        except ValueError:
            logger.error(
                f"Invalid IP address for {device['name']}: {device['ip']}"
            )
            print(
                f"ERROR: Invalid IP address for "
                f"{device['name']}: {device['ip']}"
            )
            return False

    logger.info(
        f"Device configuration validated successfully. "
        f"{len(devices)} device(s) found."
    )

    return True


# Parse Windows ping output
def parse_ping_output(output):

    packet_loss = None
    average_latency = None

    packet_loss_match = re.search(
        r"Lost\s*=\s*\d+\s*\((\d+)%\s*loss\)",
        output,
        re.IGNORECASE
    )

    if packet_loss_match:
        packet_loss = int(packet_loss_match.group(1))

    latency_match = re.search(
        r"Average\s*=\s*(\d+)ms",
        output,
        re.IGNORECASE
    )

    if latency_match:
        average_latency = int(latency_match.group(1))

    return packet_loss, average_latency


# Execute ping command
def ping_host(target):

    logger.info(f"Starting ping test for {target}.")

    try:
        result = subprocess.run(
            ["ping", "-n", "4", "-w", "1000", target],
            capture_output=True,
            text=True,
            timeout=10
        )

        output = result.stdout

        if "could not find host" in output.lower():
            logger.warning(f"Host could not be resolved: {target}")
            return "Host_not_found", None, None

        packet_loss, average_latency = parse_ping_output(output)

        if packet_loss is None:
            logger.error(
                f"Could not parse packet loss from ping output for {target}."
            )
            return "PARSE_ERROR", None, None

        logger.info(
            f"Ping test completed for {target}. "
            f"Packet loss: {packet_loss}%, "
            f"Average latency: {average_latency} ms, "
            f"Return code: {result.returncode}"
        )

        return result.returncode, packet_loss, average_latency

    except subprocess.TimeoutExpired:
        logger.warning(f"Ping test timed out: {target}")
        return "TIMEOUT", None, None


# Assess network health
def assess_health(packet_loss, average_latency):

    if (
        packet_loss == 0
        and average_latency is not None
        and average_latency < 100
    ):
        return "Healthy"

    elif (
        packet_loss is not None
        and packet_loss < 50
        and average_latency is not None
        and average_latency < 200
    ):
        return "Warning"

    else:
        return "Critical"


# Main program
def main():

    # Load devices
    devices = load_devices()

    if devices is None:
        print(
            "Program stopped because the device configuration "
            "could not be loaded."
        )
        logger.critical(
            "Program stopped: configuration could not be loaded."
        )
        return 1

    # Validate devices
    if not validate_devices(devices):
        print(
            "Program stopped because the device configuration "
            "is invalid."
        )
        logger.critical(
            "Program stopped: device configuration is invalid."
        )
        return 1

    # Store diagnostic results
    results = []

    # Check every device
    for device in devices:

        name = device["name"]
        ip = device["ip"]

        print(f"\nChecking {name} ({ip})")
        logger.info(f"Checking device: {name} ({ip})")

        status, packet_loss, average_latency = ping_host(ip)

        if status == "Host_not_found":

            print(f"{name} could not be resolved.")
            logger.warning(f"{name} could not be resolved.")

            results.append({
                "name": name,
                "ip": ip,
                "status": "Host_not_found",
                "packet_loss": None,
                "average_latency": None,
                "health": None
            })

        elif status == "TIMEOUT":

            print("Request timed out.")
            logger.warning(f"Request timed out for {name}.")

            results.append({
                "name": name,
                "ip": ip,
                "status": "TIMEOUT",
                "packet_loss": None,
                "average_latency": None,
                "health": None
            })

        elif status == "PARSE_ERROR":

            print("ERROR: Could not interpret the ping output.")
            logger.error(f"Ping output parsing failed for {name}.")

            results.append({
                "name": name,
                "ip": ip,
                "status": "PARSE_ERROR",
                "packet_loss": None,
                "average_latency": None,
                "health": None
            })

        elif status == 0:

            health = assess_health(
                packet_loss,
                average_latency
            )

            print(f"{name} is UP")
            print(f"Packet loss: {packet_loss}%")
            print(f"Average latency: {average_latency} ms")
            print(f"Health status: {health}")

            logger.info(
                f"{name} is UP. "
                f"Packet loss: {packet_loss}%, "
                f"Average latency: {average_latency} ms, "
                f"Health: {health}"
            )

            results.append({
                "name": name,
                "ip": ip,
                "status": "UP",
                "packet_loss": packet_loss,
                "average_latency": average_latency,
                "health": health
            })

        else:

            print(f"{name} is DOWN")
            logger.warning(
                f"{name} is DOWN. Return code: {status}"
            )

            results.append({
                "name": name,
                "ip": ip,
                "status": "DOWN",
                "packet_loss": packet_loss,
                "average_latency": average_latency,
                "health": None
            })

    # Display report
    print("\n" + "=" * 70)
    print("NOC NETWORK REPORT")
    print("=" * 70)

    for result in results:

        print(
            f"{result['name']:<15}"
            f"{result['ip']:<16}"
            f"{result['status']:<15}"
            f"{str(result['packet_loss']):<12}"
            f"{str(result['average_latency']):<12}"
            f"{str(result['health']):<10}"
        )

    # Save CSV report
    try:

        with open("network_report.csv", "w", newline="") as file:

            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "name",
                    "ip",
                    "status",
                    "packet_loss",
                    "average_latency",
                    "health"
                ]
            )

            writer.writeheader()
            writer.writerows(results)

        logger.info("Network report saved successfully.")
        print("\nReport saved to network_report.csv")

    except OSError as error:

        logger.error(f"Could not save network report: {error}")
        print(f"\nERROR: Could not save network report: {error}")

    logger.info("Network diagnostic program completed.")
    print("=" * 70)

    return 0


# Run the program only when this file is executed directly
if __name__ == "__main__":
    sys.exit(main())