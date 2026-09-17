# Network Diagnostic Tool

## My first Python networking project

This is the first project of my Python portfolio.

I built this project because I wanted to stop learning Python only through small exercises and start using it to solve problems related to the field I am actually preparing for: **networking, NOC operations, infrastructure and eventually cloud engineering**.

I am currently studying Information Systems Engineering and Networking/Cisco technologies, so I decided to combine both areas and build a tool that can perform basic network diagnostics automatically.

The original version of this project was much simpler. I started with a Python script containing a list of devices and used the Windows `ping` command to check whether they were reachable. As I continued developing it, I realised that I wanted the project to behave more like a real automation tool rather than just a script that happened to work.

That led me to gradually add external configuration, validation, error handling, logging, structured reports and automated testing.

This project is the result of that process.

---

## What the project does

The tool reads a list of network devices from a JSON configuration file and performs basic connectivity diagnostics.

For each device, the program:

1. Loads the device configuration.
2. Validates the configuration.
3. Verifies that the IP address is valid.
4. Executes an ICMP ping test.
5. Measures packet loss.
6. Measures average latency.
7. Determines a basic network health status.
8. Displays the results in the terminal.
9. Saves the results to a CSV report.
10. Records important events in a diagnostic log.

The main idea is to automate repetitive checks that could be useful in a basic NOC environment.

---

## Why I built it

I wanted this project to be more than just a Python exercise.

My goal is to move from networking into network automation and eventually cloud engineering, so I wanted to practise Python in a context that is actually connected to that career path.

While building this project, I started thinking less about:

> "How do I make this code run?"

and more about:

> "How do I make this code reliable, reusable and easier to troubleshoot?"

That change in mindset became one of the most valuable lessons of the project.

---

## Project architecture

The application follows this general workflow:

```text
devices.json
     |
     v
load_devices()
     |
     v
validate_devices()
     |
     v
ping_host()
     |
     v
parse_ping_output()
     |
     v
assess_health()
     |
     +-------------------+
     |                   |
     v                   v
Terminal Output      CSV Report
                         |
                         v
                  network_report.csv

Diagnostic events
        |
        v
network_diagnostic.log
```

I separated the responsibilities of the program into different functions so that each part has a clear purpose.

For example:

- `load_devices()` handles configuration loading.
- `validate_devices()` checks whether the configuration is usable.
- `ping_host()` executes the network diagnostic.
- `parse_ping_output()` extracts useful information from the command output.
- `assess_health()` evaluates the device condition.
- `main()` coordinates the entire workflow.

This structure also made it possible to test individual parts of the program instead of only testing the complete application.

---

## Project structure

```text
python-portfolio/
│
├── main.py
├── devices.json
├── README.md
├── .gitignore
│
└── tests/
    ├── __init__.py
    └── test_main.py
```

The application also generates these files locally:

```text
network_report.csv
network_diagnostic.log
```

Python may also generate:

```text
__pycache__/
```

These generated files are ignored by Git and are not part of the source code published to the repository.

---

## Device configuration

One of the biggest changes I made during the development of this project was moving the device information out of the Python code.

The first version had the devices hard-coded directly in `main.py`.

I changed that so the configuration is stored in `devices.json`.

Example:

```json
[
    {
        "name": "Localhost",
        "ip": "127.0.0.1"
    },
    {
        "name": "Google DNS",
        "ip": "8.8.8.8"
    },
    {
        "name": "Test Device",
        "ip": "192.0.2.1"
    }
]
```

This made the program easier to modify and more portable.

Now, I can change the devices I want to test without changing the Python logic itself.

This also helped me understand an important concept in automation:

**configuration and application logic should not unnecessarily be mixed together.**

---

## Validation and error handling

I did not want the program to assume that the configuration file would always be perfect.

The tool checks several possible problems before starting the diagnostics.

It can detect situations such as:

