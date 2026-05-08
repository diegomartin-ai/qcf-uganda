"""
QCF Uganda — Cash for Climate Adaptation
=========================================
Single analysis script: data → clustering → randomization → power calculations → plots → export.

Outputs:
  data/process/villages_randomized.csv          — 134 villages (119 randomized + 15 TBD)
  plots/randomization/geo_clusters_1km_39.png   — cluster identity map
  plots/randomization/randomization_1km_39.png  — randomization map (source of truth)
  plots/randomization/power_mde_vs_clusters.png — MDE curves for Q1
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.stats import norm
from pathlib import Path

# =====================================================================
# PATHS
# =====================================================================
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "01-data" / "raw"
PROCESS = ROOT / "01-data" / "process"
PROCESS.mkdir(parents=True, exist_ok=True)
PLOTS_CLUSTER = ROOT / "03-outputs" / "plots" / "clustering"
PLOTS_POWER = ROOT / "03-outputs" / "plots" / "power"
PLOTS_DEMO = ROOT / "03-outputs" / "plots" / "spillover-demos"
PLOTS_CLUSTER.mkdir(parents=True, exist_ok=True)
PLOTS_POWER.mkdir(parents=True, exist_ok=True)
PLOTS_DEMO.mkdir(parents=True, exist_ok=True)

# =====================================================================
# PARAMETERS
# =====================================================================
SEED = 2026
CLUSTER_THRESHOLD_KM = 1.0

ARM_LABELS = {1: "G1: Standard early", 2: "G2: Adaptation+plus", 3: "G3: Standard delayed"}
ARM_COLORS = {1: "#5DA5DA", 2: "#FAA43A", 3: "#60BD68"}

# Power calculation parameters
ALPHA = 0.05
POWER = 0.80
RHO_PANEL = 0.5           # baseline-endline correlation (ANCOVA gain)
SURVEY_RATE = 0.30         # fraction of HH surveyed per village
SD_CONTINUOUS = 112_500    # UGX, livelihood investment SD
MEAN_CONTINUOUS = 75_000   # UGX, livelihood investment mean
P_BINARY = 0.20           # baseline diversification rate
ICC_SCENARIOS = {"Low (0.05)": 0.05, "Medium (0.10)": 0.10, "High (0.15)": 0.15}

# =====================================================================
# 1. DATA LOADING AND CLUSTERING
# =====================================================================
print("=" * 70)
print("1. DATA AND CLUSTERING")
print("=" * 70)

df = pd.read_csv(RAW / "QCF_raw_clean_list.csv")
valid = df.dropna(subset=["lat"]).copy()
n_missing = len(df) - len(valid)
print(f"Loaded {len(df)} villages ({len(valid)} with GPS, {n_missing} missing)")

coords_km = valid[["lat", "lon"]].values * 111
Z = linkage(coords_km, method="complete")
valid["cluster"] = fcluster(Z, t=CLUSTER_THRESHOLD_KM, criterion="distance")

# Renumber clusters per district (C1, C2, ... within each)
for district in ["Amuria", "Bulambuli"]:
    mask = valid["District"] == district
    old_ids = sorted(valid.loc[mask, "cluster"].unique())
    valid.loc[mask, "cluster_label"] = (
        valid.loc[mask, "cluster"].map({old: i + 1 for i, old in enumerate(old_ids)}).astype(int)
    )

n_am = valid[valid.District == "Amuria"]["cluster"].nunique()
n_bul = valid[valid.District == "Bulambuli"]["cluster"].nunique()
n_total = n_am + n_bul
print(f"Clusters at {CLUSTER_THRESHOLD_KM} km: {n_total} total ({n_am} Amuria, {n_bul} Bulambuli)")

# =====================================================================
# 2. RANDOMIZATION (2:1:2, stratified by district)
# =====================================================================
print(f"\n{'=' * 70}")
print("2. RANDOMIZATION (2:1:2 ratio, stratified by district)")
print("=" * 70)

rng = np.random.default_rng(SEED)
cluster_df = valid.groupby(["District", "cluster"]).first().reset_index()[["District", "cluster"]]

arm_map = {}
for district in ["Amuria", "Bulambuli"]:
    clusters = cluster_df[cluster_df.District == district]["cluster"].values
    rng.shuffle(clusters)
    n = len(clusters)
    n2 = n // 5                # G2 gets floor(n/5) — minimize to maximize Q1 power
    n1 = (n - n2 + 1) // 2    # G1 gets half of remainder (rounded up)
    n3 = n - n1 - n2           # G3 gets the rest
    arms = [1] * n1 + [2] * n2 + [3] * n3
    for c, a in zip(clusters, arms):
        arm_map[c] = a

valid["arm"] = valid["cluster"].map(arm_map)

for district in ["Amuria", "Bulambuli"]:
    sub = valid[valid.District == district]
    print(f"\n{district}:")
    for arm in [1, 2, 3]:
        asub = sub[sub.arm == arm]
        print(f"  {ARM_LABELS[arm]}: {asub.cluster.nunique()}c, {len(asub)}v")

k_g1 = valid[valid.arm == 1]["cluster"].nunique()
k_g2 = valid[valid.arm == 2]["cluster"].nunique()
k_g3 = valid[valid.arm == 3]["cluster"].nunique()
print(f"\nTotal: {k_g1}/{k_g2}/{k_g3} clusters (G1/G2/G3), {len(valid)} villages")

# =====================================================================
# 3. EXPORT
# =====================================================================
print(f"\n{'=' * 70}")
print("3. EXPORT")
print("=" * 70)

export = valid[["District", "Sub county", "Parish", "Village", "lat", "lon",
                "parish_total_hhs", "parish_total_pop", "est_hh_per_village",
                "cluster", "cluster_label", "arm"]].copy()
export = export.rename(columns={"cluster": "cluster_id", "cluster_label": "cluster_label_district"})
export["arm_label"] = export["arm"].map(ARM_LABELS)
export["group"] = export["arm"].map({1: "G1", 2: "G2", 3: "G3"})
export["baseline_month"] = ""
export["note"] = ""

# Append missing-GPS villages
missing = df[df["lat"].isna()][["District", "Sub county", "Parish", "Village", "lat", "lon",
                                 "parish_total_hhs", "parish_total_pop", "est_hh_per_village"]].copy()
for col in ["cluster_id", "cluster_label_district", "arm", "arm_label", "group", "baseline_month"]:
    missing[col] = ""
missing["note"] = "Programs getting the latitude and longitude"
export = pd.concat([export, missing], ignore_index=True)

export_path = PROCESS / "QCF_cluster_village_assignation.csv"
export.to_csv(export_path, index=False)
n_valid = export["note"].eq("").sum()
n_tbd = export["note"].ne("").sum()
print(f"Saved: {export_path} ({n_valid} randomized + {n_tbd} TBD = {len(export)} total)")

# =====================================================================
# 4. POWER CALCULATIONS
# =====================================================================
print(f"\n{'=' * 70}")
print("4. POWER CALCULATIONS")
print("=" * 70)

z_alpha = norm.ppf(1 - ALPHA / 2)
z_beta = norm.ppf(POWER)

# Weighted average HH surveyed per cluster
hh_amuria = valid[valid.District == "Amuria"]["est_hh_per_village"].mean()
hh_bulambuli = valid[valid.District == "Bulambuli"]["est_hh_per_village"].mean()
frac_am = n_am / n_total
frac_bul = n_bul / n_total
m_weighted = (frac_am * hh_amuria + frac_bul * hh_bulambuli) * SURVEY_RATE
print(f"Avg HH surveyed/cluster: {m_weighted:.1f} (Amuria ~{hh_amuria * SURVEY_RATE:.0f}, Bulambuli ~{hh_bulambuli * SURVEY_RATE:.0f})")


def mde_cluster(k_per_arm, m, icc, sd, rho=RHO_PANEL):
    """MDE for cluster-randomized design with ANCOVA."""
    deff = 1 + (m - 1) * icc
    var_reduction = 1 - rho ** 2
    se = np.sqrt(2 * sd ** 2 * var_reduction * deff / (k_per_arm * m))
    return (z_alpha + z_beta) * se


def mde_individual(n_per_arm, sd, rho=RHO_PANEL):
    """MDE for individual-randomized design with ANCOVA."""
    se = np.sqrt(2 * sd ** 2 * (1 - rho ** 2) / n_per_arm)
    return (z_alpha + z_beta) * se


# Q1: Cash effect (G1 vs G3, cluster-level)
k_q1 = min(k_g1, k_g3)  # power limited by smaller arm
print(f"\nQ1: Cash effect (G1 vs G3) — {k_g1} vs {k_g3} clusters")
print(f"  Continuous (livelihood investment, SD={SD_CONTINUOUS:,} UGX):")
for label, icc in ICC_SCENARIOS.items():
    mde = mde_cluster(k_q1, m_weighted, icc, SD_CONTINUOUS)
    print(f"    {label}: MDE = {mde:,.0f} UGX ({mde / SD_CONTINUOUS:.2f} SD)")

sd_binary = np.sqrt(P_BINARY * (1 - P_BINARY))
print(f"  Binary (diversification, baseline={P_BINARY:.0%}):")
for label, icc in ICC_SCENARIOS.items():
    mde = mde_cluster(k_q1, m_weighted, icc, sd_binary)
    print(f"    {label}: MDE = {mde * 100:.1f} pp")

# Q2: Baraza framing (G1 vs G2c, cluster-level)
# G2c is 1/3 of G2 HH, but comparison is at cluster level (G1 clusters vs G2 clusters)
k_q2 = min(k_g1, k_g2)
print(f"\nQ2: Baraza framing (G1 vs G2) — {k_g1} vs {k_g2} clusters")
print(f"  Continuous:")
for label, icc in ICC_SCENARIOS.items():
    mde = mde_cluster(k_q2, m_weighted, icc, SD_CONTINUOUS)
    print(f"    {label}: MDE = {mde:,.0f} UGX ({mde / SD_CONTINUOUS:.2f} SD)")

# Q3: Plus components (2a vs 2b vs 2c, HH-level within G2)
n_g2_villages = (valid.arm == 2).sum()
total_hh_g2_surveyed = round(n_g2_villages * m_weighted)
n_per_subarm = round(total_hh_g2_surveyed / 3)
print(f"\nQ3: Plus components (HH-level within G2) — {n_g2_villages} villages, ~{n_per_subarm} HH/sub-arm")
mde_c = mde_individual(n_per_subarm, SD_CONTINUOUS)
mde_b = mde_individual(n_per_subarm, sd_binary)
print(f"  Continuous: MDE = {mde_c:,.0f} UGX ({mde_c / SD_CONTINUOUS:.2f} SD)")
print(f"  Binary: MDE = {mde_b * 100:.1f} pp")

# =====================================================================
# 5. PLOTS
# =====================================================================
print(f"\n{'=' * 70}")
print("5. PLOTS")
print("=" * 70)

# Dot sizing
hh_min = valid["est_hh_per_village"].min()
hh_max = valid["est_hh_per_village"].max()
SIZE_MIN, SIZE_MAX = 40, 350
valid["dot_size"] = SIZE_MIN + (valid["est_hh_per_village"] - hh_min) / (hh_max - hh_min) * (SIZE_MAX - SIZE_MIN)

# --- Figure 1: Cluster identity map ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
for ax, district, hazard in [(ax1, "Amuria", "drought"), (ax2, "Bulambuli", "flooding")]:
    sub = valid[valid["District"] == district]
    clusters = sorted(sub["cluster_label"].unique())
    nc = len(clusters)
    cmap = plt.colormaps.get_cmap("tab20" if nc <= 20 else "gist_ncar")
    handles = []
    for i, c in enumerate(clusters):
        csub = sub[sub["cluster_label"] == c]
        color = cmap(i % 20 / 20) if nc <= 20 else cmap(i / nc)
        ax.scatter(csub["lon"], csub["lat"], c=[color], s=csub["dot_size"],
                   alpha=0.7, edgecolors="white", linewidth=0.5, zorder=3)
        for _, row in csub.iterrows():
            ax.annotate(f"C{int(c)}", (row["lon"], row["lat"]),
                        fontsize=6, ha="center", va="bottom", xytext=(0, 5), textcoords="offset points")
        handles.append(ax.scatter([], [], c=[color], s=60, label=f"C{int(c)} ({len(csub)}v)",
                                  edgecolors="white", linewidth=0.5))
    ax.set_xlabel("Longitude"); ax.set_ylabel("Latitude")
    ax.set_title(f"{district} ({hazard})\n{nc} clusters", fontsize=13, fontweight="bold")
    ax.legend(handles=handles, loc="lower left", fontsize=7, ncol=2, framealpha=0.9, markerscale=0.8)
    ax.grid(True, alpha=0.3)

fig.suptitle(f"Geographic Cluster Assignment ({CLUSTER_THRESHOLD_KM:.0f} km threshold)\n"
             f"{n_total} clusters total — {n_am} Amuria, {n_bul} Bulambuli\n"
             f"Dot size ∝ est. households/village ({hh_min:.0f}–{hh_max:.0f})",
             fontsize=14, fontweight="bold")
plt.tight_layout()
p1 = PLOTS_CLUSTER / "geo_clusters_1km_39.png"
plt.savefig(p1, dpi=150, bbox_inches="tight"); plt.close()
print(f"Saved: {p1}")

# --- Figure 2: Randomization map ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
for ax, district, hazard in [(ax1, "Amuria", "drought"), (ax2, "Bulambuli", "flooding")]:
    sub = valid[valid["District"] == district]
    for arm in [1, 2, 3]:
        asub = sub[sub.arm == arm]
        ax.scatter(asub["lon"], asub["lat"], c=ARM_COLORS[arm], s=asub["dot_size"],
                   alpha=0.7, edgecolors="white", linewidth=0.5, zorder=3,
                   label=f"{ARM_LABELS[arm]} ({asub.cluster.nunique()}c, {len(asub)}v)")
    for _, row in sub.iterrows():
        ax.annotate(f"C{int(row['cluster_label'])}", (row["lon"], row["lat"]),
                    fontsize=6, ha="center", va="bottom", xytext=(0, 5), textcoords="offset points")
    ax.set_xlabel("Longitude"); ax.set_ylabel("Latitude")
    ax.set_title(f"{district} ({hazard})\n{sub.cluster_label.nunique()} clusters", fontsize=13, fontweight="bold")
    ax.legend(loc="lower left", fontsize=8, framealpha=0.9)
    ax.grid(True, alpha=0.3)

fig.suptitle(f"Stratified Randomization ({CLUSTER_THRESHOLD_KM:.0f} km clusters)\n"
             f"Stratification variable: District — {n_total} clusters → 3 arms (2:1:2)\n"
             f"Dot size ∝ est. households/village ({hh_min:.0f}–{hh_max:.0f})",
             fontsize=14, fontweight="bold")
plt.tight_layout()
p2 = PLOTS_CLUSTER / "randomization_1km_39.png"
plt.savefig(p2, dpi=150, bbox_inches="tight"); plt.close()
print(f"Saved: {p2}")

# --- Figure 3: Power — MDE vs clusters per arm ---
k_range = np.arange(5, 60, 1)
ref_effects = {
    "Haushofer & Shapiro 2016": {"sd": 0.52, "pp": None},
    "Egger et al. 2022 (Kenya GE)": {"sd": 0.36, "pp": 8},
    "GD Malawi (Aggarwal 2023)": {"sd": 0.25, "pp": 18},
    "Labeling effects (Thomas 2020)": {"sd": 0.15, "pp": 4},
}

fig, (ax_c, ax_b) = plt.subplots(1, 2, figsize=(14, 6))

# Continuous
for label, icc in ICC_SCENARIOS.items():
    mdes = [mde_cluster(k, m_weighted, icc, SD_CONTINUOUS) / SD_CONTINUOUS for k in k_range]
    ax_c.plot(k_range, mdes, label=f"ICC = {icc}", linewidth=2)
ax_c.axvspan(k_q1 - 0.5, k_q1 + 0.5, alpha=0.2, color="blue", label=f"Our design ({k_q1}c/arm)")
for name, vals in ref_effects.items():
    if vals["sd"]:
        ax_c.axhline(y=vals["sd"], color="red", linestyle=":", alpha=0.5, linewidth=1)
        ax_c.text(60.5, vals["sd"], name, fontsize=6.5, va="center", color="red", alpha=0.8)
ax_c.set_xlabel("Clusters per arm"); ax_c.set_ylabel("MDE (SD units)")
ax_c.set_title("Q1: Livelihood Investment ($)\nCluster-randomized", fontsize=12, fontweight="bold")
ax_c.legend(fontsize=8, loc="upper right"); ax_c.grid(True, alpha=0.3)
ax_c.set_ylim(0, 0.8); ax_c.set_xlim(5, 60)

# Binary
for label, icc in ICC_SCENARIOS.items():
    mdes = [mde_cluster(k, m_weighted, icc, sd_binary) * 100 for k in k_range]
    ax_b.plot(k_range, mdes, label=f"ICC = {icc}", linewidth=2)
ax_b.axvspan(k_q1 - 0.5, k_q1 + 0.5, alpha=0.2, color="blue", label=f"Our design ({k_q1}c/arm)")
for name, vals in ref_effects.items():
    if vals["pp"]:
        ax_b.axhline(y=vals["pp"], color="red", linestyle=":", alpha=0.5, linewidth=1)
        ax_b.text(60.5, vals["pp"], name, fontsize=6.5, va="center", color="red", alpha=0.8)
ax_b.set_xlabel("Clusters per arm"); ax_b.set_ylabel("MDE (percentage points)")
ax_b.set_title("Q1: Income Diversification (%)\nCluster-randomized", fontsize=12, fontweight="bold")
ax_b.legend(fontsize=8, loc="upper right"); ax_b.grid(True, alpha=0.3)
ax_b.set_ylim(0, 30); ax_b.set_xlim(5, 60)

fig.suptitle(f"Minimum Detectable Effect vs. Clusters per Arm\n"
             f"(α={ALPHA}, power={POWER}, panel ρ={RHO_PANEL}, avg {m_weighted:.0f} HH surveyed/cluster)",
             fontsize=13, fontweight="bold")
fig.tight_layout()
p3 = PLOTS_POWER / "power_mde_vs_clusters.png"
fig.savefig(p3, dpi=150, bbox_inches="tight"); plt.close()
print(f"Saved: {p3}")

# --- Figure 4: Village-level randomization (spillover demo) ---
demo = df.dropna(subset=["lat"]).copy()
demo_rng = np.random.default_rng(42)
for district in ["Amuria", "Bulambuli"]:
    mask = demo["District"] == district
    n = mask.sum()
    n2 = n // 5; n1 = (n - n2 + 1) // 2; n3 = n - n1 - n2
    a = [1]*n1 + [2]*n2 + [3]*n3
    demo_rng.shuffle(a)
    demo.loc[mask, "demo_arm"] = a
demo["demo_arm"] = demo["demo_arm"].astype(int)
demo["dot_size"] = SIZE_MIN + (demo["est_hh_per_village"] - hh_min) / (hh_max - hh_min) * (SIZE_MAX - SIZE_MIN)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
for ax, district, hazard in [(ax1, "Amuria", "drought"), (ax2, "Bulambuli", "flooding")]:
    sub = demo[demo["District"] == district]
    for arm in [1, 2, 3]:
        asub = sub[sub.demo_arm == arm]
        ax.scatter(asub["lon"], asub["lat"], c=ARM_COLORS[arm], s=asub["dot_size"],
                   alpha=0.7, edgecolors="white", linewidth=0.5, zorder=3,
                   label=f"{ARM_LABELS[arm]} ({len(asub)}v)")
    ax.set_xlabel("Longitude"); ax.set_ylabel("Latitude")
    ax.set_title(f"{district} ({hazard})", fontsize=13, fontweight="bold")
    ax.legend(loc="lower left", fontsize=8, framealpha=0.9); ax.grid(True, alpha=0.3)

fig.suptitle(f"Simulated Village-Level Randomization (2:1:2 ratio)\n"
             f"Note: neighboring villages in Bulambuli assigned to different arms — spillover risk\n"
             f"Dot size ∝ est. households/village ({hh_min:.0f}–{hh_max:.0f})",
             fontsize=14, fontweight="bold")
plt.tight_layout()
p4 = PLOTS_DEMO / "randomization_village_level.png"
plt.savefig(p4, dpi=150, bbox_inches="tight"); plt.close()
print(f"Saved: {p4}")

print(f"\n{'=' * 70}")
print("DONE")
print("=" * 70)
