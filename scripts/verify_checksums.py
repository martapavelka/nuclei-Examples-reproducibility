#!/usr/bin/env python3
"""Check the research-directory SHA256 manifests using the standard library."""
from pathlib import Path
import hashlib
import re

ROOT = Path(__file__).resolve().parent.parent
PACKAGES = (
    "classification", "unique-boundary-filling", "automorphisms",
    "spanning-edges", "trefoil-edges", "dual-genus",
    "nuclei_intrinsic_spines_and_evasiveness",
    "atom-reduction-nonuniqueness",
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
    root_manifest = ROOT / "SHA256SUMS_ROOT.txt"
    if not root_manifest.is_file():
        raise RuntimeError("Missing repository checksum manifest")
    root_entries = set()
    for line in root_manifest.read_text().splitlines():
        if not line.strip():
            continue
        m = re.fullmatch(r"([0-9a-fA-F]{64})\s+\*?(.+)", line.strip())
        if not m:
            raise RuntimeError(f"Malformed repository checksum entry: {line!r}")
        expected, relative = m.groups()
        path = (ROOT / relative).resolve()
        if not path.is_relative_to(ROOT.resolve()) or not path.is_file():
            raise RuntimeError(f"Missing or unsafe repository file: {relative}")
        if hashlib.sha256(path.read_bytes()).hexdigest().lower() != expected.lower():
            raise RuntimeError(f"Repository checksum mismatch: {relative}")
        root_entries.add(relative)
    files = {str(p.relative_to(ROOT)) for p in ROOT.rglob("*")
             if p.is_file() and p.name != "SHA256SUMS_ROOT.txt"}
    if files != root_entries:
        missing = sorted(files - root_entries)
        excess = sorted(root_entries - files)
        raise RuntimeError(f"Incomplete repository manifest: missing={missing}, extra={excess}")
    print(f"All {checked} package checksums and {len(root_entries)} repository checksums match.")

if __name__ == "__main__":
    main()
