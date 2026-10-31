# vsl-port-banner-grabber, drawn out

I made these five pictures because the tool is small enough that its
whole behavior fits on a page, and I would rather show the exchange
than describe it. Everything in them comes from main.py, all 143
lines of it, and from the README beside it.

One naming note, stated plainly: this clone was taken from
github.com/ShadowGuardAI/vsl-port-banner-grabber, the public home
this repo actually has. The ShadowGuard-AI org copy does not exist
yet (the API answers 404 for it), so the API rows below cite the
ShadowGuardAI repo the clone came from.

## The visuals

- [architecture.svg](architecture.svg): the system shape. Target on
  the left, the functions of main.py in a column in the middle,
  the service answering on the right.
- [sequence.svg](sequence.svg): one port, one exchange, in time
  order across four lifelines: me, main(), the resolve and scan
  functions, and the service.
- [flowchart.svg](flowchart.svg): a scan followed port by port,
  with the loop back to the next port drawn as a loop, because that
  is what scan_ports does.
- [product-map.svg](product-map.svg): the product as a wheel: the
  tool at the hub, who it serves, inputs, outputs, and boundaries
  on four spokes.
- [statistics.svg](statistics.svg): the numbers from the table
  below, drawn as bars on paper. The license text is the longest
  bar, and the sheet says why.

Each sheet also ships as a PNG beside its SVG (architecture.png,
flowchart.png, and so on): the same drawing, finished as a photograph
of the paper page.

Every sheet here is drawn to look like what it is: a page sketched by
hand on paper, and each one is signed GK somewhere in the drawing,
never twice in the same place, because that is what I do with a page
I made.

## Written product map

What it is: a small command line tool that connects to TCP ports on
a target, sends one blank line, and reports the banner text each
service sends back, printed to the terminal and optionally saved
to a file.

Who it serves: me, taking a first look at a machine I am allowed to
look at: what is listening, and what does it call itself.

Capabilities, grouped:

- Target handling: resolve_target turns a hostname into an IP with
  socket.gethostbyname and logs the answer; a name that will not
  resolve raises ValueError, main() logs it, and the run stops
  before any port is touched.
- The grab itself, get_service_banner: a TCP socket with a 3 second
  timeout, connect, sendall of one blank line (CRLF), one recv of up
  to 1024 bytes, stripped and decoded. An empty answer becomes "No
  banner retrieved."; a timeout, a refusal, or a socket error
  becomes the error text, kept as that port result.
- The scan loop, scan_ports: one pass over the port list, a log line
  per port, and a dict of port to banner as the result.
- Reporting: main() prints "Port <n>: <banner>" for every port and,
  with -o, writes the same lines to the output file; a failed save
  is logged.

Inputs: -t target (required, IP or hostname), -p a comma separated
port list, -o an optional output file, --version. Without -p, the
port list is the common nine: 80, 443, 22, 21, 25, 110, 143, 3306,
8080. Outputs: the printed lines and, when asked, the results file.

Boundaries, what it does NOT do: TCP only, no UDP. It sends one
blank line and reads one answer; it does not log in, does not probe
past the banner, and runs no version or vulnerability tests of its
own, whatever the old README line about vulnerability
identification suggests. The scanning work runs on the socket
module alone. main.py also imports nmap and tldextract at the top
and never calls either of them; requirements.txt still lists both,
which is drift between the files that these visuals record rather
than hide.

## Statistics, with citations

Counted 2026-10-30, from the clone this folder ships in, at the
commit before this visuals set (0f917a3).

| Number | Value | How it was counted, and from what |
|---|---|---|
| Files in the repo | 4 | git ls-files in the clone, counted 2026-10-30 |
| Python lines | 143 | Line count over the 1 tracked .py file (main.py), by wc -l, 2026-10-30 |
| Markdown lines | 14 | Line count over the 1 tracked .md file (README.md), same method, 2026-10-30 |
| LICENSE lines | 674 | Line count over the tracked LICENSE file (no extension; the GPL version 3 text), same method, 2026-10-30 |
| Text lines | 3 | Line count over the 1 tracked .txt file (requirements.txt, including its code fence lines), same method, 2026-10-30 |
| Commits | 5 | git log in the clone, counted 2026-10-30 |
| First commit | 2025-01-02 | git log, oldest entry, 2026-10-30 |
| Last commit before this one | 2025-01-02 | git log, newest entry, 2026-10-30. Every commit in this repo carries the same date. |
| Tests | 0 test files; not run | No test file exists in the clone (git ls-files shows none), counted 2026-10-30. The tool also would not start in my sandbox on 2026-10-30: python3 main.py --help stops with "ModuleNotFoundError: No module named 'nmap'", because nmap is imported at the top of main.py and is not installed here, and installing was out of scope for this pass. No run and no pass is claimed. |
| Languages (API) | Python 4,075 bytes | GitHub API, GET /repos/ShadowGuardAI/vsl-port-banner-grabber/languages, read 2026-10-30. The ShadowGuard-AI org path answers 404; this is the repo the clone came from. |
| Repo size (API) | 17 KB | GitHub API, GET /repos/ShadowGuardAI/vsl-port-banner-grabber, size field, read 2026-10-30 |
| Stars / forks (API) | 0 / 0 | Same API response, read 2026-10-30 |

External statistics: none. No outside number says anything honest
about this repo, so the repo's own numbers are the whole table.

## Roadmap summary

Done: the whole tool in one sitting, resolve, scan, grab, print,
save, all present since the first day of commits. Working now:
nothing in flight. Next, if I return to it: remove the two unused
imports and the requirements entries that go with them, so the
tool starts on a machine with nothing installed. The full roadmap,
with the Later and Not planned sections, is in
[ROADMAP.md](ROADMAP.md).
