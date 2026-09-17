# Python Portfolio

## My Journey into Python, Network Automation and Cloud

This repository is part of my journey into IT.

I am currently studying Information Systems Engineering and developing my networking skills through Cisco and CCNA-related studies. My long-term goal is to move into **networking, NOC operations, infrastructure automation and eventually cloud engineering**.

Because of that, I decided that learning Python should not be separate from the rest of my technical development.

I don't want to learn Python just by completing random exercises and small coding challenges.

I want to use Python to solve problems that are connected to the kind of work I want to do.

That's the purpose of this repository.

---

# Why am I building this portfolio?

When I started learning Python, I realised quite quickly that understanding syntax is only one part of becoming a developer or an automation engineer.

I can learn:

- variables
- loops
- functions
- lists
- dictionaries
- classes
- libraries

but that does not necessarily mean I know how to use Python to solve a real problem.

So I decided to learn through projects.

My idea is simple:

> **Learn Python by building things that are relevant to networking, infrastructure and cloud.**

Instead of creating six unrelated beginner projects, I want these projects to form a progression.

The first projects will focus on Python and networking fundamentals.

Then I want to move into network automation, monitoring and APIs.

Finally, I want to apply the same concepts to cloud infrastructure and Azure.

This repository is therefore not just a collection of Python scripts.

It is a record of my progression from **Python beginner to infrastructure and cloud automation.**

---

# What am I trying to achieve?

My main objective is to become comfortable enough with Python that I can use it as a practical tool in my future IT career.

I want to be able to look at a repetitive technical task and think:

> "I could probably automate this."

That could mean:

- checking network devices,
- analysing logs,
- collecting information,
- connecting to network equipment,
- monitoring infrastructure,
- consuming APIs,
- or interacting with cloud resources.

I also want to develop something equally important:

**the ability to build reliable automation.**

That means learning to:

- handle errors,
- validate data,
- organise code,
- test my work,
- document what I build,
- use Git properly,
- and understand why something works instead of simply copying code that works.

---

# My learning philosophy

I am intentionally building these projects step by step.

I don't want to receive a finished application and simply paste it into VS Code.

I want to understand what I am building.

During the development of each project, I am trying to learn:

```text
Understand the problem
        ↓
Design a solution
        ↓
Write the code
        ↓
Test it
        ↓
Break it
        ↓
Fix it
        ↓
Document it
        ↓
Improve it
```

I believe that making mistakes is part of the process.

Some of the most useful things I have already learned came from situations where something did not work on the first try.

For example, working with file paths, JSON configuration, Git, testing and subprocesses has taught me things that I probably would not have understood as well through theory alone.

So this portfolio is also a record of those lessons.

---

# The Six-Project Roadmap

I am following a six-project roadmap that gradually increases in complexity.

Each project is designed to introduce new Python concepts while staying connected to networking, infrastructure and cloud.

---

## Project 1 — Network Diagnostic Tool

**Status: Completed**

This is where I started.

The goal was to build a Python tool capable of checking multiple devices and collecting basic network information.

The project evolved from a simple ping script into a more complete application with:

- JSON-based configuration
- Device validation
- IP validation
- ICMP diagnostics
- Packet-loss measurement
- Latency measurement
- Health assessment
- Logging
- CSV reporting
- Exception handling
- Automated tests
- Git and GitHub version control

The main lesson from this project was that writing code that works is only the beginning.

I also needed to learn how to make the program easier to configure, test, troubleshoot and maintain.

This project created the foundation for the rest of the portfolio.

---

## Project 2 — Log Analyzer

**Status: In progress**

The second project will build directly on Project 1.

Project 1 creates a diagnostic log.

Project 2 will analyse that log.

The idea is to build a Python tool capable of reading log files, identifying important events and turning raw log information into something easier to understand.

I want it to be able to identify things such as:

- INFO messages
- WARNING messages
- ERROR messages
- CRITICAL messages
- affected devices
- repeated problems
- event counts
- useful summaries

This project will help me develop stronger skills in:

- File processing
- Text parsing
- Regular expressions
- String manipulation
- Data transformation
- Dictionaries
- Filtering
- Aggregation
- Report generation

The important connection is that Project 2 will consume information produced by Project 1.

---

## Project 3 — SSH Network Automation

After learning how to analyse network information, I want to start interacting with network devices directly.

The goal of Project 3 is to build automation that can connect to network devices through SSH and perform tasks such as:

- Establishing SSH sessions
- Sending commands
- Collecting device information
- Gathering interface information
- Collecting routing information
- Automating repetitive administrative tasks
- Handling connection failures

This project will take the portfolio from:

```text
Observe the network
```

to:

```text
Interact with the network
```

This is especially relevant to my networking studies because I want to understand how Python can complement the Cisco and networking knowledge I am already developing.

---

## Project 4 — Network Monitoring Tool

The fourth project will take the diagnostic concept from Project 1 and turn it into something more continuous.

Instead of running a diagnostic once, I want to build a basic monitoring system capable of checking devices repeatedly and recording changes over time.

The project will explore concepts such as:

