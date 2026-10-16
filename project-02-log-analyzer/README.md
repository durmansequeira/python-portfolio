# Project 02 — Python Log Analyzer

**Turning network logs into useful information with Python.**

## Why I built this project

After finishing my first Python project, a Network Diagnostic Tool, I wanted to take things a step further.

In Project 01, I built a tool that checks network devices, measures packet loss and latency, and records the results in a log file. That was useful, but I wanted to do more with the information it produced.

I started asking myself a question: *What if I could make Python read those logs, understand what happened, identify devices that are having problems, and put the results into a report?*

That was the idea behind this project.

I'm studying Information Systems Engineering and working towards a career in networking, infrastructure, automation, and cloud computing. I want to become comfortable using Python to solve practical problems, so I decided to build this project step by step rather than just write a script and move on.

## What I built

I developed a Python program that reads a sample log file from my first project, analyses its contents, and produces a summary of the network devices' health.

The sample contains **44 log entries** from two diagnostic runs involving three devices:

- **Localhost** — `127.0.0.1`
- **Google DNS** — `8.8.8.8`
- **Test Device** — `192.0.2.1`

The program processes the logs and presents the information in the terminal. It also exports the final device health results to a CSV file, which I can open in a spreadsheet application or inspect directly from PowerShell.

## How I approached the project

I split the program into smaller functions, with each one responsible for a particular task. This made it easier to understand what was happening and to troubleshoot problems as I added new features.

### 1. Reading and parsing log files

I started by writing a function to read the log file line by line.

Each valid entry follows this general format:

`TIMESTAMP | LEVEL | MESSAGE`

The parser separates these three parts and stores them in a Python dictionary. This gives me structured data that I can work with instead of repeatedly searching through raw text.

I also added basic error handling for missing files and other file-reading problems.

### 2. Analysing severity levels

Next, I added a function to count the severity levels recorded in the logs:

- `INFO`
- `WARNING`
- `ERROR`
- `CRITICAL`
- `UNKNOWN`

For the current sample, the program finds 39 INFO entries, 2 WARNING entries, 3 ERROR entries, and no CRITICAL or UNKNOWN entries.

This gives me a quick overview of the messages contained in the file.

### 3. Identifying device events

I then wanted to extract device availability events, such as a device being UP or DOWN.

I used Python's `re` module and regular expressions to search the log messages for these states.

For example, a message containing `Test Device is DOWN` becomes a structured record with the device name and its status. This lets me display device events separately from the rest of the log.

### 4. Extracting ping diagnostics

The next step was to extract the actual network diagnostic results.

I used regular expressions to identify the IP address, packet loss, average latency, and ping return code recorded in each result.

One issue I encountered was that a failed ping could contain `Average latency: None ms` rather than a number. My initial expression only accepted digits, so it skipped those entries.

I updated the parser to accept either a numeric latency or `None`. I also converted numeric values into integers so they could be used in later calculations.

This was a useful reminder to test against the data I actually have, rather than assume every log entry will follow the same pattern.

### 5. Building a device health summary

Once I had the device events and ping results, I combined them into a single health summary.

The program uses the device name and timestamp to associate the corresponding records. I discovered that two related events could have timestamps differing by a few milliseconds, so I adjusted the matching logic to ignore the milliseconds when comparing them.

I also added a health assessment function with three possible results:

- **Healthy** — the ping succeeded, packet loss is zero, and the measured latency is below 100 ms.
- **Warning** — the device does not meet the Healthy criteria, but packet loss is below 50%.
- **Critical** — packet loss is 50% or higher.

These are the rules I chose for this learning project, rather than universal network monitoring standards.

For failed pings, the program preserves `None` as the missing latency value instead of treating it as a real measurement of zero milliseconds.

### 6. Exporting the results to CSV

Once the health summary was working, I added a function to export it to `network_health_report.csv`.

The report includes the timestamp, device name, IP address, availability status, packet loss, latency, return code, and health classification.

This means the results are no longer limited to terminal output. I can inspect the report in a spreadsheet application or use PowerShell to display selected columns.

The CSV file is generated by the program and is excluded from Git because it can be recreated whenever the analysis runs.

### 7. Testing the program

I didn't want to rely only on running `main.py` and checking whether the output looked correct, so I created a test suite using Python's built-in `unittest` framework.

The tests cover:

- Parsing valid and malformed log entries.
- Reading existing and missing files.
- Counting severity levels.
- Identifying UP and DOWN events.
- Extracting successful and failed ping results.
- Assessing device health.
- Combining device events with ping diagnostics.
- Creating a CSV report and checking its headers and contents.

While working on the tests, I encountered a few bugs involving indentation, function calls, and test discovery. Fixing them helped me understand how Python executes code and how automated tests can catch mistakes that aren't always obvious from the terminal output.

**Current testing result: 12 tests passing.**

To run the tests yourself, use the command below from the project directory.

## Project structure

```text
project-02-log-analyzer/
├── README.md
├── main.py
├── data/
│   └── network_diagnostic_sample.log
└── tests/
    ├── __init__.py
    └── test_main.py
```

The file `network_health_report.csv` is generated when the program runs and is excluded from version control.

## Tools and concepts I used

- **Python 3** for the application logic.
- **`pathlib`** for working with file paths.
- **`re`** for extracting information from log messages.
- **`csv`** for exporting structured results.
- **`unittest`** for automated testing.
- **PowerShell** for running the program, executing tests, and inspecting the generated report.
- **Git and GitHub** for version control and portfolio development.

The project uses Python's standard library and does not require third-party packages.

## How to run it

First, open a terminal in the `project-02-log-analyzer` directory.

Run the program:

```powershell
python main.py
```

The program reads `data/network_diagnostic_sample.log`, displays the analysis, builds the device health summary, and generates `network_health_report.csv`.

To run the automated tests:

```powershell
python -m unittest tests.test_main -v
```

To inspect the generated CSV report in PowerShell:

```powershell
Import-Csv .\network_health_report.csv |
    Format-Table device, ip, status, packet_loss, average_latency, health -AutoSize
```

## What I have learned

This project has helped me understand how to break a larger task into smaller functions and connect them into a complete program.

I've practised processing text files, using regular expressions, working with dictionaries and lists, handling missing values, combining related records, exporting CSV files, and writing automated tests.

I've also learned that getting a program to run once is only part of the job. I need to check what happens when the input is malformed, a file is missing, a value is unavailable, or two records don't match exactly as expected.

Most importantly, I'm beginning to understand how Python can be used to take information that would otherwise require manual inspection and turn it into something easier to analyse.

## What's next?

I'm continuing to build my portfolio around Python, networking, and infrastructure automation.

My next goals are to improve the structure and reliability of the tools I've built, expand my testing experience, and move towards automating network administration tasks.

From there, I plan to explore network monitoring, REST API integration, and eventually cloud automation with Azure.

Each project builds on what I've learned from the previous one. My aim is to develop practical skills that I can demonstrate through working code, clear documentation, and projects that solve real technical problems.