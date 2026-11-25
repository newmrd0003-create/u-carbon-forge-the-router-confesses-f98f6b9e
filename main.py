#!/usr/bin/env python3
"""The Router Confesses — make.fun entry generator.

Writes a single-line router excuse to /output/entry.txt (and a local
entry.txt copy for verification). Deterministic: same input, same bytes.
"""

import hashlib
import os
import sys

# Draft 2 (revised): petty grudge — the hero gets the girl, the router
# gets rebooted. Smug, jealous, one breath, no buffering/firmware angle.
ENTRY = (
    "I killed the Wi-Fi at the climax because the hero gets the girl and "
    "I get rebooted - some of us never get a happy ending."
)


def validate(text: str):
    """Check the gate: UTF-8 text, 1-200 chars, not only whitespace.

    Returns (True, []) when the entry passes, else (False, [reasons]).
    """
    errors = []
    if not text or not text.strip():
        errors.append("entry is empty or only whitespace")
    if len(text) > 200:
        errors.append(f"entry is {len(text)} chars, over the 200 limit")
    if "\n" in text or "\r" in text:
        errors.append("entry must be a single line")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        errors.append(f"entry is not valid UTF-8: {exc}")
    return (not errors, errors)


def main() -> int:
    ok, errors = validate(ENTRY)
    if not ok:
        for err in errors:
            print(f"validate FAILED: {err}", file=sys.stderr)
        return 1

    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(ENTRY + "\n")

    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "entry.txt"), "w", encoding="utf-8",
              newline="\n") as fh:
        fh.write(ENTRY + "\n")

    digest = hashlib.sha256((ENTRY + "\n").encode("utf-8")).hexdigest()
    print(f"entry ({len(ENTRY)} chars): {ENTRY}")
    print(f"sha256: {digest}")
    print("validate: (True, [])")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
