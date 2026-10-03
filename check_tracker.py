# Which Build Your Own Coach version is a tracker page, and was it changed after setup?
#   python3 check_tracker.py <saved tracker page>
# Read their tracker with the Artifact tool first (action "read"), then run this on the file it saved.
# The kit's build fills in KNOWN; don't edit it by hand.
import hashlib, re, sys

LATEST = "3.1"
KNOWN = {
    "ae0cd4869893c9c2": "3.0",
    "f5ba97bbf9b0f172": "2",
    "f721ef4d2a213e08": "3.1"
}

def fingerprint(html):   # the page minus the wrapper claude.ai adds and minus the <title> line
    s = html.replace("\r\n", "\n")
    i = s.find("<title>")
    if i >= 0: s = s[i:]
    s = re.sub(r"^<title>.*?</title>\n", "", s, count=1).strip()
    if s.endswith("</body></html>"): s = s[:-len("</body></html>")].strip()
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]

def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 check_tracker.py <saved tracker page>")
    html = open(sys.argv[1], encoding="utf-8").read()
    m = re.search(r'<meta name="byoc-version" content="([^"]+)">', html)
    fp = fingerprint(html)
    if fp in KNOWN:
        v, changed = KNOWN[fp], False
    elif m:
        v, changed = m.group(1), True
    elif "Build Your Own Coach" in html and "config/main" in html:
        v, changed = "2", True
    else:
        print("This doesn't look like a Build Your Own Coach tracker. Don't update it with this kit.")
        return
    print("Kit version:", v)
    print("Changed after setup:", "yes, carry the 'Custom:' changes from tracker-notes.md over" if changed else "no")
    print("Latest version:", LATEST, "(up to date)" if v == LATEST and not changed else "(update available)" if v != LATEST else "")

if __name__ == "__main__":
    main()