- Repeated checks
- Monitoring intervals
- Historical data
- Device state changes
- Alerts
- Monitoring logs
- Availability
- Performance trends

The idea is to move from:

```text
Run a diagnostic
```

to:

```text
Continuously observe infrastructure
```

This project should bring together many of the concepts learned in the previous projects.

---

## Project 5 — REST API and Automation

Once I am comfortable working with files, network devices and monitoring data, I want to learn how modern applications communicate through APIs.

The goal of this project is to work with:

- REST APIs
- HTTP requests
- JSON responses
- Authentication
- API errors
- Data parsing
- Automation workflows

This project is important because modern infrastructure is increasingly managed through APIs.

The objective is to understand how Python can communicate with external systems rather than only working with local files or direct network-device connections.

---

## Project 6 — Azure Cloud Automation

This is where I want the roadmap to connect with my long-term cloud goals.

The final project will focus on using Python to interact with Microsoft Azure and automate cloud-related tasks.

Possible areas include:

- Azure resources
- Resource groups
- Virtual machines
- Networking
- Storage
- Resource information
- Automation through Azure APIs or SDKs

The idea is to take everything I have learned throughout the portfolio and apply it to cloud infrastructure.

The progression should look something like this:

```text
Python
   ↓
Networking
   ↓
Automation
   ↓
Monitoring
   ↓
APIs
   ↓
Cloud
```

That is the direction I want to take professionally.

---

# The progression I am trying to build

The six projects are intentionally connected.

```text
Project 1
Network Diagnostics
        ↓
Project 2
Log Analysis
        ↓
Project 3
Network Device Automation
        ↓
Project 4
Infrastructure Monitoring
        ↓
Project 5
API Automation
        ↓
Project 6
Azure Cloud Automation
```

Each project should make the next one easier to understand.

I don't want to finish Project 6 and look back at six unrelated applications.

I want to look back and see a progression.

---

# What I want to be able to do by the end

By the end of these six projects, I want to feel comfortable using Python for practical infrastructure tasks.

I want to have experience with:

```text
Python
├── File handling
├── JSON
├── CSV
├── Regular expressions
├── Error handling
├── Logging
├── Testing
├── Subprocesses
├── Networking
├── SSH
├── APIs
├── Automation
└── Cloud SDKs / APIs
```

But more importantly, I want to develop the ability to approach a technical problem and break it down into a working automation solution.

---

# Git and GitHub

Git is also part of this learning process.

I want this repository to document not only the final code, but also how the projects evolve.

I am practising:

- Commits
- Branches
- Repository organisation
- `.gitignore`
- Project structure
- Version control
- GitHub documentation

I want my GitHub profile to eventually show a clear history of progression instead of a collection of disconnected files.

---

# Why networking + Python + cloud?

I am deliberately combining these areas.

Networking gives me the infrastructure foundation.

Python gives me the automation and programming layer.

Cloud engineering gives me the environment where these skills can eventually come together.

My long-term direction looks like:

```text
Networking
     +
Python
     +
Automation
     +
Cloud
     ↓
Infrastructure / Cloud Engineering
```

I know that this is a long process, and I do not expect six projects to turn me into an expert.

The purpose of this portfolio is to build the foundation.

---

# What I am learning from the process

One of the biggest lessons I am learning is that technical growth is not only about learning more technologies.

It is also about learning how to think.

While building these projects, I am trying to become better at:

- Breaking large problems into smaller problems
- Reading errors instead of being afraid of them
- Debugging systematically
- Asking why something works
- Designing before coding
- Testing assumptions
- Improving code after it works
- Documenting what I build
- Using version control properly

The projects are therefore also a way for me to practise my problem-solving skills.

---

# My goal with this repository

My goal is for this portfolio to eventually become evidence of my practical development as an IT professional.

I want someone looking at this repository to be able to see:

```text
"I started learning Python."
        ↓
"I applied it to networking."
        ↓
"I learned automation."
        ↓
"I learned monitoring."
        ↓
"I learned APIs."
        ↓
"I applied it to cloud infrastructure."
```

That story is more important to me than simply having a list of technologies on a CV.

---

# Current Progress

```text
✅ Project 1 — Network Diagnostic Tool
🚧 Project 2 — Log Analyzer
⬜ Project 3 — SSH Network Automation
⬜ Project 4 — Network Monitoring Tool
⬜ Project 5 — REST API / Automation
⬜ Project 6 — Azure Cloud Automation
```

I am building these projects one at a time.

I don't want to rush through the roadmap just to say that I completed six projects.

I want to understand each one, break it, fix it, improve it and learn from it before moving to the next.

---

# Final note

This repository is a work in progress.

It represents where my Python and automation skills are today, not where I expect them to stay.

I am building it while studying, experimenting, making mistakes and gradually becoming more comfortable with infrastructure automation.

The final goal is not simply to say:

> "I know Python."

The goal is to be able to say:

> **"I can use Python to solve practical problems in networking, infrastructure and cloud environments."**

And this portfolio is my way of working towards that goal.

---

## Author

**Durman Sequeira Quiros**

Information Systems Engineering Student  
Networking and Cisco Technologies Student

GitHub:

https://github.com/durmansequeira/python-portfolio