#!/usr/bin/env python3
"""Run the quick, bounded verifiers without starting an exhaustive search."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
COMMANDS = [
    ["scripts/verify_checksums.py"],
    ["automorphisms/verify_automorphisms.py"],
    ["classification/src/verify_n00_collapse_strict.py", "classification/results/n00_collapse_certificate.json"],
    ["classification/src/verify_n00_positive.py"],
    ["trefoil-edges/verify_inputs.py"],
]

def main():
    for args in COMMANDS:
        print(f"\n==> {' '.join(args)}", flush=True)
        proc = subprocess.run([sys.executable, '-B', *args], cwd=ROOT, check=False)
        if proc.returncode:
            raise SystemExit(f"FAILED ({proc.returncode}): {' '.join(args)}")
    print("\nAll quick checks passed. The expensive enumerations and SAT searches were NOT run.")

if __name__ == "__main__":
    main()
