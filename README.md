# vsl-port-banner-grabber

A lightweight command line tool that connects to TCP ports on a target host, sends a blank line, and prints the service banner the host sends back. Banners can help identify which service and version is listening on a port. Use it only against systems you own or are authorized to test.

## Requirements

- Python 3.10 or later (tested on Python 3.12)
- No third-party dependencies. The tool uses only the Python standard library (argparse, socket, logging, sys), so requirements.txt intentionally lists nothing to install.

## Installation

1. Clone the repository: `git clone https://github.com/ShadowGuardAI/vsl-port-banner-grabber.git`
2. Move into the directory: `cd vsl-port-banner-grabber`

## Usage

```
python main.py -t TARGET [-p PORTS] [-o OUTPUT] [--version]
```

- `-t` / `--target`: target IP address or hostname (required). Hostnames are resolved to an IP address before scanning.
- `-p` / `--ports`: comma separated list of ports to scan, for example `22,80,443`. If omitted, a built in list of common ports is used: 80, 443, 22, 21, 25, 110, 143, 3306, 8080.
- `-o` / `--output`: optional path to a text file the results are also written to.
- `--version`: print the version (vsl-port-banner-grabber 1.0) and exit
- `-h` / `--help`: show help and exit

## Example

```
python main.py -t 127.0.0.1 -p 22,80
```

Example output:

```
Port 22: SSH-2.0-OpenSSH_8.9p1
Port 80: Error: [Errno 111] Connection refused
```

Saving the same results to a file:

```
python main.py -t 127.0.0.1 -p 22,80 -o results.txt
```

## Behavior and limitations

- Each connection has a 3 second timeout. A port that accepts a connection, sends nothing, and keeps the connection open is reported as `Error: timed out` after about 3 seconds. A port that accepts a connection and closes it without sending anything is reported as `No banner retrieved.`
- Closed or filtered ports are reported on their own line as `Port N: Error: ...` rather than aborting the scan.
- Banners that are not valid UTF-8 text are printed with replacement characters instead of crashing the scan.
- An invalid port list (non numeric values, or ports outside 1 to 65535) and an unresolvable target are reported as errors with exit code 1.
- The tool sends a blank line and reads up to 1024 bytes. It does not send protocol specific probes, so some services will return only a first line or nothing at all.
- This is a banner grabber only. It does not run an nmap scan, fingerprint vulnerabilities, or test credentials.

## License

See LICENSE in this repository.