- `devices.json` does not exist.
- The JSON syntax is invalid.
- The device list is empty.
- A device is not represented as a dictionary.
- A device is missing the `name` field.
- A device is missing the `ip` field.
- A device name is empty.
- An IP address is invalid.

For example, this is valid JSON:

```json
[
    {
        "name": "Router",
        "ip": "hello"
    }
]
```

but it is not valid device configuration for this project.

The application therefore validates both the **JSON format** and the **meaning of the data** before continuing.

This was an important lesson for me:

> Valid JSON does not necessarily mean valid application data.

---

## Network diagnostics

The program uses the Windows `ping` command through Python's `subprocess` module.

The current implementation explicitly sends four ICMP echo requests and uses a one-second timeout for each request.

The program attempts to identify:

- Reachable devices
- Unreachable devices
- Timeouts
- Host resolution failures
- Packet loss
- Average latency
- Ping output parsing errors

The output is then processed and converted into structured information that the rest of the program can use.

---

## Ping output parsing

One of the improvements I made during the development of this project was replacing fragile output parsing based on fixed list positions.

Instead of assuming that a value would always appear in one exact position after using `split()`, I introduced regular expressions to search for the information I actually need.

For example, the program searches the Windows ping output for:

```text
Lost = 1 (25% loss)
```

and:

```text
Average = 20ms
```

This made the parser easier to understand and less dependent on exact spacing.

I also separated the parsing logic into its own function:

```python
parse_ping_output()
```

This means the function responsible for running `ping` does not also have to contain all the parsing logic.

---

## Health assessment

After collecting the network information, the program evaluates the condition of the device.

The current rules are:

### Healthy

```text
Packet loss = 0%
Average latency < 100 ms
```

### Warning

```text
Packet loss < 50%
Average latency < 200 ms
```

### Critical

Anything that does not satisfy the previous conditions is classified as critical.

These thresholds are intentionally simple because this project is meant to demonstrate Python automation and networking fundamentals rather than act as a complete enterprise monitoring platform.

---

## Logging

I also added application logging so the program does not depend only on terminal output.

The tool generates:

```text
network_diagnostic.log
```

The log records important events such as:

- Configuration loading
- Configuration validation
- Device checks
- Successful diagnostics
- Timeouts
- Failed diagnostics
- Parsing errors
- Report generation
- Program termination

Example:

```text
2026-09-11 15:50:12,423 | INFO | Device configuration loaded successfully.
2026-09-11 15:50:12,424 | INFO | Checking device: Google DNS (8.8.8.8)
2026-09-11 15:50:13,521 | INFO | Google DNS is UP. Packet loss: 0%, Average latency: 45 ms, Health: Healthy
```

This taught me an important difference between:

```text
print()
```

and:

```text
logging
```

`print()` is useful for showing the person running the program what is happening right now.

Logging gives me a historical record that I can inspect later when troubleshooting.

That concept will become even more important in the later projects of this portfolio.

---

## CSV reporting

After the diagnostic process finishes, the program saves the results into:

```text
network_report.csv
```

The report contains fields such as:

```text
name
ip
status
packet_loss
average_latency
health
```

This gives me structured output that can be opened later in spreadsheet software or processed by another Python program.

---

## Testing

Once the main functionality was working, I did not want to rely only on manually running the program.

I introduced automated testing using Python's built-in `unittest` framework.

The tests currently cover areas such as:

- Valid device configurations
- Empty configurations
- Missing IP addresses
- Invalid IP addresses
- Ping output parsing
- Packet loss parsing
- Healthy devices
- Warning devices
- Critical devices

The test suite currently contains **9 tests**.

I can run them with:

```bash
python -m unittest discover -s tests
```

and the expected result is:

```text
Ran 9 tests

OK
```

One thing I learned here is that testing also affects the way a program should be structured.

I introduced:

```python
def main():
```

as the main workflow of the application and:

```python
if __name__ == "__main__":
    sys.exit(main())
```

to make sure the program only executes automatically when the file is run directly.

That allows other Python files, such as my test suite, to import the functions without automatically starting the complete diagnostic tool.

