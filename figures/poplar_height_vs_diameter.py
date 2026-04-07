"""
Plot predicted tree heights vs. DBH for the Poplars species group (Group 12).

Sweeps DBH from 5" to 30" and plots three height definitions:
  - Total height (top diameter = 0 in)
  - 4-inch bole height (top diameter = 4 in)
  - 9-inch sawlog height (top diameter = 9 in)

Demonstration tree parameters:
  - Compacted crown ratio: 50%
  - Tree class: preferred
  - Crown class: codominant
"""

import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Allow running the script directly from the figures/ folder
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from westfall_2006 import predict_height_westfall

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
SPECIES_GROUP = 12          # Poplars (Balsam poplar, Bigtooth aspen, Quaking aspen, etc.)
CCR_PCT = 50.0              # Compacted crown ratio (%)
TREE_CLASS = "preferred"
CROWN_CLASS = "codominant"

DBH_MIN = 5.0               # inches
DBH_MAX = 30.0              # inches
N_POINTS = 500

# ---------------------------------------------------------------------------
# Compute heights across the DBH sweep
# ---------------------------------------------------------------------------
dbh = np.linspace(DBH_MIN, DBH_MAX, N_POINTS)

total_ht = predict_height_westfall(SPECIES_GROUP, dbh, CCR_PCT, TREE_CLASS, CROWN_CLASS, top_diam_in=0.0)
bole_4in = predict_height_westfall(SPECIES_GROUP, dbh, CCR_PCT, TREE_CLASS, CROWN_CLASS, top_diam_in=4.0)
sawlog_9in = predict_height_westfall(SPECIES_GROUP, dbh, CCR_PCT, TREE_CLASS, CROWN_CLASS, top_diam_in=9.0)

# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5.5))

ax.plot(dbh, total_ht,  color="#2166ac", linewidth=2.0, label="Total height (top diam. = 0\")")
ax.plot(dbh, bole_4in,  color="#4dac26", linewidth=2.0, linestyle="--", label="4\" bole height (top diam. = 4\")")
ax.plot(dbh, sawlog_9in, color="#d01c8b", linewidth=2.0, linestyle=":",  label="9\" sawlog height (top diam. = 9\")")

# Reference diameter tick lines
for ref_dbh in (10, 15, 20, 25):
    ax.axvline(ref_dbh, color="lightgray", linewidth=0.8, zorder=0)

ax.set_xlabel("Diameter at Breast Height (inches)", fontsize=12)
ax.set_ylabel("Predicted Height (feet)", fontsize=12)
ax.set_title(
    "Height (ft) vs Diameter (in) for a Poplar tree",
    fontsize=13,
    fontweight="bold",
)
ax.text(
    0.5, 1.01,
    f"Species Group 12  |  CCR = {CCR_PCT:.0f}%  |  tree class = {TREE_CLASS}  |  crown class = {CROWN_CLASS}",
    transform=ax.transAxes,
    ha="center", va="bottom",
    fontsize=9, color="#444444",
)

ax.set_xlim(DBH_MIN, DBH_MAX)
ax.set_ylim(0)
ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))
ax.tick_params(axis="both", which="major", labelsize=10)
ax.grid(axis="y", linestyle="--", linewidth=0.6, alpha=0.6)

ax.legend(fontsize=10, loc="upper left", framealpha=0.9)

fig.tight_layout()

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
out_path = Path(__file__).with_suffix(".png")
fig.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"Saved: {out_path}")

plt.show()
