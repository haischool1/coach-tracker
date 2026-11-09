# Build Your Own Coach: the tracker checker. It only reads files. It never changes anything and never goes online.
#
#   python3 check_tracker.py <saved tracker page> [--versions version.json]
#       Which kit version is this tracker page, and was it changed after setup?
#       Read their tracker with the Artifact tool first (action "read"), then run this on the file it saved.
#       With --versions (the version.json downloaded from GitHub) it also knows versions newer than this kit.
#
#   python3 check_tracker.py --verify <downloaded tracker-template.html> --versions version.json
#       Is a tracker page downloaded from GitHub safe to publish? version.json must carry the maker's signature, the page
#       must be the exact file it describes, and it must not contain anything that could send a person's data somewhere else.
#       Prints SAFE TO USE, or DO NOT USE with the reason (and exits with an error).
#
# The kit's build fills in LATEST and KNOWN. Don't edit them by hand.
import hashlib, json, re, sys

LATEST = "3.4.2"
KNOWN = {
    "1fd87ccd81091261": "3.4.0",
    "4adf5baa31129e14": "3.4.1",
    "72dbed3f92ee4e2d": "3.3.2",
    "7db65d1a10d4fe06": "3.3.3",
    "ae0cd4869893c9c2": "3.0",
    "b2316d2271fb5bac": "3.3.0",
    "c4fb11c6943d9fa5": "3.2",
    "d3d26eb05bba47b2": "3.4.2",
    "e11c295c3b6bfef0": "3.3.1",
    "e75b9526fda5b2d9": "3.2.1",
    "f5ba97bbf9b0f172": "2",
    "f721ef4d2a213e08": "3.1"
}
# The maker's public keys (the big number of each RSA key, in hex). A release is only trusted when its signature in version.json
# was made with the matching private key, which never leaves the maker's computer and is never on GitHub.
PUBKEYS = ["c5ed9fbc62d5d09ccff7aade4a7ad7c0aaf79607408464ba65f823a9189ec33d9448dcbe3bc448a132d63a28b9e6cb20d793b800aa4f34d8a63fdf1070409426fc358c0c564562bc89ec53fa7018df3dbaecf08273a98847cc32b8b9d496afcb5b5bd0e638d817cd6edf77f4dbf158e51e0409e5b0df3ddce24154dbfea05968bae1c6c59d7f529406c7841570d237d478551d1f3da901426201b778cdb42adb31e3cc0b85b32c36475a4265d71e64cda49b10b1cf3ed90d9f7f908cce102ab5ed7606cfb03b30b739807e0cecbab2fa77d0d518f792299b9babcabf7f70b38035048a31777a19bdc9b5d899b57b895bf44da47c1dfaa5a47142b9414bd90b5c593c25b7ec90ef98a6a111f08317b29ba795f38d262bb6a761c707fcca0f026d14183de00d57ad7c58b295e9f3fbe4c08cc57a40d19d38fb41693139876e078949b67c8c69fd767720fa9a1029cf9a9f3b500267675d792af5b98fba75ac5eefd26e0cf2d793437da326b8335a5d70bc95efb7e6569ffabbc53c779ae66b7de7"]

# The only outside addresses a tracker page may mention: the form-video search link and the page's font.
ALLOWED_HOSTS = {"www.youtube.com", "fonts.googleapis.com", "fonts.gstatic.com", "www.w3.org"}
# Things a tracker page never needs. Any of them in a downloaded page means: do not publish it.
FORBIDDEN = ["fetch(", "XMLHttpRequest", "sendBeacon", "WebSocket", "EventSource", "<script src", "<iframe", "<object", "<embed", "<form action",
             "eval(", "new Function", "importScripts", "atob(", "document.cookie", "location.assign", "location.replace", "location.href=",
             "location.href =", "window.open(", "serviceWorker", "globalThis[", "window[", "self["]

def ver(s):   # "3.4.2" -> (3, 4, 2), for comparing versions
    return tuple(int(x) for x in re.findall(r"\d+", str(s)))

def fingerprint(html):   # the page minus the wrapper claude.ai adds and minus the <title> line
    s = html.replace("\r\n", "\n")
    i = s.find("<title>")
    if i >= 0: s = s[i:]
    s = re.sub(r"^<title>.*?</title>\n", "", s, count=1).strip()
    if s.endswith("</body></html>"): s = s[:-len("</body></html>")].strip()
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]

def load_versions(args):
    if "--versions" not in args: return {}
    try:
        v = json.load(open(args[args.index("--versions") + 1], encoding="utf-8"))
        return v if isinstance(v, dict) else {}
    except Exception:
        return {}

