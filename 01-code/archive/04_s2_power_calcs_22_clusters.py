"""
Power calculations for QCF Uganda — Cash for Climate Adaptation

Q1: Cash effect — cluster-randomized at village level (Group 1 vs Group 3)
Q2: Plus effect — individual-randomized at household level within Group 2
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLOTS = ROOT / "plots" / "randomization"
PLOTS.mkdir(parents=True, exist_ok=True)

# --- Parameters ---
ALPHA = 0.05
POWER = 0.80
z_alpha = norm.ppf(1 - ALPHA / 2)
z_beta = norm.ppf(POWER)

# Village sizes (estimated HH per village, from UBOS 2024)
HH_AMURIA = 222
HH_BULAMBULI = 29
SURVEY_RATE = 0.30
M_AMURIA = round(HH_AMURIA * SURVEY_RATE)   # ~67
M_BULAMBULI = round(HH_BULAMBULI * SURVEY_RATE)  # ~9

# Baseline-endline correlation (panel design)
RHO_PANEL = 0.5  # central case

# Outcome parameters
SD_CONTINUOUS = 112500  # UGX, livelihood investment
MEAN_CONTINUOUS = 75000  # UGX
P_BINARY = 0.20  # baseline diversification rate

# ICC scenarios
ICC_LIVELIHOOD = {"Low (0.05)": 0.05, "Medium (0.10)": 0.10, "High (0.15)": 0.15}
ICC_DIVERSIFICATION = {"Low (0.05)": 0.05, "Medium (0.10)": 0.10, "High (0.15)": 0.15}


def mde_continuous_cluster(k_per_arm, m, icc, sd, rho_panel, alpha=ALPHA, power=POWER):
    """MDE for continuous outcome in a cluster-randomized design with baseline control (ANCOVA)."""
    z_a = norm.ppf(1 - alpha / 2)
    z_b = norm.ppf(power)
    deff = 1 + (m - 1) * icc
    variance_reduction = 1 - rho_panel ** 2  # ANCOVA gain from panel
    var_per_arm = sd ** 2 * variance_reduction * deff / (k_per_arm * m)
    se = np.sqrt(2 * var_per_arm)
    return (z_a + z_b) * se


def mde_binary_cluster(k_per_arm, m, icc, p0, rho_panel, alpha=ALPHA, power=POWER):
    """MDE for binary outcome in a cluster-randomized design with baseline control."""
    sd = np.sqrt(p0 * (1 - p0))
    return mde_continuous_cluster(k_per_arm, m, icc, sd, rho_panel, alpha, power)


def mde_continuous_individual(n_per_arm, sd, rho_panel, alpha=ALPHA, power=POWER):
    """MDE for continuous outcome in an individual-randomized design with baseline control."""
    z_a = norm.ppf(1 - alpha / 2)
    z_b = norm.ppf(power)
    variance_reduction = 1 - rho_panel ** 2
    se = np.sqrt(2 * sd ** 2 * variance_reduction / n_per_arm)
    return (z_a + z_b) * se


def mde_binary_individual(n_per_arm, p0, rho_panel, alpha=ALPHA, power=POWER):
    """MDE for binary outcome in an individual-randomized design with baseline control."""
    sd = np.sqrt(p0 * (1 - p0))
    return mde_continuous_individual(n_per_arm, sd, rho_panel, alpha, power)


# --- Weighted average m across districts ---
# 16 Amuria + 118 Bulambuli = 134 villages
# In each arm (2:1:2 ratio), roughly same district proportions
N_AMURIA = 16
N_BULAMBULI = 118
FRAC_AMURIA = N_AMURIA / (N_AMURIA + N_BULAMBULI)
FRAC_BULAMBULI = N_BULAMBULI / (N_AMURIA + N_BULAMBULI)
M_WEIGHTED = FRAC_AMURIA * M_AMURIA + FRAC_BULAMBULI * M_BULAMBULI


# --- Plot: MDE vs number of clusters per arm (Q1) ---
def plot_mde_vs_clusters():
    k_range = np.arange(10, 80, 1)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Reference effects from literature — shared studies use consistent labels
    ref_shared = {
        "Egger et al. 2022 (Kenya GE)":    {"sd": 0.36, "pp": 8},
        "GD Malawi Nsanje (2025)":          {"sd": 0.25, "pp": 18},
        "Labeling effects (Thomas 2020)":   {"sd": 0.15, "pp": 4},
    }
    # Additional refs per panel
    ref_sd_only = {
        "Haushofer & Shapiro 2016 (Kenya)": 0.52,
    }

    # Continuous outcome
    ax = axes[0]
    for label, icc in ICC_LIVELIHOOD.items():
        mdes = [mde_continuous_cluster(k, M_WEIGHTED, icc, SD_CONTINUOUS, RHO_PANEL) for k in k_range]
        mdes_sd = [m / SD_CONTINUOUS for m in mdes]
        ax.plot(k_range, mdes_sd, label=f"ICC = {icc}", linewidth=2)
    ax.axvspan(54, 58, alpha=0.15, color="gray", label="Village-level (56)")
    ax.axvspan(8, 10, alpha=0.15, color="blue", label="Cluster design (9)")
    for name, vals in ref_shared.items():
        ax.axhline(y=vals["sd"], color="red", linestyle=":", alpha=0.5, linewidth=1)
        ax.text(80.5, vals["sd"], name, fontsize=6.5, va="center", color="red", alpha=0.8)
    for name, val in ref_sd_only.items():
        ax.axhline(y=val, color="red", linestyle=":", alpha=0.5, linewidth=1)
        ax.text(80.5, val, name, fontsize=6.5, va="center", color="red", alpha=0.8)
    ax.set_xlabel("Villages per arm", fontsize=11)
    ax.set_ylabel("MDE (in SD units)", fontsize=11)
    ax.set_title("Q1: Livelihood Investment ($)\nCluster-randomized", fontsize=12, fontweight="bold")
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 0.8)
    ax.set_xlim(10, 80)

    # Binary outcome
    ax = axes[1]
    for label, icc in ICC_DIVERSIFICATION.items():
        mdes = [mde_binary_cluster(k, M_WEIGHTED, icc, P_BINARY, RHO_PANEL) for k in k_range]
        mdes_pp = [m * 100 for m in mdes]
        ax.plot(k_range, mdes_pp, label=f"ICC = {icc}", linewidth=2)
    ax.axvspan(54, 58, alpha=0.15, color="gray", label="Village-level (56)")
    ax.axvspan(8, 10, alpha=0.15, color="blue", label="Cluster design (9)")
    for name, vals in ref_shared.items():
        ax.axhline(y=vals["pp"], color="red", linestyle=":", alpha=0.5, linewidth=1)
        ax.text(80.5, vals["pp"], name, fontsize=6.5, va="center", color="red", alpha=0.8)
    ax.set_xlabel("Villages per arm", fontsize=11)
    ax.set_ylabel("MDE (percentage points)", fontsize=11)
    ax.set_title("Q1: Income Diversification (%)\nCluster-randomized", fontsize=12, fontweight="bold")
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 30)
    ax.set_xlim(10, 80)

    fig.suptitle(
        f"Minimum Detectable Effect vs. Number of Clusters per Arm\n"
        f"(α=0.05, power=0.80, panel ρ={RHO_PANEL}, avg {M_WEIGHTED:.0f} HH surveyed/village)",
        fontsize=13, fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(PLOTS / "power_mde_vs_clusters.png", dpi=150, bbox_inches="tight")
    print("Saved power_mde_vs_clusters.png")
    plt.close()


# --- Print summary table ---
def print_power_summary():
    k_q1 = 56  # villages per arm for Q1

    print("=" * 70)
    print("Q1: CASH EFFECT — Cluster-randomized (56 villages per arm)")
    print(f"  Weighted avg HH surveyed/village: {M_WEIGHTED:.0f}")
    print(f"  Panel baseline correlation: {RHO_PANEL}")
    print("=" * 70)

    print("\n  Continuous: Livelihood Investment (SD = {:.0f} UGX)".format(SD_CONTINUOUS))
    for label, icc in ICC_LIVELIHOOD.items():
        mde = mde_continuous_cluster(k_q1, M_WEIGHTED, icc, SD_CONTINUOUS, RHO_PANEL)
        mde_sd = mde / SD_CONTINUOUS
        print(f"    {label}: MDE = {mde:,.0f} UGX ({mde_sd:.2f} SD, ~${mde/3750:.0f} USD)")

    print(f"\n  Binary: Income Diversification (baseline = {P_BINARY:.0%})")
    for label, icc in ICC_DIVERSIFICATION.items():
        mde = mde_binary_cluster(k_q1, M_WEIGHTED, icc, P_BINARY, RHO_PANEL)
        print(f"    {label}: MDE = {mde*100:.1f} pp")

    # Q2: Individual-randomized within Group 2
    # Group 2 has ~28 villages. Each HH randomized to 3 sub-arms (1/3 each)
    # Total HH in Group 2: 28 villages × weighted avg HH × survey rate
    n_villages_g2 = 28
    total_hh_g2_surveyed = round(n_villages_g2 * M_WEIGHTED)
    n_per_subarm = round(total_hh_g2_surveyed / 3)

    print("\n" + "=" * 70)
    print(f"Q2: PLUS EFFECT — Individual-randomized ({n_villages_g2} villages)")
    print(f"  Total HH surveyed in Group 2: ~{total_hh_g2_surveyed}")
    print(f"  HH per sub-arm (1/3 each): ~{n_per_subarm}")
    print("=" * 70)

    print("\n  Continuous: Livelihood Investment")
    mde = mde_continuous_individual(n_per_subarm, SD_CONTINUOUS, RHO_PANEL)
    print(f"    MDE = {mde:,.0f} UGX ({mde/SD_CONTINUOUS:.2f} SD, ~${mde/3750:.0f} USD)")

    print(f"\n  Binary: Income Diversification (baseline = {P_BINARY:.0%})")
    mde = mde_binary_individual(n_per_subarm, P_BINARY, RHO_PANEL)
    print(f"    MDE = {mde*100:.1f} pp")


def _plot_randomization(df, group_col, title_str, filename):
    """Helper to plot a randomization assignment."""
    group_colors = {1: "#2196F3", 2: "#FF9800", 3: "#4CAF50"}
    group_labels = {1: "G1: Standard early", 2: "G2: Adaptation+plus", 3: "G3: Standard delayed"}

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    for district, ax, title in [
        ("Amuria", ax1, "Amuria (drought)"),
        ("Bulambuli", ax2, "Bulambuli (flooding)"),
    ]:
        sub = df[df["District"] == district]
        for g in [1, 2, 3]:
            gsub = sub[sub[group_col] == g]
            if len(gsub) == 0:
                continue
            sizes = gsub["est_hh_per_village"] * 1.2
            ax.scatter(
                gsub["lon"], gsub["lat"],
                s=sizes, c=group_colors[g], alpha=0.7,
                edgecolors="black", linewidth=0.5, label=group_labels[g],
            )
        for _, r in sub.iterrows():
            ax.annotate(
                f'{r["est_hh_per_village"]:.0f}',
                (r["lon"], r["lat"]),
                fontsize=5, color="gray", ha="center", va="bottom",
                xytext=(0, 5), textcoords="offset points",
            )
        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.legend(fontsize=7, loc="lower left")
        ax.set_aspect("equal")
        ax.grid(True, alpha=0.3)

    fig.suptitle(title_str, fontsize=12, fontweight="bold")
    fig.tight_layout()
    fig.savefig(PLOTS / filename, dpi=150, bbox_inches="tight")
    print(f"Saved {filename}")
    plt.close()


def plot_randomization_spillovers():
    """Village-level randomization (2:1:2) — shows spillover risk."""
    import pandas as pd
    df = pd.read_csv(ROOT / "raw" / "villages_clean.csv")
    df = df.dropna(subset=["lat"]).copy()
    np.random.seed(42)

    for district in df["District"].unique():
        mask = df["District"] == district
        n = mask.sum()
        ratio = np.array([2, 1, 2])
        counts = (ratio / ratio.sum() * n).astype(int)
        counts[-1] = n - counts[:-1].sum()
        assignments = np.concatenate([np.full(c, g + 1) for g, c in enumerate(counts)])
        np.random.shuffle(assignments)
        df.loc[mask, "group"] = assignments

    df["group"] = df["group"].astype(int)
    _plot_randomization(
        df, "group",
        "Village-Level Randomization (2:1:2, seed=42)\nDot size = estimated HH — Note neighboring villages in different arms",
        "randomization_village_level.png",
    )


def plot_randomization_parish():
    """Parish-level randomization — all villages in a parish get the same arm."""
    import pandas as pd
    df = pd.read_csv(ROOT / "raw" / "villages_clean.csv")
    df = df.dropna(subset=["lat"]).copy()
    np.random.seed(42)

    for district in df["District"].unique():
        parishes = df[df["District"] == district]["Parish"].unique()
        n_parishes = len(parishes)
        ratio = np.array([2, 1, 2])
        counts = (ratio / ratio.sum() * n_parishes).astype(int)
        counts[-1] = n_parishes - counts[:-1].sum()
        assignments = np.concatenate([np.full(c, g + 1) for g, c in enumerate(counts)])
        np.random.shuffle(assignments)
        parish_map = dict(zip(parishes, assignments))
        mask = df["District"] == district
        df.loc[mask, "group"] = df.loc[mask, "Parish"].map(parish_map)

    df["group"] = df["group"].astype(int)
    n_parishes = df.groupby("Parish")["group"].first().nunique()
    total_parishes = df["Parish"].nunique()
    _plot_randomization(
        df, "group",
        f"Parish-Level Randomization ({total_parishes} parishes, 2:1:2, seed=42)\n"
        "All villages in a parish assigned to same arm — eliminates within-parish spillovers",
        "randomization_parish_level.png",
    )


def plot_randomization_hybrid():
    """Hybrid: village-level in Amuria (spread out), parish-level in Bulambuli (dense)."""
    import pandas as pd
    df = pd.read_csv(ROOT / "raw" / "villages_clean.csv")
    df = df.dropna(subset=["lat"]).copy()
    np.random.seed(42)

    # Amuria: village-level
    mask_a = df["District"] == "Amuria"
    n_a = mask_a.sum()
    ratio = np.array([2, 1, 2])
    counts = (ratio / ratio.sum() * n_a).astype(int)
    counts[-1] = n_a - counts[:-1].sum()
    assignments = np.concatenate([np.full(c, g + 1) for g, c in enumerate(counts)])
    np.random.shuffle(assignments)
    df.loc[mask_a, "group"] = assignments

    # Bulambuli: parish-level
    mask_b = df["District"] == "Bulambuli"
    parishes_b = df[mask_b]["Parish"].unique()
    n_p = len(parishes_b)
    counts = (ratio / ratio.sum() * n_p).astype(int)
    counts[-1] = n_p - counts[:-1].sum()
    assignments = np.concatenate([np.full(c, g + 1) for g, c in enumerate(counts)])
    np.random.shuffle(assignments)
    parish_map = dict(zip(parishes_b, assignments))
    df.loc[mask_b, "group"] = df.loc[mask_b, "Parish"].map(parish_map)

    df["group"] = df["group"].astype(int)
    n_units = n_a + n_p
    _plot_randomization(
        df, "group",
        f"Hybrid Randomization (seed=42)\n"
        f"Amuria: village-level ({n_a} villages) — Bulambuli: parish-level ({n_p} parishes) — {n_units} total units",
        "randomization_hybrid.png",
    )


def plot_randomization_geo_cluster(threshold_km):
    """Randomize at geographic cluster level using hierarchical clustering."""
    import pandas as pd
    from scipy.cluster.hierarchy import fcluster, linkage

    df = pd.read_csv(ROOT / "raw" / "villages_clean.csv")
    df = df.dropna(subset=["lat"]).copy()
    np.random.seed(42)

    coords_km = df[["lat", "lon"]].values * 111
    Z = linkage(coords_km, method="complete")
    df["geo_cluster"] = fcluster(Z, t=threshold_km, criterion="distance")

    # Assign groups at the cluster level, stratified by district
    for district in df["District"].unique():
        mask = df["District"] == district
        clusters = df.loc[mask, "geo_cluster"].unique()
        n_c = len(clusters)
        ratio = np.array([2, 1, 2])
        counts = (ratio / ratio.sum() * n_c).astype(int)
        counts[-1] = n_c - counts[:-1].sum()
        assignments = np.concatenate([np.full(c, g + 1) for g, c in enumerate(counts)])
        np.random.shuffle(assignments)
        cluster_map = dict(zip(clusters, assignments))
        df.loc[mask, "group"] = df.loc[mask, "geo_cluster"].map(cluster_map)

    df["group"] = df["group"].astype(int)

    n_clusters_a = df[df["District"] == "Amuria"]["geo_cluster"].nunique()
    n_clusters_b = df[df["District"] == "Bulambuli"]["geo_cluster"].nunique()
    n_total = n_clusters_a + n_clusters_b

    _plot_randomization(
        df, "group",
        f"Geographic Cluster Randomization ({threshold_km:.0f} km threshold, seed=42)\n"
        f"Amuria: {n_clusters_a} clusters — Bulambuli: {n_clusters_b} clusters — {n_total} total units",
        f"randomization_geo_{threshold_km:.0f}km.png",
    )


def plot_geo_clusters_map(threshold_km):
    """Show each geographic cluster in a unique color so you can see which villages group together."""
    import pandas as pd
    from scipy.cluster.hierarchy import fcluster, linkage
    import matplotlib.cm as cm

    df = pd.read_csv(ROOT / "raw" / "villages_clean.csv")
    df = df.dropna(subset=["lat"]).copy()

    coords_km = df[["lat", "lon"]].values * 111
    Z = linkage(coords_km, method="complete")
    df["geo_cluster"] = fcluster(Z, t=threshold_km, criterion="distance")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    for district, ax, title in [
        ("Amuria", ax1, "Amuria (drought)"),
        ("Bulambuli", ax2, "Bulambuli (flooding)"),
    ]:
        sub = df[df["District"] == district].copy()
        clusters = sorted(sub["geo_cluster"].unique())
        n_c = len(clusters)
        cmap = cm.get_cmap("tab20", max(n_c, 20))
        color_map = {c: cmap(i) for i, c in enumerate(clusters)}

        for cl in clusters:
            csub = sub[sub["geo_cluster"] == cl]
            sizes = csub["est_hh_per_village"] * 1.2
            ax.scatter(
                csub["lon"], csub["lat"],
                s=sizes, c=[color_map[cl]], alpha=0.8,
                edgecolors="black", linewidth=0.5,
                label=f"C{cl} ({len(csub)} villages)",
            )

        for _, r in sub.iterrows():
            ax.annotate(
                f'C{int(r["geo_cluster"])}',
                (r["lon"], r["lat"]),
                fontsize=5, color="black", ha="center", va="bottom",
                xytext=(0, 5), textcoords="offset points", fontweight="bold",
            )

        ax.set_title(f"{title}\n{n_c} clusters", fontsize=12, fontweight="bold")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.legend(fontsize=5, loc="lower left", ncol=2)
        ax.set_aspect("equal")
        ax.grid(True, alpha=0.3)

    n_total = df["geo_cluster"].nunique()
    fig.suptitle(
        f"Geographic Clusters ({threshold_km:.0f} km threshold, complete linkage)\n"
        f"{n_total} clusters total — villages in the same cluster share a color and label",
        fontsize=12, fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(PLOTS / f"geo_clusters_map_{threshold_km:.0f}km.png", dpi=150, bbox_inches="tight")
    print(f"Saved geo_clusters_map_{threshold_km:.0f}km.png")
    plt.close()


if __name__ == "__main__":
    print_power_summary()
    plot_mde_vs_clusters()
    plot_randomization_spillovers()
    plot_randomization_parish()
    plot_randomization_hybrid()
    plot_randomization_geo_cluster(2.0)
    plot_randomization_geo_cluster(3.0)
    plot_geo_clusters_map(2.0)
