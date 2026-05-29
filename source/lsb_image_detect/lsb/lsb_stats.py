#!/usr/bin/env python3
import argparse
from PIL import Image
import os
import string

def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits), 8):
        chunk = bits[i:i+8]
        if len(chunk) < 8:
            break
        chars.append(chr(int(chunk, 2)))
    return ''.join(chars)

def safe_preview(text):
    out = []
    for c in text:
        if c in string.ascii_letters + string.digits + "_-{}":
            out.append(c)
        elif c in string.printable:
            out.append(".")
        else:
            out.append("?")
    return ''.join(out)

def get_lsb_bits(path, max_bits):
    img = Image.open(path).convert("RGB")
    bits = []

    for r, g, b in img.getdata():
        for value in (r, g, b):
            bits.append(str(value & 1))
            if len(bits) >= max_bits:
                return bits

    return bits

def main():
    parser = argparse.ArgumentParser(description="Compute simple LSB statistics for PNG images.")
    parser.add_argument("--dir", default="samples", help="Directory containing PNG images")
    parser.add_argument("--bits", type=int, default=128, help="Number of leading LSB bits to inspect")
    parser.add_argument("--out", default="findings/lsb_stats.txt", help="Output statistics file")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    files = sorted(
        os.path.join(args.dir, f)
        for f in os.listdir(args.dir)
        if f.lower().endswith(".png")
    )

    lines = []
    lines.append("LSB_STATS_REPORT")
    lines.append(f"DIR={args.dir}")
    lines.append(f"LEADING_BITS={args.bits}")

    for path in files:
        bits = get_lsb_bits(path, args.bits)
        zeros = bits.count("0")
        ones = bits.count("1")
        text = bits_to_text(''.join(bits[:72]))
        preview = safe_preview(text)

        # Điểm nghi vấn đơn giản: chuỗi preview có nhiều ký tự chữ/số liên tiếp.
        printable_count = sum(1 for c in text if c in string.ascii_letters + string.digits)
        score = printable_count

        line = (
            f"FILE={path} zeros={zeros} ones={ones} "
            f"score={score} preview={preview}"
        )
        lines.append(line)

    with open(args.out, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")

    for line in lines:
        print(line)

    print("STATS_OK")

if __name__ == "__main__":
    main()