---

## Why `main()` matters in this project

The `main()` function acts as the coordinator of the application.

Instead of putting the entire workflow directly at the top level of the file, the program now follows a clearer sequence:

```text
Load configuration
        ↓
Validate configuration
        ↓
Run diagnostics
        ↓
Process results
        ↓
Display results
        ↓
Generate report
        ↓
Finish
```

The individual functions handle specific responsibilities, while `main()` coordinates the order in which everything happens.

This was one of the biggest improvements in the project because it made the code easier to understand and test.

---

## Technologies and Python modules

This project uses Python's standard library, so no external Python packages are required.

Main technologies and modules:

- Python
- JSON
- CSV
- Regular Expressions
- ICMP Ping
- `subprocess`
- `logging`
- `ipaddress`
- `unittest`
- Git
- GitHub
- Visual Studio Code

---

## What I learned

This project started as a simple Python script, but it ended up teaching me much more than I originally expected.

The main things I practised were:

- Python functions
- Lists and dictionaries
- Loops
- File handling
- JSON
- CSV files
- Exception handling
- Input validation
- IP address validation
- Working with operating system commands
- `subprocess`
- Regular expressions
- Logging
- Unit testing
- Git and GitHub
- Separation of responsibilities
- Basic application structure

More importantly, I started learning how to think about reliability.

For example, instead of only asking:

> "Does this work?"

I started asking:

> "What happens if the file is missing?"

> "What happens if the data is malformed?"

> "What happens if the device cannot be reached?"

> "What happens if the command output is different from what I expected?"

> "How can I verify that a future change doesn't break something that already works?"

That mindset is one of the main reasons I built this project.

---

## A problem that helped me understand portability

During development, I also tested the repository on another computer.

That exposed an issue with the way I had originally configured the devices.

For example:

```text
127.0.0.1
```

does not represent one permanently fixed computer.

It always refers to:

> The machine running the program.

That experience made the importance of external configuration much clearer to me.

Moving the device information into `devices.json` solved that architectural problem and made the project easier to reuse on different machines.

---

## Current limitations

This project is intentionally limited in scope.

The current version is designed for Windows because it uses the Windows `ping` command and parses Windows-style ping output.

It is therefore not yet a fully cross-platform network diagnostic tool.

It currently focuses primarily on basic ICMP connectivity, packet loss and latency.

It is also not intended to replace professional network monitoring platforms.

The purpose of the project is to demonstrate my progression in Python, networking and automation.

---

## Future improvements

There are several improvements I would like to explore as my Python skills develop:

- Cross-platform ping support
- Hostname support
- DNS diagnostics
- TCP port checks
- More detailed network statistics
- User-configurable ping count and timeouts
- More advanced reporting
- A more modular project structure
- Additional automated tests
- Integration with network monitoring systems

Some of these ideas will not be added to this project because I want the portfolio to progress through separate projects instead of turning Project 1 into an unnecessarily large application.

---

## Portfolio Roadmap

This project is the first step in a larger Python portfolio focused on networking, automation and cloud engineering.

My planned progression is:

```text
Project 1
Network Diagnostic Tool
        ↓
Project 2
Log Analyzer
        ↓
Project 3
SSH Network Automation
        ↓
Project 4
Network Monitoring Tool
        ↓
Project 5
REST API / Automation
        ↓
Project 6
Azure Cloud Automation
```

The goal is for the projects to become progressively more advanced rather than being six unrelated Python exercises.

I want each project to build on concepts from the previous one and gradually take me from basic Python automation toward real infrastructure and cloud automation.

---

## Project status

**Status:** Completed

**Project:** Network Diagnostic Tool

**Focus:** Python + Networking + NOC Automation

This is Project 1 of my Python portfolio.

---

## Author

**Durman Sequeira Quiros**

Information Systems Engineering Student  
Networking and Cisco Technologies Student

GitHub:

https://github.com/durmansequeira/python-portfolio