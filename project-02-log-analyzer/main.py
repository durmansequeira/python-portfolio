from pathlib import Path
import csv
import re


# Parse one log line into structured data
def parse_log_line(line):

    parts = line.strip().split(" | ", 2)

    if len(parts) != 3:
        return None

    timestamp, level, message = parts

    return {
        "timestamp": timestamp,
        "level": level,
        "message": message
    }


# Load and parse the log file
def load_log_file(file_path):

    entries = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:

            for line in file:
                entry = parse_log_line(line)

                if entry is not None:
                    entries.append(entry)

        return entries

    except FileNotFoundError:
        print(f"ERROR: Log file not found: {file_path}")
        return None

    except OSError as error:
        print(f"ERROR: Could not read log file: {error}")
        return None


# Analyse log severity levels
def analyse_log_levels(entries):

    levels = {
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0,
        "CRITICAL": 0,
        "UNKNOWN": 0
    }

    for entry in entries:

        level = entry["level"].strip().upper()

        if level in levels:
            levels[level] += 1

        else:
            levels["UNKNOWN"] += 1

    return levels


# Analyse device UP/DOWN events
def analyse_device_events(entries):

    device_events = []

    for entry in entries:

        message = entry["message"]

        # Example:
        # "Test Device is DOWN. Return code: 1"

        match = re.search(
            r"(.+?)\s+is\s+(UP|DOWN)",
            message,
            re.IGNORECASE
        )

        if match:

            device_name = match.group(1).strip()
            event = match.group(2).upper()

            device_events.append({
                "timestamp": entry["timestamp"],
                "level": entry["level"],
                "device": device_name,
                "event": event,
                "message": message
            })

    return device_events


# Analyse ping diagnostic results
def analyse_ping_results(entries):

    ping_results = []

    current_device = None
    current_ip = None

    # Pattern used to find the device being checked
    checking_pattern = re.compile(
        r"Checking device:\s+(.+?)\s+\(([\d.]+)\)",
        re.IGNORECASE
    )

    # Pattern used to find the final ping result
    ping_pattern = re.compile(
        r"Ping test completed for "
        r"(?P<ip>[\d.]+)\.\s+"
        r"Packet loss:\s+(?P<packet_loss>\d+)%\s*,\s+"
        r"Average latency:\s+(?P<latency>\d+|None)\s+ms,\s+"
        r"Return code:\s+(?P<return_code>-?\d+)",
        re.IGNORECASE
    )

    for entry in entries:

        message = entry["message"]

        # Check whether this line identifies a device
        checking_match = checking_pattern.search(message)

        if checking_match:

            current_device = checking_match.group(1).strip()
            current_ip = checking_match.group(2)

            continue

        # Check whether this line contains ping results
        ping_match = ping_pattern.search(message)

        if ping_match:

            ip = ping_match.group("ip")

            packet_loss = int(
                ping_match.group("packet_loss")
            )

            latency_value = ping_match.group("latency")

            if latency_value.lower() == "none":
                average_latency = None
            else:
                average_latency = int(latency_value)

            return_code = int(
                ping_match.group("return_code")
            )

            ping_results.append({
                "timestamp": entry["timestamp"],
                "device": current_device or "Unknown",
                "ip": ip or current_ip,
                "packet_loss": packet_loss,
                "average_latency": average_latency,
                "return_code": return_code
            })

    return ping_results


# Assess the health of a device
def assess_health(packet_loss, average_latency, return_code):

    if return_code == 0 and packet_loss == 0:

        if average_latency is not None and average_latency < 100:
            return "Healthy"

    if packet_loss < 50:
        return "Warning"

    return "Critical"


# Build a consolidated device health summary
def build_health_summary(device_events, ping_results):

    health_summary = []

    # Create a lookup table for device events.
    # Milliseconds are removed because the event and ping
    # timestamps can differ by a few milliseconds.
    event_lookup = {}

    for event in device_events:

        timestamp_without_milliseconds = (
            event["timestamp"].split(",")[0]
        )

        key = (
            timestamp_without_milliseconds,
            event["device"]
        )

        event_lookup[key] = event

    # Combine device events with ping results
    for result in ping_results:

        timestamp_without_milliseconds = (
            result["timestamp"].split(",")[0]
        )

        key = (
            timestamp_without_milliseconds,
            result["device"]
        )

        event = event_lookup.get(key)

        if event is not None:
            status = event["event"]
        else:
            status = "UNKNOWN"

        health = assess_health(
            result["packet_loss"],
            result["average_latency"],
            result["return_code"]
        )

        health_summary.append({
            "timestamp": result["timestamp"],
            "device": result["device"],
            "ip": result["ip"],
            "status": status,
            "packet_loss": result["packet_loss"],
            "average_latency": result["average_latency"],
            "return_code": result["return_code"],
            "health": health
        })

    return health_summary

#Export health summary to CSV
def export_health_summary_to_csv(health_summary, output_file):

    fieldnames = [
        "timestamp",
        "device",
        "ip",
        "status",
        "packet_loss",
        "average_latency",
        "return_code",
        "health"
    ]
    # Normalize the destination into a path object.
    output_path = Path(output_file)

    try:

        with output_path.open(
            "w",
            newline="",
            encoding="utf-8"
            ) as file:

                writer = csv.DictWriter(
                    file,
                    fieldnames=fieldnames
                    )

                writer.writeheader()
                writer.writerows(health_summary)

        # Only report success after writing has completed.

        return True

    except OSError as error:
        print(f"ERROR: Could not write report: {error}")
        return False


# Main program
def main():

    project_directory = Path(__file__).parent

    log_file = (
        project_directory
        / "data"
        / "network_diagnostic_sample.log"
    )

    report_file = (
        project_directory / "network_health_report.csv"
    )

    entries = load_log_file(log_file)

    if entries is None:
        return 1

    severity_counts = analyse_log_levels(entries)

    device_events = analyse_device_events(entries)

    ping_results = analyse_ping_results(entries)

    health_summary = build_health_summary(
        device_events,
        ping_results
    )

    report_created = export_health_summary_to_csv(
        health_summary,
        report_file
    )

    print("=" * 70)
    print("LOG ANALYZER")
    print("=" * 70)

    print(f"\nTotal parsed entries: {len(entries)}")

    print("\nSeverity summary")
    print("-" * 70)

    print(f"INFO:      {severity_counts['INFO']}")
    print(f"WARNING:   {severity_counts['WARNING']}")
    print(f"ERROR:     {severity_counts['ERROR']}")
    print(f"CRITICAL:  {severity_counts['CRITICAL']}")
    print(f"UNKNOWN:   {severity_counts['UNKNOWN']}")

    print("\nDevice events")
    print("-" * 70)

    for event in device_events:

        print(
            f"{event['timestamp']} | "
            f"{event['level']} | "
            f"{event['device']} | "
            f"{event['event']}"
        )

    print("\nPing diagnostics")
    print("-" * 70)

    for result in ping_results:

        print(
            f"{result['device']:<15}"
            f"{result['ip']:<16}"
            f"Loss: {result['packet_loss']}% | "
            f"Latency: {result['average_latency']} ms | "
            f"Return code: {result['return_code']}"
        )

    print("\nDevice health summary")
    print("-" * 70)

    for device in health_summary:

        print(
            f"{device['device']:<15}"
            f"{device['ip']:<16}"
            f"Status: {device['status']:<7}"
            f"Loss: {device['packet_loss']}% | "
            f"Latency: {device['average_latency']} ms | "
            f"Health: {device['health']}"
        )

    if report_created:
     print(f"\nReport created: {report_file}")
    else:
      print("\nReport creation failed.")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())