#!/usr/bin/env bash
set -euo pipefail
python3 dual_genus.py --selftest --selftest-seconds 30
for X in N00 N0 N1; do
  echo "=== $X ==="
  python3 dual_genus.py "$X.txt" --anneal 30 --cert "${X}_certificate.txt" --json "${X}_certificate.json" | tee "${X}_run.log"
done
