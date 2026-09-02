# Network Diagnostic Tool

A Python-based network diagnostic tool that I built as my first Python project while developing my skills in networking, automation, and NOC operations.

The main idea behind this project is simple: instead of manually checking devices one by one, I wanted to build a small tool that could automatically test multiple hosts and provide useful information about their connectivity.

---

## What This Project Does

The tool checks a list of devices and performs a ping test against each one.

For every target, it can:

- Check whether the host is reachable
- Detect timeouts
- Detect hostname resolution failures
- Measure packet loss
- Measure average latency
- Assess basic network health
- Generate a NOC-style console report
- Export diagnostic results to a CSV file

### Example Output

    ================================================================================
    NOC NETWORK REPORT
    ================================================================================
    DEVICE    IP                STATUS            LOSS        LATENCY     HEALTH
    --------------------------------------------------------------------------------
    R1        127.0.0.1         UP                0%          0 ms        Healthy
    R2        8.8.8.8           UP                0%          54 ms       Healthy
    SW1       192.0.2.1         TIMEOUT           --          --          --
    ================================================================================

---

## Technologies Used

- Python 3.13
- `subprocess`
- `csv`
- Visual Studio Code
- Git
- GitHub

The project currently uses only Python's standard library, so no external Python packages are required.

---

## How It Works

### 1. Device Inventory

The devices to be checked are stored in a list of dictionaries.

    devices = [
        {
            "name": "R1",
            "ip": "127.0.0.1"
        }
    ]

This makes it possible to add more devices without rewriting the diagnostic logic.

### 2. Network Diagnostic

The `ping_host()` function uses Python's `subprocess` module to execute the Windows `ping` command.

The command output is captured by Python and analysed to obtain information such as:

- Packet loss
- Average latency
- Return codes
- Timeout conditions
- Hostname resolution failures

### 3. Health Assessment

The `assess_health()` function evaluates packet loss and latency and assigns a basic health status:

- Healthy
- Warning
- Critical

The current thresholds are simple learning-oriented thresholds and can be improved in future versions.

### 4. Results Collection

After each device is checked, the result is stored in a list of dictionaries.

This allows the program to generate a summary report after all devices have been processed.

### 5. CSV Export

The diagnostic results are automatically exported to:

    network_report.csv

This file contains the results of the current execution and is excluded from Git tracking because it is generated runtime data rather than source code.

---

## How to Run

Clone the repository:

    git clone <repository-url>

Move into the project directory:

    cd python-portfolio

Run the application:

    python main.py

The devices that will be checked can be modified directly in the `devices` list inside `main.py`.

---

## What I Learned

This project helped me move from knowing basic Python syntax to actually using Python to solve an infrastructure-related problem.

During the development of this project, I practised:

- Variables and data types
- Lists
- Dictionaries
- `for` loops
- `if`, `elif`, and `else`
- Functions
- Parameters and return values
- `try` / `except`
- Working with `None`
- String manipulation
- `.split()`
- `.splitlines()`
- `.replace()`
- `.strip()`
- `subprocess`
- Capturing command output
- Working with return codes
- CSV files
- Basic Git workflow
- Basic GitHub workflow

---

## A Little About Why I Built This

I'm currently working towards a career in networking and cloud engineering, and I wanted to learn Python in a way that was connected to the kind of work I actually want to do.

I already had some programming experience from studying C#, but I wanted to take that knowledge and apply it to networking and infrastructure instead of only doing traditional programming exercises.

This project is my first step in that direction.

I know this is not a production-grade monitoring platform, and that's not what I was trying to build here. The goal was to understand how Python can interact with the operating system, process command output, analyse network information, and automate repetitive tasks.

Building the project step by step also taught me something that I think is just as important as the code itself: debugging.

Several parts of the project did not work the first time. I had to inspect command output, find mistakes in my assumptions, fix dictionary keys, deal with indentation problems, and figure out how Windows was actually returning information from the `ping` command.

That process was probably one of the most useful parts of the project for me, because it made me realise that programming is not just about writing code that works on the first try. It is also about understanding what went wrong, investigating it, and improving the solution.

---

## Future Improvements

There are several things I would like to improve as my Python skills grow:

- Improve the ping result parser
- Make health thresholds configurable
- Improve error handling
- Add logging
- Add DNS diagnostics
- Add TCP port checks
- Improve the console interface
- Organise the application into multiple Python modules
- Add automated tests
- Add support for Linux
- Add more detailed network diagnostics
- Eventually integrate the project with network devices through SSH
- Connect similar automation concepts to cloud environments

---

## Python Portfolio Roadmap

This project is part of a larger Python portfolio focused on networking, NOC operations, automation, and cloud engineering.

### Project 1 — Network Diagnostic Tool

Ping multiple hosts, analyse connectivity, packet loss and latency, and generate diagnostic reports.

### Project 2 — Log Analyzer

Analyse network and system logs to detect errors, warnings, failed logins, timeouts, and other relevant events.

### Project 3 — SSH Network Automation

Use Python and SSH to connect to network devices, execute commands, collect information, and automate repetitive network administration tasks.

### Project 4 — Network Monitoring Tool

Create a more advanced monitoring system capable of continuously checking multiple devices, recording results, and providing alerts.

### Project 5 — REST API / Automation Project

Work with APIs, JSON, authentication, requests, and external services to automate infrastructure-related tasks.

### Project 6 — Azure Cloud Automation

Use Python with Azure APIs and SDKs to inspect, manage, and automate cloud resources.

---

## Long-Term Goal

The long-term goal is to use Python not just as a programming language, but as a practical tool for:

- Network engineering
- NOC operations
- Infrastructure automation
- Network monitoring
- Cloud engineering
- Cloud automation

This portfolio is part of my process of combining programming, networking, and cloud technologies into practical projects that I can continue improving over time.

---

## Author

**Durman Sequeira**

Built while learning Python and developing practical skills for a career in networking and cloud engineering.