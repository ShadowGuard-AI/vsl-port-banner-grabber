import argparse
import socket
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def setup_argparse():
    """
    Sets up the command-line argument parser.

    Returns:
        argparse.ArgumentParser: Configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description="vsl-port-banner-grabber: A lightweight tool to grab service banners from open TCP ports."
    )
    parser.add_argument(
        "-t", "--target",
        required=True,
        help="Target IP address or hostname."
    )
    parser.add_argument(
        "-p", "--ports",
        help="Comma-separated list of ports to scan (e.g., 80,443,22). If not provided, a common port list is used."
    )
    parser.add_argument(
        "-o", "--output",
        help="Optional output file to save the results."
    )
    parser.add_argument(
        "--version",
        action="version",
        version="vsl-port-banner-grabber 1.0",
        help="Show the version of the tool and exit."
    )
    return parser


def get_service_banner(ip, port):
    """
    Attempts to connect to a specified port on the target IP and retrieve the service banner.

    Args:
        ip (str): Target IP address.
        port (int): Port number.

    Returns:
        str: The retrieved service banner or an error message.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)  # Timeout after 3 seconds
            s.connect((ip, port))
            # I speak first, with a blank line. A service waiting for a real request, HTTP being the
            # common one, answers that empty line with an error or with silence, so the banner I
            # record is shaped by my probe and not only by the service.
            s.sendall(b"\r\n")  # Send a blank request
            # One recv is all I take. A banner split across packets comes back as its first piece
            # only, and anything past 1024 bytes is cut off mid line.
            banner = s.recv(1024).decode(errors="replace").strip()
            return banner if banner else "No banner retrieved."
    except (socket.timeout, ConnectionRefusedError, socket.error) as e:
        # Refused, filtered, and connected but silent all land in this one Error string. Their only
        # difference is the operating system wording pasted after the colon.
        return f"Error: {str(e)}"


def scan_ports(target, ports):
    """
    Scans the specified ports on the target and retrieves service banners.

    Args:
        target (str): Target IP address or hostname.
        ports (list): List of ports to scan.

    Returns:
        dict: Mapping of port numbers to service banners or error messages.
    """
    results = {}
    for port in ports:
        logging.info(f"Scanning port {port}...")
        banner = get_service_banner(target, int(port))
        # The results are keyed by port, so a port listed twice is probed twice and stored once.
        # The second answer quietly replaces the first, and the output never shows it happened.
        results[port] = banner
    return results


def resolve_target(target):
    """
    Resolves the target to an IP address if a hostname is provided.

    Args:
        target (str): Target hostname or IP address.

    Returns:
        str: Resolved IP address.
    """
    try:
        ip = socket.gethostbyname(target)
        logging.info(f"Resolved {target} to {ip}")
        return ip
    except socket.gaierror as e:
        logging.error(f"Failed to resolve target: {e}")
        raise ValueError(f"Invalid target: {target}")


def main():
    """
    Main function to handle command-line arguments and execute the banner grabbing process.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    # Resolve target
    try:
        target_ip = resolve_target(args.target)
    except ValueError as e:
        logging.error(e)
        sys.exit(1)

    # Determine ports to scan
    if args.ports:
        try:
            ports = [int(p.strip()) for p in args.ports.split(",")]
        except ValueError:
            logging.error(f"Invalid port list: {args.ports!r}. Ports must be integers separated by commas.")
            sys.exit(1)
        if any(port < 1 or port > 65535 for port in ports):
            logging.error(f"Invalid port list: {args.ports!r}. Ports must be between 1 and 65535.")
            sys.exit(1)
    else:
        # Default to common ports if none are provided
        ports = [80, 443, 22, 21, 25, 110, 143, 3306, 8080]

    # Perform the scan
    logging.info(f"Starting scan on {target_ip}...")
    results = scan_ports(target_ip, ports)

    # Display results
    for port, banner in results.items():
        print(f"Port {port}: {banner}")

    # Save results to file if requested
    if args.output:
        try:
            with open(args.output, "w") as f:
                for port, banner in results.items():
                    f.write(f"Port {port}: {banner}\n")
            logging.info(f"Results saved to {args.output}")
        except IOError as e:
            logging.error(f"Failed to save results: {e}")


if __name__ == "__main__":
    main()