def manifest(info):   # the exact text the maker signs: the version, the page's fingerprint, the kit it needs and the what's-new text
    notes = hashlib.sha256(str(info.get("notes") or "").encode("utf-8")).hexdigest()
    return ("byoc-release\n%s\n%s\n%s\n%s\n" % (info.get("version"), info.get("sha256"), info.get("needsKit") or "", notes)).encode("utf-8")

def signed_by_maker(info):   # RSA signature check (PKCS#1 v1.5 with SHA-256), in plain Python so nothing has to be installed
    try:
        sig = int(str(info.get("signature") or ""), 16)
    except ValueError:
        return False
    digest = hashlib.sha256(manifest(info)).digest()
    prefix = bytes.fromhex("3031300d060960864801650304020105000420")   # says "this is a SHA-256 fingerprint"
    for nhex in PUBKEYS:
        n = int(nhex, 16); k = (n.bit_length() + 7) // 8
        if not 0 < sig < n: continue
        want = b"\x00\x01" + b"\xff" * (k - len(prefix) - len(digest) - 3) + b"\x00" + prefix + digest
        if pow(sig, 65537, n).to_bytes(k, "big") == want: return True
    return False

def scan(html):   # reasons this page must not be published (an empty list means none found)
    bad = []
    for host in sorted(set(re.findall(r"(?:https?:)?//([A-Za-z0-9.-]+\.[A-Za-z]{2,})", html))):
        if host.lower() not in ALLOWED_HOSTS: bad.append("it mentions an outside address: " + host)
    for word in FORBIDDEN:
        if word in html: bad.append("it contains " + word.strip())
    return bad

def verify(path, info):
    raw = open(path, "rb").read()
    html = raw.decode("utf-8", errors="replace")
    why = []
    want = str(info.get("sha256") or "")
    if not want: why.append("version.json has no sha256 for the page, so it can't be checked")
    elif hashlib.sha256(raw).hexdigest() != want: why.append("the file is not the one version.json describes (the sha256 does not match)")
    if not info.get("signature"): why.append("version.json has no signature from the maker")
    elif not signed_by_maker(info): why.append("the maker's signature does not match, so this release did not come from the maker")
    m = re.search(r'<meta name="byoc-version" content="([^"]+)">', html)
    if not m: why.append("it has no byoc-version line, so it is not a tracker page")
    elif str(info.get("version")) != m.group(1): why.append("the page says version %s but version.json says %s" % (m.group(1), info.get("version")))
    if "config/main" not in html: why.append("it does not look like a tracker page")
    why += scan(html)
    need = info.get("needsKit")
    if need and ver(need) > ver(LATEST):
        why.append("this page needs kit %s or newer and this kit is %s. Ask them to download the newest kit file from where they bought it, add the new skill, and say update my tracker again" % (need, LATEST))
    if why:
        print("DO NOT USE this downloaded page:")
        for w in why: print(" -", w)
        print("Use this skill's own tracker-template.html instead, and tell them in one line that the online update could not be checked.")
        sys.exit(1)
    print("SAFE TO USE: signed by the maker, it is the page version.json describes (version %s), and nothing in it sends data anywhere." % m.group(1))

def main():
    args = sys.argv[1:]
    info = load_versions(args)
    if "--verify" in args:
        if "--versions" not in args: sys.exit("Usage: python3 check_tracker.py --verify <downloaded page> --versions <version.json>")
        return verify(args[args.index("--verify") + 1], info)
    files = [a for i, a in enumerate(args) if not a.startswith("--") and (i == 0 or args[i - 1] != "--versions")]
    if not files:
        sys.exit("Usage: python3 check_tracker.py <saved tracker page> [--versions version.json]")
    html = open(files[0], encoding="utf-8").read()
    known = dict(KNOWN)
    extra = info.get("fingerprints")
    if isinstance(extra, dict): known.update({str(k): str(v) for k, v in extra.items()})
    latest = str(info.get("version")) if info.get("version") and ver(info["version"]) > ver(LATEST) else LATEST
    m = re.search(r'<meta name="byoc-version" content="([^"]+)">', html)
    fp = fingerprint(html)
    if fp in known:
        v, changed = known[fp], False
    elif m:
        v, changed = m.group(1), True
    elif "Build Your Own Coach" in html and "config/main" in html:
        v, changed = "2", True
    else:
        print("This doesn't look like a Build Your Own Coach tracker. Don't update it with this kit.")
        return
    print("Kit version:", v)
    print("Changed after setup:", "yes, carry the 'Custom:' changes from tracker-notes.md over" if changed else "no")
    print("Latest version:", latest, "(up to date)" if v == latest and not changed else "(update available)" if ver(v) < ver(latest) else "")

if __name__ == "__main__":
    main()
