"""Worst Fix Ever: Funniest Commit Message.

Writes one commit message to $MAKEFUN_OUTPUT_DIR/entry.txt.

The line is a commit message for a bug fix that made everything worse:
the complaints about the bug stopped only because the fix deleted the
people who were complaining — the repair "worked" by removing the users
instead of the bug. That is the whole joke, and it lands in one read:
a tired engineer typing a plain commit subject at the end of a bad day,
with the escalation (complaints -> deleted accounts) doing the work.
The gate is 1-100 characters (the bounty caps the line at 100
characters), UTF-8, not only whitespace, and the file must carry no
trailing newline so the byte count is the line itself.
"""

import os
import sys

TEXT = "fix: users stopped complaining about the bug after we deleted their accounts"


def gate(text):
    """Check the line against the bounty gate: 1-100 chars, UTF-8, real text."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    text.encode("utf-8")
    if not 1 <= len(text) <= 100:
        raise ValueError("entry must be 1-100 characters, got %d" % len(text))
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def main():
    text = gate(TEXT)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    os.chmod(path, 0o644)
    # Read back and verify byte-identical, then re-run the gate on it.
    with open(path, "rb") as f:
        raw = f.read()
    if raw != text.encode("utf-8"):
        raise ValueError("read-back mismatch")
    gate(raw.decode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
