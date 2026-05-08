"""
QCF Uganda — Cluster Construction, Randomization, and Power Calculations

Produces all 10 figures from villages_clean.csv.

SETUP: Set ROOT below to the folder containing raw/, code/, and drafts/.
       Then run: python qcf_analysis.py

Figures produced:
  Figure 1:  All settlements by district (98 km separation)
  Figure 2:  Settlements sized by estimated households
  Figure 3:  Village-level randomization — spillover problem
  Figure 4:  Number of clusters vs. distance threshold
  Figure 5:  Geographic cluster randomization (1 km)
  Figure 6:  Geographic cluster randomization (2 km)
  Figure 7:  Geographic cluster randomization (3 km)
  Figure 8:  Final 22 manual clusters
  Figure 9:  Final randomization into 3 arms
  Figure 10: Power calculations — MDE vs. clusters per arm
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.stats import norm
from pathlib import Path

# =====================================================================
# CONFIGURATION — Change this path to your local project folder
# =====================================================================
ROOT = Path(__file__).resolve().parent.parent
# =====================================================================

RAW = ROOT / "raw"
PLOTS = ROOT / "drafts" / "figures"
PLOTS.mkdir(parents=True, exist_ok=True)

# =====================================================================
# Load data
# =====================================================================
df = pd.read_csv(RAW / "villages_clean.csv")
valid = df.dropna(subset=["lat"]).copy()

DISTRICT_COLORS = {"Amuria": "#E63946", "Bulambuli": "#457B9D"}

# =====================================================================
# FIGURE 1: All settlements by district
# =====================================================================
def figure_1():
    fig, ax = plt.subplots(figsize=(10, 8))
    for district, color in DISTRICT_COLORS.items():
        sub = valid[valid["District"] == district]
        ax.scatter(sub["lon"], sub["lat"], c=color, s=30, alpha=0.7,
                   edgecolors="white", linewidth=0.3, label=district)
    for _, r in valid.iterrows():
        ax.annotate(r["Village"], (r["lon"], r["lat"]), fontsize=4, color="gray",
                    alpha=0.8, xytext=(2, 2), textcoords="offset points")
    mid_lon = (valid[valid["District"] == "Amuria"]["lon"].max() +
               valid[valid["District"] == "Bulambuli"]["lon"].min()) / 2
    mid_lat = (valid["lat"].min() + valid["lat"].max()) / 2
    ax.annotate("~98 km apart", (mid_lon, mid_lat), fontsize=11, color="#555555",
                ha="center", fontstyle="italic")
    ax.set_xlabel("Longitude"); ax.set_ylabel("Latitude")
    ax.set_title(f"All Villages by District (n={len(valid)})", fontsize=13, fontweight="bold")
    ax.legend(fontsize=10); ax.set_aspect("equal"); ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOTS / "figure_1.png", dpi=150, bbox_inches="tight"); plt.close()

# =====================================================================
# FIGURE 2: Settlements sized by estimated households
# =====================================================================
def figure_2():
    sub = valid.dropna(subset=["est_hh_per_village"])
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6), gridspec_kw={"width_ratios": [1, 1.3], "wspace": 0.15})
    for district, ax, title in [("Amuria", ax1, "Amuria (drought)"), ("Bulambuli", ax2, "Bulambuli (flooding)")]:
        d = sub[sub["District"] == district]
        sc = ax.scatter(d["lon"], d["lat"], s=d["est_hh_per_village"] * 1.5,
                        c=d["est_hh_per_village"], cmap="YlOrRd", alpha=0.8,
                        edgecolors="black", linewidth=0.5, vmin=0, vmax=250)
        lbl_color = "white" if district == "Amuria" else "gray"
        for _, r in d.iterrows():
            ax.annotate(f'{r["est_hh_per_village"]:.0f}', (r["lon"], r["lat"]),
                        fontsize=5, color=lbl_color, ha="center", va="bottom",
                        xytext=(0, 5), textcoords="offset points")
        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.set_xlabel("Longitude"); ax.set_ylabel("Latitude")
        ax.set_aspect("equal"); ax.grid(True, alpha=0.3)
    fig.suptitle("Village Locations Sized by Estimated Households", fontsize=13, fontweight="bold")
    fig.subplots_adjust(bottom=0.15)
    cbar_ax = fig.add_axes([0.3, 0.05, 0.4, 0.02])
    fig.colorbar(sc, cax=cbar_ax, orientation="horizontal").set_label("Estimated HH per village", fontsize=10)
    fig.savefig(PLOTS / "figure_2.png", dpi=150, bbox_inches="tight"); plt.close()

# =====================================================================
# Helper: plot a randomization assignment
# =====================================================================
GROUP_COLORS = {1: "#2196F3", 2: "#FF9800", 3: "#4CAF50"}
GROUP_LABELS = {1: "G1: Standard early", 2: "G2: Adaptation+plus", 3: "G3: Standard delayed"}

def _plot_randomization(data, group_col, title_str, filename):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    for district, ax, title in [("Amuria", ax1, "Amuria (drought)"), ("Bulambuli", ax2, "Bulambuli (flooding)")]:
        sub = data[data["District"] == district]
        for g in [1, 2, 3]:
            gsub = sub[sub[group_col] == g]
            if len(gsub) == 0: continue
            ax.scatter(gsub["lon"], gsub["lat"], s=gsub["est_hh_per_village"] * 1.2,
                       c=GROUP_COLORS[g], alpha=0.7, edgecolors="black", linewidth=0.5,
                       label=GROUP_LABELS[g])
        for _, r in sub.iterrows():
            ax.annotate(f'{r["est_hh_per_village"]:.0f}', (r["lon"], r["lat"]),
                        fontsize=5, color="gray", ha="center", va="bottom",
                        xytext=(0, 5), textcoords="offset points")
        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.set_xlabel("Longitude"); ax.set_ylabel("Latitude")
        ax.legend(fontsize=7, loc="lower left"); ax.set_aspect("equal"); ax.grid(True, alpha=0.3)
    fig.suptitle(title_str, fontsize=12, fontweight="bold")
    fig.tight_layout()
    fig.savefig(PLOTS / filename, dpi=150, bbox_inches="tight"); plt.close()

def _assign_village_level(data):
    data = data.copy()
    np.random.seed(42)
    for district in data["District"].unique():
        mask = data["District"] == district
        n = mask.sum()
        ratio = np.array([2, 1, 2])
        counts = (ratio / ratio.sum() * n).astype(int)
        counts[-1] = n - counts[:-1].sum()
        a = np.concatenate([np.full(c, g + 1) for g, c in enumerate(counts)])
        np.random.shuffle(a)
        data.loc[mask, "group"] = a
    data["group"] = data["group"].astype(int)
    return data

def _assign_geo_cluster(data, threshold_km):
    data = data.copy()
    np.random.seed(42)
    coords_km = data[["lat", "lon"]].values * 111
    Z = linkage(coords_km, method="complete")
    data["geo_cluster"] = fcluster(Z, t=threshold_km, criterion="distance")
    for district in data["District"].unique():
        mask = data["District"] == district
        clusters = data.loc[mask, "geo_cluster"].unique()
        n_c = len(clusters)
        ratio = np.array([2, 1, 2])
        counts = (ratio / ratio.sum() * n_c).astype(int)
        counts[-1] = n_c - counts[:-1].sum()
        a = np.concatenate([np.full(c, g + 1) for g, c in enumerate(counts)])
        np.random.shuffle(a)
        data.loc[mask, "group"] = data.loc[mask, "geo_cluster"].map(dict(zip(clusters, a)))
    data["group"] = data["group"].astype(int)
    return data

# =====================================================================
# FIGURE 3: Village-level randomization (spillover problem)
# =====================================================================
def figure_3():
    data = _assign_village_level(valid)
    _plot_randomization(data, "group",
        "Village-Level Randomization (2:1:2, seed=42)\n"
        "Dot size = estimated HH — Note neighboring settlements in different arms",
        "figure_3.png")

# =====================================================================
# FIGURE 4: Clusters by distance threshold
# =====================================================================
def figure_4():
    coords_km = valid[["lat", "lon"]].values * 111
    Z = linkage(coords_km, method="complete")
    thresholds = np.arange(0.5, 15.5, 0.5)
    counts = {"All": [], "Amuria": [], "Bulambuli": []}
    for t in thresholds:
        labels = fcluster(Z, t=t, criterion="distance")
        valid["_cl"] = labels
        counts["All"].append(valid["_cl"].nunique())
        counts["Amuria"].append(valid[valid["District"] == "Amuria"]["_cl"].nunique())
        counts["Bulambuli"].append(valid[valid["District"] == "Bulambuli"]["_cl"].nunique())
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(thresholds, counts["All"], "k-o", ms=4, label="All", linewidth=2)
    ax.plot(thresholds, counts["Amuria"], "--s", color="#E63946", ms=4, label="Amuria")
    ax.plot(thresholds, counts["Bulambuli"], "--^", color="#457B9D", ms=4, label="Bulambuli")
    ax.set_xlabel("Distance threshold (km)", fontsize=11)
    ax.set_ylabel("Number of clusters", fontsize=11)
    ax.set_title("Number of Geographic Clusters by Distance Threshold", fontsize=13, fontweight="bold")
    ax.legend(fontsize=10); ax.grid(True, alpha=0.3); ax.set_xticks(range(0, 16))
    fig.tight_layout()
    fig.savefig(PLOTS / "figure_4.png", dpi=150, bbox_inches="tight"); plt.close()

# =====================================================================
# FIGURES 5-7: Geographic cluster randomization at 1, 2, 3 km
# =====================================================================
def figure_5():
    data = _assign_geo_cluster(valid, 1.0)
    n_a = data[data["District"] == "Amuria"]["geo_cluster"].nunique()
    n_b = data[data["District"] == "Bulambuli"]["geo_cluster"].nunique()
    _plot_randomization(data, "group",
        f"Geographic Cluster Randomization (1 km threshold, seed=42)\n"
        f"Amuria: {n_a} clusters — Bulambuli: {n_b} clusters — {n_a+n_b} total units",
        "figure_5.png")

def figure_6():
    data = _assign_geo_cluster(valid, 2.0)
    n_a = data[data["District"] == "Amuria"]["geo_cluster"].nunique()
    n_b = data[data["District"] == "Bulambuli"]["geo_cluster"].nunique()
    _plot_randomization(data, "group",
        f"Geographic Cluster Randomization (2 km threshold, seed=42)\n"
        f"Amuria: {n_a} clusters — Bulambuli: {n_b} clusters — {n_a+n_b} total units",
        "figure_6.png")

def figure_7():
    data = _assign_geo_cluster(valid, 3.0)
    n_a = data[data["District"] == "Amuria"]["geo_cluster"].nunique()
    n_b = data[data["District"] == "Bulambuli"]["geo_cluster"].nunique()
    _plot_randomization(data, "group",
        f"Geographic Cluster Randomization (3 km threshold, seed=42)\n"
        f"Amuria: {n_a} clusters — Bulambuli: {n_b} clusters — {n_a+n_b} total units",
        "figure_7.png")

# =====================================================================
# FIGURE 8: Final 22 manual clusters
# =====================================================================
def build_manual_clusters(data):
    """Build 22 manual clusters from 3km base + Amuria splits + Bulambuli C6 split."""
    data = data.copy()
    coords_km = data[["lat", "lon"]].values * 111
    Z = linkage(coords_km, method="complete")
    data["manual_cluster"] = fcluster(Z, t=3.0, criterion="distance").astype(str)
    am = data["District"] == "Amuria"
    bul = data["District"] == "Bulambuli"
    # Amuria splits
    data.loc[am & (data["Village"] == "AKAMURIEI"), "manual_cluster"] = "9a"
    data.loc[am & (data["Village"] == "OPADOI"), "manual_cluster"] = "9b"
    data.loc[am & (data["Village"].isin(["AARATOM", "OGWETE"])), "manual_cluster"] = "10a"
    data.loc[am & (data["Village"].isin(["KATINE", "ASILANG"])), "manual_cluster"] = "10b"
    data.loc[am & (data["Village"] == "NAIKURO"), "manual_cluster"] = "12a"
    data.loc[am & (data["Village"] == "OMODOI"), "manual_cluster"] = "12b"
    data.loc[am & (data["Village"] == "ONGUTOI"), "manual_cluster"] = "16a"
    data.loc[am & (data["Village"] == "AKERIAU"), "manual_cluster"] = "16b"
    # Bulambuli C6 split
    data.loc[bul & (data["Village"].isin(["KISIYOPO", "BIRINDA"])), "manual_cluster"] = "6a"
    data.loc[bul & (data["Village"].isin(["MABONO", "MADUWA", "MASEJESE"])), "manual_cluster"] = "6b"
    # Renumber 1-22
    am_clusters = sorted(data.loc[am, "manual_cluster"].unique(), key=lambda x: (len(x), x))
    bul_clusters = sorted(data.loc[bul, "manual_cluster"].unique(), key=lambda x: (len(x), x))
    rename = {}
    for i, c in enumerate(am_clusters, 1): rename[c] = str(i)
    for i, c in enumerate(bul_clusters, len(am_clusters) + 1): rename[c] = str(i)
    data["cluster"] = data["manual_cluster"].map(rename)
    return data

def figure_8():
    data = build_manual_clusters(valid)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    for district, ax, title in [("Amuria", ax1, "Amuria (drought)"), ("Bulambuli", ax2, "Bulambuli (flooding)")]:
        sub = data[data["District"] == district]
        clusters = sorted(sub["cluster"].unique(), key=lambda x: int(x))
        n_c = len(clusters)
        cmap = plt.get_cmap("tab20", 22)
        for cl in clusters:
            csub = sub[sub["cluster"] == cl]
            ax.scatter(csub["lon"], csub["lat"], s=csub["est_hh_per_village"] * 1.2,
                       c=[cmap(int(cl) - 1)], alpha=0.8, edgecolors="black", linewidth=0.5,
                       label=f"{cl} ({len(csub)}v)")
        for _, r in sub.iterrows():
            ax.annotate(r["cluster"], (r["lon"], r["lat"]), fontsize=6, color="black",
                        ha="center", va="bottom", xytext=(0, 5), textcoords="offset points",
                        fontweight="bold")
        ax.set_title(f"{title}\n{n_c} clusters", fontsize=12, fontweight="bold")
        ax.set_xlabel("Longitude"); ax.set_ylabel("Latitude")
        ax.legend(fontsize=6, loc="lower left", ncol=2, title="Cluster")
        ax.set_aspect("equal"); ax.grid(True, alpha=0.3)
    fig.suptitle("Randomization Clusters (22 total)\n13 Amuria + 9 Bulambuli",
                 fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(PLOTS / "figure_8.png", dpi=150, bbox_inches="tight"); plt.close()

# =====================================================================
# FIGURE 9: Final randomization into 3 arms
# =====================================================================
def figure_9():
    data = build_manual_clusters(valid)
    np.random.seed(2026)
    for district in data["District"].unique():
        mask = data["District"] == district
        clusters = sorted(data.loc[mask, "cluster"].unique(), key=lambda x: int(x))
        n_c = len(clusters)
        ratio = np.array([2, 1, 2])
        counts = (ratio / ratio.sum() * n_c).astype(int)
        counts[-1] = n_c - counts[:-1].sum()
        a = np.concatenate([np.full(c, g + 1) for g, c in enumerate(counts)])
        np.random.shuffle(a)
        data.loc[mask, "arm"] = data.loc[mask, "cluster"].map(dict(zip(clusters, a)))
    data["arm"] = data["arm"].astype(int)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    for district, ax, title in [("Amuria", ax1, "Amuria (drought)"), ("Bulambuli", ax2, "Bulambuli (flooding)")]:
        sub = data[data["District"] == district]
        for g in [1, 2, 3]:
            gsub = sub[sub["arm"] == g]
            if len(gsub) == 0: continue
            ax.scatter(gsub["lon"], gsub["lat"], s=gsub["est_hh_per_village"] * 1.2,
                       c=GROUP_COLORS[g], alpha=0.7, edgecolors="black", linewidth=0.5,
                       label=GROUP_LABELS[g])
        for _, r in sub.iterrows():
            ax.annotate(str(int(r["arm"])), (r["lon"], r["lat"]), fontsize=5, color="black",
                        ha="center", va="bottom", xytext=(0, 5), textcoords="offset points",
                        fontweight="bold")
        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.set_xlabel("Longitude"); ax.set_ylabel("Latitude")
        ax.legend(fontsize=8, loc="lower left"); ax.set_aspect("equal"); ax.grid(True, alpha=0.3)
    fig.suptitle("Cluster Randomization into 3 Arms (2:1:2, seed=2026)\n22 clusters — stratified by district",
                 fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(PLOTS / "figure_9.png", dpi=150, bbox_inches="tight"); plt.close()

# =====================================================================
# FIGURE 10: Power calculations — MDE vs clusters
# =====================================================================
ALPHA = 0.05
POWER = 0.80
RHO_PANEL = 0.5
SD_CONTINUOUS = 112500
P_BINARY = 0.20
N_AMURIA = 16; N_BULAMBULI = 118
HH_AMURIA = 222; HH_BULAMBULI = 29; SURVEY_RATE = 0.30
M_AMURIA = round(HH_AMURIA * SURVEY_RATE)
M_BULAMBULI = round(HH_BULAMBULI * SURVEY_RATE)
M_WEIGHTED = (N_AMURIA / (N_AMURIA + N_BULAMBULI)) * M_AMURIA + \
             (N_BULAMBULI / (N_AMURIA + N_BULAMBULI)) * M_BULAMBULI
ICC_VALS = {"Low (0.05)": 0.05, "Medium (0.10)": 0.10, "High (0.15)": 0.15}

def mde_continuous(k, m, icc, sd, rho):
    z_a, z_b = norm.ppf(1 - ALPHA / 2), norm.ppf(POWER)
    deff = 1 + (m - 1) * icc
    return (z_a + z_b) * np.sqrt(2 * sd**2 * (1 - rho**2) * deff / (k * m))

def mde_binary(k, m, icc, p0, rho):
    return mde_continuous(k, m, icc, np.sqrt(p0 * (1 - p0)), rho)

def figure_10():
    k_range = np.arange(10, 80, 1)
    ref_shared = {
        "Egger et al. 2022 (Kenya GE)": {"sd": 0.36, "pp": 8},
        "GD Malawi Nsanje (2025)":       {"sd": 0.25, "pp": 18},
        "Labeling effects (Thomas 2020)":{"sd": 0.15, "pp": 4},
    }
    ref_sd_only = {"Haushofer & Shapiro 2016 (Kenya)": 0.52}

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Left: continuous
    ax = axes[0]
    for label, icc in ICC_VALS.items():
        mdes = [mde_continuous(k, M_WEIGHTED, icc, SD_CONTINUOUS, RHO_PANEL) / SD_CONTINUOUS for k in k_range]
        ax.plot(k_range, mdes, label=f"ICC = {icc}", linewidth=2)
    ax.axvspan(54, 58, alpha=0.15, color="gray", label="Village-level (56)")
    ax.axvspan(8, 10, alpha=0.15, color="blue", label="Cluster design (9)")
    for name, vals in ref_shared.items():
        ax.axhline(y=vals["sd"], color="red", linestyle=":", alpha=0.5, linewidth=1)
        ax.text(80.5, vals["sd"], name, fontsize=6.5, va="center", color="red", alpha=0.8)
    for name, val in ref_sd_only.items():
        ax.axhline(y=val, color="red", linestyle=":", alpha=0.5, linewidth=1)
        ax.text(80.5, val, name, fontsize=6.5, va="center", color="red", alpha=0.8)
    ax.set_xlabel("Villages per arm"); ax.set_ylabel("MDE (in SD units)")
    ax.set_title("Q1: Livelihood Investment ($)\nCluster-randomized", fontsize=12, fontweight="bold")
    ax.legend(fontsize=8, loc="upper right"); ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 0.8); ax.set_xlim(10, 80)

    # Right: binary
    ax = axes[1]
    for label, icc in ICC_VALS.items():
        mdes = [mde_binary(k, M_WEIGHTED, icc, P_BINARY, RHO_PANEL) * 100 for k in k_range]
        ax.plot(k_range, mdes, label=f"ICC = {icc}", linewidth=2)
    ax.axvspan(54, 58, alpha=0.15, color="gray", label="Village-level (56)")
    ax.axvspan(8, 10, alpha=0.15, color="blue", label="Cluster design (9)")
    for name, vals in ref_shared.items():
        ax.axhline(y=vals["pp"], color="red", linestyle=":", alpha=0.5, linewidth=1)
        ax.text(80.5, vals["pp"], name, fontsize=6.5, va="center", color="red", alpha=0.8)
    ax.set_xlabel("Villages per arm"); ax.set_ylabel("MDE (percentage points)")
    ax.set_title("Q1: Income Diversification (%)\nCluster-randomized", fontsize=12, fontweight="bold")
    ax.legend(fontsize=8, loc="upper right"); ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 30); ax.set_xlim(10, 80)

    fig.suptitle(f"Minimum Detectable Effect vs. Number of Clusters per Arm\n"
                 f"(\u03b1=0.05, power=0.80, panel \u03c1={RHO_PANEL}, avg {M_WEIGHTED:.0f} HH surveyed/village)",
                 fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(PLOTS / "figure_10.png", dpi=150, bbox_inches="tight"); plt.close()

# =====================================================================
# Run all
# =====================================================================
if __name__ == "__main__":
    print("Generating figures from villages_clean.csv...")
    for i in range(1, 11):
        print(f"  Figure {i}...", end=" ")
        globals()[f"figure_{i}"]()
        print("done")
    print(f"\nAll figures saved to {PLOTS}/")
