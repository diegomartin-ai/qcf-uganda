"""
1km geographic clusters: cluster map + stratified randomization by district.
Produces two figures:
  1. geo_clusters_1km_39.png  — clusters colored by ID
  2. randomization_1km_39.png — clusters colored by treatment arm
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import fcluster, linkage
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
PROCESS = ROOT / "data" / "process"
OUT = ROOT / "plots" / "randomization"
PROCESS.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

SEED = 2026
ARM_LABELS = {1: "G1: Standard early", 2: "G2: Adaptation+plus", 3: "G3: Standard delayed"}
ARM_COLORS = {1: "#5DA5DA", 2: "#FAA43A", 3: "#60BD68"}

# --- Data and clustering ---
df = pd.read_csv(RAW / "villages_with_clusters.csv")
valid = df.dropna(subset=["lat"]).copy()

coords_km = valid[["lat", "lon"]].values * 111
Z = linkage(coords_km, method="complete")
valid["cluster_1km"] = fcluster(Z, t=1.0, criterion="distance")

# Renumber clusters per district
for district in ["Amuria", "Bulambuli"]:
    mask = valid["District"] == district
    old_ids = sorted(valid.loc[mask, "cluster_1km"].unique())
    mapping = {old: i + 1 for i, old in enumerate(old_ids)}
    valid.loc[mask, "cluster_label"] = valid.loc[mask, "cluster_1km"].map(mapping).astype(int)

# --- Dot sizing based on est_hh_per_village ---
hh_min = valid["est_hh_per_village"].min()
hh_max = valid["est_hh_per_village"].max()
SIZE_MIN, SIZE_MAX = 40, 350
valid["dot_size"] = (
    SIZE_MIN + (valid["est_hh_per_village"] - hh_min) / (hh_max - hh_min) * (SIZE_MAX - SIZE_MIN)
)

# --- Randomization: stratified by district, balanced across 3 arms ---
rng = np.random.default_rng(SEED)
cluster_df = valid.groupby(["District", "cluster_1km"]).first().reset_index()[
    ["District", "cluster_1km"]
]

arm_map = {}
for district in ["Amuria", "Bulambuli"]:
    clusters = cluster_df[cluster_df.District == district]["cluster_1km"].values
    rng.shuffle(clusters)
    n = len(clusters)
    # 2:1:2 ratio — minimize G2 to maximize Q1 power (G1 vs G3)
    n2 = n // 5                # G2 gets floor(n/5)
    n1 = (n - n2 + 1) // 2    # G1 gets half of remainder (rounded up)
    n3 = n - n1 - n2           # G3 gets the rest
    arms = [1]*n1 + [2]*n2 + [3]*n3
    for c, a in zip(clusters, arms):
        arm_map[c] = a

valid["arm"] = valid["cluster_1km"].map(arm_map)

# Print summary
print("=== Randomization summary (stratified by district) ===")
for district in ["Amuria", "Bulambuli"]:
    sub = valid[valid.District == district]
    print(f"\n{district}:")
    for arm in [1, 2, 3]:
        asub = sub[sub.arm == arm]
        n_c = asub.cluster_1km.nunique()
        n_v = len(asub)
        print(f"  {ARM_LABELS[arm]}: {n_c} clusters, {n_v} villages")
print(f"\nTotal: {valid.cluster_1km.nunique()} clusters, {len(valid)} villages")

# --- Export randomized data to process/ ---
export = valid[["District", "Sub county", "Parish", "Village", "lat", "lon",
                "parish_total_hhs", "parish_total_pop", "est_hh_per_village",
                "cluster_1km", "cluster_label", "arm"]].copy()
export = export.rename(columns={"cluster_1km": "cluster_id", "cluster_label": "cluster_label_district"})
export["arm_label"] = export["arm"].map(ARM_LABELS)
export["group"] = export["arm"].map({1: "G1", 2: "G2", 3: "G3"})
export["baseline_month"] = ""
export["note"] = ""

# Append missing-GPS villages so programs team can see the full list
missing = df[df["lat"].isna()].copy()
missing = missing[["District", "Sub county", "Parish", "Village", "lat", "lon",
                    "parish_total_hhs", "parish_total_pop", "est_hh_per_village"]].copy()
for col in ["cluster_id", "cluster_label_district", "arm", "arm_label", "group", "baseline_month"]:
    missing[col] = ""
missing["note"] = "Programs getting the latitude and longitude"
export = pd.concat([export, missing], ignore_index=True)

export_path = PROCESS / "villages_randomized.csv"
export.to_csv(export_path, index=False)
n_valid = export["note"].eq("").sum()
n_tbd = export["note"].ne("").sum()
print(f"Exported: {export_path} ({n_valid} randomized + {n_tbd} TBD = {len(export)} total)")


# =====================================================================
# FIGURE 1: Clusters colored by cluster ID
# =====================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

for ax, district, hazard in [(ax1, "Amuria", "drought"), (ax2, "Bulambuli", "flooding")]:
    sub = valid[valid["District"] == district].copy()
    clusters = sorted(sub["cluster_label"].unique())
    n_clusters = len(clusters)
    cmap = plt.colormaps.get_cmap("tab20" if n_clusters <= 20 else "gist_ncar")

    handles = []
    for i, c in enumerate(clusters):
        csub = sub[sub["cluster_label"] == c]
        n_v = len(csub)
        color = cmap(i % 20 / 20) if n_clusters <= 20 else cmap(i / n_clusters)
        ax.scatter(
            csub["lon"], csub["lat"], c=[color], s=csub["dot_size"],
            alpha=0.7, edgecolors="white", linewidth=0.5, zorder=3,
        )
        for _, row in csub.iterrows():
            ax.annotate(
                f"C{int(c)}", (row["lon"], row["lat"]),
                fontsize=6, ha="center", va="bottom",
                xytext=(0, 5), textcoords="offset points",
            )
        handles.append(
            ax.scatter([], [], c=[color], s=60, label=f"C{int(c)} ({n_v}v)",
                       edgecolors="white", linewidth=0.5)
        )
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title(f"{district} ({hazard})\n{n_clusters} clusters", fontsize=13, fontweight="bold")
    ax.legend(handles=handles, loc="lower left", fontsize=7, ncol=2, framealpha=0.9, markerscale=0.8)
    ax.grid(True, alpha=0.3)

n_am = valid[valid.District == "Amuria"]["cluster_label"].nunique()
n_bul = valid[valid.District == "Bulambuli"]["cluster_label"].nunique()
fig.suptitle(
    f"Geographic Cluster Assignment (1 km threshold)\n"
    f"{n_am + n_bul} clusters total — {n_am} Amuria, {n_bul} Bulambuli\n"
    f"Dot size ∝ est. households/village ({hh_min:.0f}–{hh_max:.0f})",
    fontsize=14, fontweight="bold",
)
plt.tight_layout()
p1 = OUT / "geo_clusters_1km_39.png"
plt.savefig(p1, dpi=150, bbox_inches="tight")
print(f"Saved: {p1}")


# =====================================================================
# FIGURE 2: Clusters colored by treatment arm
# =====================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

for ax, district, hazard in [(ax1, "Amuria", "drought"), (ax2, "Bulambuli", "flooding")]:
    sub = valid[valid["District"] == district].copy()

    for arm in [1, 2, 3]:
        asub = sub[sub.arm == arm]
        ax.scatter(
            asub["lon"], asub["lat"], c=ARM_COLORS[arm], s=asub["dot_size"],
            alpha=0.7, edgecolors="white", linewidth=0.5, zorder=3,
            label=f"{ARM_LABELS[arm]} ({asub.cluster_1km.nunique()}c, {len(asub)}v)",
        )
    # Label with cluster ID
    for _, row in sub.iterrows():
        ax.annotate(
            f"C{int(row['cluster_label'])}", (row["lon"], row["lat"]),
            fontsize=6, ha="center", va="bottom",
            xytext=(0, 5), textcoords="offset points",
        )
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    n_clusters = sub.cluster_label.nunique()
    ax.set_title(f"{district} ({hazard})\n{n_clusters} clusters", fontsize=13, fontweight="bold")
    ax.legend(loc="lower left", fontsize=8, framealpha=0.9)
    ax.grid(True, alpha=0.3)

fig.suptitle(
    f"Stratified Randomization (1 km clusters, seed={SEED})\n"
    f"Stratification variable: District — {n_am + n_bul} clusters → 3 arms\n"
    f"Dot size ∝ est. households/village ({hh_min:.0f}–{hh_max:.0f})",
    fontsize=14, fontweight="bold",
)
plt.tight_layout()
p2 = OUT / "randomization_1km_39.png"
plt.savefig(p2, dpi=150, bbox_inches="tight")
print(f"Saved: {p2}")
