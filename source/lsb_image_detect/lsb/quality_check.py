#!/usr/bin/env python3
import argparse
from PIL import Image
import os
import sys

def main():
    parser = argparse.ArgumentParser(description="Check that a PNG image is valid.")
    parser.add_argument("--input", required=True, help="Image to check")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print("QUALITY_FAIL")
        print("missing input")
        sys.exit(1)

    try:
        img = Image.open(args.input)
        fmt = img.format
        mode = img.mode
        size = img.size
        img.verify()
    except Exception as e:
        print("QUALITY_FAIL")
        print(f"error={e}")
        sys.exit(1)

    print(f"INPUT={args.input}")
    print(f"FORMAT={fmt}")
    print(f"MODE={mode}")
    print(f"SIZE={size}")

    if fmt == "PNG":
        print("QUALITY_OK")
    else:
        print("QUALITY_FAIL")

if __name__ == "__main__":
    main()
