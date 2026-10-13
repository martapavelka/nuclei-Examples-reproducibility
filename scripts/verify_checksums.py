#!/usr/bin/env python3
"""Check all preserved SHA256 manifests using Python's standard library."""
from pathlib import Path
import hashlib
import re

ROOT = Path(__file__).resolve().parent.parent
PACKAGES = (
    "classification", "unique-boundary-filling", "automorphisms",
    "spanning-edges", "trefoil-edges", "dual-genus",
)

def main():
    checked = 0
    for name in PACKAGES:
        folder = ROOT / name
        manifests = [p for p in (folder / "SHA256SUMS", folder / "SHA256SUMS.txt") if p.is_file()]
        if len(manifests) != 1:
            raise RuntimeError(f"Expected one SHA256 manifest in {name}")
        for line in manifests[0].read_text().splitlines():
            if not line.strip():
                continue
            m = re.fullmatch(r"([0-9a-fA-F]{64})\s+\*?(.+)", line.strip())
            if not m:
                raise RuntimeError(f"Malformed checksum line in {name}: {line!r}")
            expected, relative = m.groups()
            path = (folder / relative).resolve()
            if not path.is_relative_to(folder.resolve()) or not path.is_file():
                raise RuntimeError(f"Missing or unsafe file: {name}/{relative}")
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual.lower() != expected.lower():
                raise RuntimeError(f"Checksum mismatch: {name}/{relative}")
            checked += 1
        print(f"PASS: {name}")
    print(f"All {checked} recorded file checksums match.")

if __name__ == "__main__":
    main()
