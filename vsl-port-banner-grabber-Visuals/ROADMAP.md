# vsl-port-banner-grabber roadmap

Written 2026-10-30 from the repo as it stands. No dates on the future
items, because I do not know when I will be back in this code, and a
date I invent here would be a small lie in a public file.

## Done

- The full tool, landed in one day of commits (2025-01-02):
  setup_argparse with -t, -p, -o, and --version; resolve_target on
  gethostbyname; scan_ports over the named ports or the common
  nine; get_service_banner with a 3 second timeout, a blank line
  probe, and a 1024 byte read; results printed per port and saved
  when -o is given.
- A license file (GPL version 3) and a requirements file.
- These visuals, and a VISUAL.md that records the unused imports
  instead of leaving them for the next reader to find.

## Working now

- Nothing in flight. The repo has not changed since 2025-01-02
  apart from the campaigns that documented it.

## Next

- Drop the unused imports. main.py imports nmap and tldextract and
  never calls them, and requirements.txt lists both. On a machine
  without them the tool will not even start, which I confirmed in
  my sandbox on 2026-10-30: the import fails before --help can
  print. Removing two import lines and the requirements entries
  makes the tool run on the standard library alone, which is all
  its code ever used.
- Nothing else is queued. The code has no TODO or FIXME markers in
  it (checked 2026-10-30), so this section stays short on purpose.

## Later

- A short README usage section with a real example run. The
  current README is 14 lines and its usage line names a command
  form the parser does not take; the code and its --help are the
  honest reference until that is rewritten.

## Not planned

- UDP scanning or service probes beyond the banner. The tool asks
  one polite question per port; turning it into a prober is a
  different tool, and nmap already exists for that work.
- Parallel scanning. Nine ports at a 3 second worst case finish
  fast enough in sequence for how I use it.
