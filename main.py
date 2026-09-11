import subprocess
import csv
import json
import sys
import ipaddress


# Load device configuration from JSON
def load_devices():
    try:
        with open("devices.json", "r") as file:
            devices = json.load(file)

        return devices

    except FileNotFoundError:
        print("ERROR: devices.json was not found.")
        return None

    except json.JSONDecodeError:
        print("ERROR: devices.json contains invalid JSON.")
        return None

    except OSError as error:
        print(f"ERROR: Could not read devices.json: {error}")
        return None


# Validate device configuration
def validate_devices(devices):

    if not isinstance(devices, list):
        print("ERROR: Device configuration must be a list.")
        return False

    if not devices:
        print("ERROR: Device configuration is empty.")
        return False

    for device in devices:

        if not isinstance(device, dict):
            print("ERROR: Each device must be a dictionary.")
            return False

        if "name" not in device:
            print("ERROR: A device is missing the 'name' field.")
            return False

        if "ip" not in device:
            print("ERROR: A device is missing the 'ip' field.")
            return False

        if not isinstance(device["name"], str) or not device["name"].strip():
            print("ERROR: Device name must be a non-empty string.")
            return False

        if not isinstance(device["ip"], str):
            print(f"ERROR: IP address for {device['name']} must be a string.")
            return False

        try:
            ipaddress.ip_address(device["ip"])

        except ValueError:
            print(
                f"ERROR: Invalid IP address for "
                f"{device['name']}: {device['ip']}"
            )
            return False

    return True


# Definition of the ping_host function
def ping_host(target):

    try:
        result = subprocess.run(
            ["ping", target],
            capture_output=True,
            text=True,
            timeout=10
        )

        # Check whether hostname could be resolved or not
        if "could not find host" in result.stdout.lower():
            return "Host_not_found", None, None

        packet_loss = None
        average_latency = None

        for line in result.stdout.splitlines():

            if "Lost =" in line:
                parts = line.split()
                packet_loss = int(parts[10].strip("(%"))

            if "Average =" in line:
                parts = line.split()
                average_latency = int(
                    parts[-1].replace("ms", "")
                )

        return result.returncode, packet_loss, average_latency

    except subprocess.TimeoutExpired:
        return "TIMEOUT", None, None


# Assess network health
def assess_health(packet_loss, average_latency):

    if packet_loss == 0 and average_latency < 100:
        return "Healthy"

    elif packet_loss < 50 and average_latency < 200:
        return "Warning"

    else:
        return "Critical"


# Load devices from configuration file
devices = load_devices()


# Stop the program if the configuration could not be loaded
if devices is None:
    print(
        "Program stopped because the device configuration "
        "could not be loaded."
    )
    sys.exit(1)


# Validate the device configuration
if not validate_devices(devices):
    print(
        "Program stopped because the device configuration "
        "is invalid."
    )
    sys.exit(1)


# Store diagnostic results
results = []


# Check every device
for device in devices:

    print(f"\nChecking {device['name']} ({device['ip']})")

    status, packet_loss, average_latency = ping_host(device["ip"])

    if status == "Host_not_found":

        print(f"{device['name']} could not be resolved.")

        results.append({
            "name": device["name"],
            "ip": device["ip"],
            "status": "Host_not_found",
            "packet_loss": None,
            "average_latency": None,
            "health": None
        })

    elif status == "TIMEOUT":

        print("Request timed out.")

        results.append({
            "name": device["name"],
            "ip": device["ip"],
            "status": "TIMEOUT",
            "packet_loss": None,
            "average_latency": None,
            "health": None
        })

    elif status == 0:

        health = assess_health(
            packet_loss,
            average_latency
        )

        print(f"{device['name']} is UP")
        print(f"Packet loss: {packet_loss}%")
        print(f"Average latency: {average_latency} ms")
        print(f"Health status: {health}")

        results.append({
            "name": device["name"],
            "ip": device["ip"],
            "status": "UP",
            "packet_loss": packet_loss,
            "average_latency": average_latency,
            "health": health
        })

    else:

        print(f"{device['name']} is DOWN")

        results.append({
            "name": device["name"],
            "ip": device["ip"],
            "status": "DOWN",
            "packet_loss": None,
            "average_latency": None,
            "health": None
        })


# Display stored results
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


# Save results to CSV
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


print("\nReport saved to network_report.csv")
print("=" * 70)