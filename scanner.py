import socket
import argparse
import logging
from concurrent.futures import ThreadPoolExecutor

# إعداد ملف الـ log
logging.basicConfig(
    filename="scan.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def scan_port(host, port, timeout):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        status = "OPEN"
    except TimeoutError:
        status = "TIMEOUT"
    except ConnectionRefusedError:
        status = "CLOSED"
    except OSError as e:
        status = "ERROR"
        logging.warning(f"{host}:{port} error detail: {e}")
    finally:
        s.close()
    logging.info(f"{host}:{port} -> {status}")
    return port, status


def main():
    parser = argparse.ArgumentParser(description="Simple TCP Port Scanner")
    parser.add_argument("host", help="Target host (e.g. 127.0.0.1 or scanme.nmap.org)")
    parser.add_argument("-s", "--start", type=int, default=1, help="Start port")
    parser.add_argument("-e", "--end", type=int, default=1024, help="End port")
    parser.add_argument("-t", "--timeout", type=float, default=1.0, help="Timeout in seconds")
    parser.add_argument("-w", "--workers", type=int, default=100, help="Number of threads")
    args = parser.parse_args()

    if not (1 <= args.start <= args.end <= 65535):
        print("Error: ports must satisfy 1 <= start <= end <= 65535")
        return

    try:
        ip = socket.gethostbyname(args.host)
    except socket.gaierror:
        print(f"Error: cannot resolve host '{args.host}'")
        logging.error(f"Cannot resolve host {args.host}")
        return

    print(f"Scanning {args.host} ({ip}) from port {args.start} to {args.end}...")
    logging.info(f"Scan started on {args.host} ({ip}) ports {args.start}-{args.end}")

    ports = range(args.start, args.end + 1)
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        results = list(executor.map(lambda p: scan_port(ip, p, args.timeout), ports))

    counts = {"OPEN": 0, "CLOSED": 0, "TIMEOUT": 0, "ERROR": 0}
    for port, status in results:
        counts[status] += 1
        if status == "OPEN":
            print(f"Port {port} is OPEN")

    summary = (f"Open: {counts['OPEN']} | Closed: {counts['CLOSED']} | "
               f"Timeout: {counts['TIMEOUT']} | Error: {counts['ERROR']}")
    print("Scan finished.", summary)
    logging.info(f"Scan finished. {summary}")


if __name__ == "__main__":
    main()