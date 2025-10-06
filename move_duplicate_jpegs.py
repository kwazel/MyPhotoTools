#! /usr/bin/python3
import os
import sys
from typing import List, Set

CAMERA_JPEGS = "camera_jpegs"

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} DIR")
        return
    path = sys.argv[1]
    for dirpath, dirnames, filenames in os.walk(path):
        copy_jpegs = find_copy_jpegs(filenames)
        generate_mv_commands(copy_jpegs, dirpath)

def find_copy_jpegs(filenames: List[str]):
    """Find all jpegs that are just copies of raw images"""
    other_roots = set()
    jpegs = set()
    for filename in filenames:
        root, ext = os.path.splitext(filename)
        if ext.lower() == ".jpg" or ext.lower == ".jpeg":
            jpegs.add((root, filename))
        else:
            other_roots.add(root)
    copy_jpegs = set()
    for jpeg_root, jpeg_filename in jpegs:
        jpeg_desshotwelled = jpeg_root.replace("_RW2_shotwell", "")
        jpeg_desshotwelled = jpeg_root.replace("_dng_shotwell", "")
        if jpeg_desshotwelled in other_roots:
            copy_jpegs.add(jpeg_filename)
    return copy_jpegs

def generate_mv_commands(copy_jpegs: Set[str], dirpath: List[str]):    
    copy_dir = os.path.join(dirpath, "..", "..", CAMERA_JPEGS)
    if copy_jpegs:
        print(f"mkdir -p {copy_dir}")
    for filename in sorted(copy_jpegs):
        root, _ext = os.path.splitext(filename)
        source = os.path.join(dirpath, filename)
        destination = os.path.join(copy_dir, filename)
        print(f"mv {source} {destination}")


if __name__ == "__main__":
    main()

