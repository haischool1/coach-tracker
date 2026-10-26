# Which Build Your Own Coach version is a tracker page, and was it changed after setup?
#   python3 check_tracker.py <saved tracker page>
# Read their tracker with the Artifact tool first (action "read"), then run this on the file it saved.
# The kit's build (workout-plans/app/build.py --kit) fills in KNOWN; don't edit it by hand.
import hashlib, re, sys

LATEST = "3.3.0"
KNOWN = {
    "0f3a4fd2a7c5e8a3": "3.2.1",
    "PLACEHOLDER": "x"
}
