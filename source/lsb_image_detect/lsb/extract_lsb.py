#!/usr/bin/env python3
import argparse
from PIL import Image

def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits), 8):
        chunk = bits[i:i+8]
        if len(chunk) < 8:
            break
        chars.append(chr(int(chunk, 2)))
    return ''.join(chars)

def main():
    parser = argparse.ArgumentParser(description="Extract hidden text from LSBs of an RGB PNG.")
    parser.add_argument("--input", required=True, help="Input PNG file")
    parser.add_argument("--output", required=True, help="Output text file")
    parser.add_argument("--msg-len", type=int, required=True, help="Message length in characters")
    args = parser.parse_args()

    img = Image.open(args.input).convert("RGB")

    total_bits = args.msg_len * 8
    bits = []

    for r, g, b in img.getdata():
        for value in (r, g, b):
            if len(bits) < total_bits:
                bits.append(str(value & 1))

    text = bits_to_text(''.join(bits))

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(text)

    print("EXTRACT_RUN_OK")
    print(f"INPUT={args.input}")
    print(f"OUTPUT={args.output}")
    print(f"MSG_LEN={args.msg_len}")
    print(f"EXTRACTED_TEXT={text}")

if __name__ == "__main__":
    main()
