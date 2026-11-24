#!/usr/bin/env python3
"""THE WORLD TODAY -- entrypoint for make.fun news-image-20261124.

The front page (1024x1024, Tuesday 24 November 2026) is drawn by
draw_frontpage.py, which produced the entry.png shipped in this repository.
This entrypoint is standard library only: it copies that image to the
grader's output directory, so it runs in the sandbox (no network, a
read-only repository, nothing installed before it runs).

Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    with open(src, "rb") as f:
        want = hashlib.sha256(f.read()).hexdigest()
    with open(dst, "rb") as f:
        got = hashlib.sha256(f.read()).hexdigest()
    assert want == got, "copied entry.png does not match the repository copy"
    print("wrote", dst, "sha256", got)


if __name__ == "__main__":
    main()
