#!/usr/bin/env python3
import argparse
import subprocess
import fs

parser = argparse.ArgumentParser()
parser.add_argument("--size", type=int, help="Disk image size", default=128*512)
parser.add_argument("disk", type=str, help="Disk image file")
parser.add_argument("html", type=str, help="Config HTML file")

args = parser.parse_args()

with open(args.disk, "wb") as f:
    f.write(bytearray(args.size))

subprocess.run(["mkdosfs", "-F12", "-n", "DESKHOP", "-i", "0", args.disk], check=True)

with fs.open_fs(f"fat://{args.disk}", writeable=True, create=True) as f:
    with f.openbin("/config.htm", "w") as file:
        file.write(open(args.html, "rb").read())
