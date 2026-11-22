#!/usr/bin/env python3
"""Rebuild the report figures from the saved outputs of the two notebooks.

Every figure in the report is a rendered output of a notebook cell, so the report
cannot drift away from the code that produced it. Run this before `./build.sh`:

    python3 make_figures.py

The cell indices below are the plotting cells in the current notebooks. If a cell is
inserted or removed, update the index and re-run; the script fails loudly rather than
writing a wrong figure.
"""
import base64
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
TAB_NB = os.path.join(ROOT, "Notebook", "DataMining&MachineLearning_Coursework_01.ipynb")
CNN_NB = os.path.join(ROOT, "Notebook", "Phishing_Image_CNN_Pipeline.ipynb")
FIGURES = os.path.join(HERE, "figures")

# plotting cell -> which panel of which figure
SOURCES = {
    "url_length": (TAB_NB, 24, 0),   # histogram of URL length by class
    "flag_rates": (TAB_NB, 27, 0),   # share of websites carrying four flags
    "tree":       (TAB_NB, 65, 0),   # depth-three decision tree
    "curves":     (CNN_NB, 24, 0),   # loss / accuracy / F1 / overfit gap
}

COLUMN_IN = 3.42
TEXT_IN = 7.06


def cell_image(nb_path, cell_index, output_index):
    """Return the raw PNG bytes of one image output of one cell."""
    with open(nb_path, encoding="utf-8") as fh:
        nb = json.load(fh)
    try:
        cell = nb["cells"][cell_index]
    except IndexError:
        sys.exit(f"{os.path.basename(nb_path)}: no cell {cell_index}")
    images = [o for o in cell.get("outputs", []) if "image/png" in o.get("data", {})]
    if len(images) <= output_index:
        sys.exit(f"{os.path.basename(nb_path)} cell {cell_index}: expected an image output")
    src = "".join(cell["source"])[:60].replace("\n", " ")
    print(f"  cell {cell_index:>2}  {src}...")
    return base64.b64decode(images[output_index]["data"]["image/png"])


def write_png(name, raw):
    path = os.path.join(FIGURES, name + ".png")
    with open(path, "wb") as fh:
        fh.write(raw)
    return path


def size(path):
    with Image.open(path) as im:
        return im.size


def stack(paths, out, width_in, gap=0.05, pad=0.03):
    """Lay images out vertically at a fixed printed width, keeping their aspect."""
    heights = [width_in * size(p)[1] / size(p)[0] for p in paths]
    total = sum(heights) + gap * (len(paths) - 1) + 2 * pad
    fig = plt.figure(figsize=(width_in + 2 * pad, total), dpi=320)
    y = pad
    for path, h in zip(paths, heights):
        ax = fig.add_axes([pad / (width_in + 2 * pad), y / total,
                           width_in / (width_in + 2 * pad), h / total])
        ax.imshow(mpimg.imread(path))
        ax.set_axis_off()
        y += h + gap
    fig.savefig(out, dpi=320, facecolor="white")
    plt.close(fig)
    print(f"  wrote {os.path.basename(out)}  {width_in:.2f} x {total:.2f} in")


def main():
    os.makedirs(FIGURES, exist_ok=True)
    print("extracting notebook outputs")
    raw = {}
    for name, (nb, cell, idx) in SOURCES.items():
        raw[name] = write_png("_raw_" + name, cell_image(nb, cell, idx))

    print("composing report figures")
    stack([raw["url_length"], raw["flag_rates"]], os.path.join(FIGURES, "eda_tab.png"), COLUMN_IN)
    stack([raw["tree"]], os.path.join(FIGURES, "tree_d3.png"), TEXT_IN * 0.78)
    stack([raw["curves"]], os.path.join(FIGURES, "cnn_curves.png"), COLUMN_IN * 0.95)

    for name in raw:
        os.remove(raw[name])
    print("figures rebuilt:", sorted(f for f in os.listdir(FIGURES) if f.endswith(".png")))


if __name__ == "__main__":
    main()
