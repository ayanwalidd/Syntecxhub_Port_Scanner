# Syntecxhub Port Scanner

A multi-threaded TCP port scanner written in Python, built as part of the Syntecxhub Cybersecurity Internship (Task 1, Project 1).

## Features
- Scan a single port or a range of ports
- Multi-threaded scanning for speed (ThreadPoolExecutor)
- Classifies each port as OPEN, CLOSED, TIMEOUT, or ERROR
- Logs every result with a timestamp to `scan.log`
- Handles invalid hosts, invalid port ranges, and network errors
- Configurable timeout and thread count

## Requirements
- Python 3.8+
- No external libraries (standard library only)

## Usage
```
python scanner.py <host> [-s START] [-e END] [-t TIMEOUT] [-w WORKERS] [-v]
```

| Option | Description | Default |
|---|---|---|
| `host` | Target hostname or IP | required |
| `-s`, `--start` | First port to scan | 1 |
| `-e`, `--end` | Last port to scan | 1024 |
| `-t`, `--timeout` | Timeout per port (seconds) | 1.0 |
| `-w`, `--workers` | Number of threads | 100 |
| `-v`, `--verbose` | Print closed/timeout/error ports too | off |

## Examples
```
# Scan ports 1-1000 on localhost
python scanner.py 127.0.0.1 -s 1 -e 1000

# Scan a single port
python scanner.py 127.0.0.1 -s 8000 -e 8000

# Faster scan with a shorter timeout
python scanner.py 127.0.0.1 -s 1 -e 1000 -t 0.5

# Print every port state, not just open ones
python scanner.py 127.0.0.1 -s 1 -e 100 -v
```

## Sample Output
```
Scanning 127.0.0.1 (127.0.0.1) from port 1 to 1000...
Port 135 is OPEN
Port 445 is OPEN
Scan finished. Open: 4 | Closed: 0 | Timeout: 995 | Error: 1
```

## Port States
| State | Meaning |
|---|---|
| OPEN | A service accepted the connection |
| CLOSED | The host actively refused the connection |
| TIMEOUT | No response (often a firewall dropping packets) |
| ERROR | Another network or OS-level error (details in `scan.log`) |

## Legal Disclaimer
This tool is for educational purposes only. Only scan systems you own or have explicit permission to test. Scanning others' systems without authorization may be illegal. `scanme.nmap.org` is a host provided for testing.

## Author
Ayan Ebeid - Syntecxhub Cybersecurity Intern