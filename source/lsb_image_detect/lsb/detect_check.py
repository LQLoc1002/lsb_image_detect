#!/usr/bin/env python3
import os
import sys

expected = "samples/image03.png"
path = "suspect.txt"

if not os.path.exists(path):
    print("DETECT_FAIL")
    print("missing suspect.txt")
    sys.exit(1)

with open(path, "r", encoding="utf-8", errors="ignore") as f:
    value = f.read().strip()

print(f"SUSPECT={value}")

if value == expected or value == "image03.png":
    print("DETECT_OK")
else:
    print("DETECT_FAIL")
