import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import fcluster, linkage
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
PLOTS = ROOT / "plots" / "randomization"
PLOTS.mkdir(parents=True, exist_ok=True)

# --- Load and clean ---
df = pd.read_excel(RAW / "20260420___Amuria & Bulambuli  Village selection.xlsx")
df.rename(columns={"Coordiantes": "Coordinates"}, inplace=True)


def parse_coords(c):
    if pd.isna(c):
        return np.nan, np.nan
    c = str(c).strip().lstrip(":").strip().split("\n")[0].strip()
    parts = c.split(",")
    if len(parts) == 2:
        try:
            return float(parts[0].strip()), float(parts[1].strip())
        except ValueError:
            return np.nan, np.nan
    return np.nan, np.nan


df["lat"], df["lon"] = zip(*df["Coordinates"].apply(parse_coords))
valid = df.dropna(subset=["lat"]).copy()
missing_n = len(df) - len(valid)

DISTRICT_COLORS = {"Amuria": "#E63946", "Bulambuli": "#457B9D"}
SUBCOUNTY_COLORS = {"Abarilela": "#E63946", "Namisuni": "#457B9D", "BULUGANYA": "#2A9D8F"}


# --- Plot 1: Village map by sub-county (two panels) ---
def plot_village_map():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    for district, ax, title in [
        ("Amuria", ax1, "Amuria (drought)"),
        ("Bulambuli", ax2, "Bulambuli (flooding)"),
    ]:
        sub = valid[valid["District"] == district]
        for sc in sub["Sub county"].unique():
            sc_data = sub[sub["Sub county"] == sc]
            ax.scatter(
                sc_data["lon"], sc_data["lat"],
                c=SUBCOUNTY_COLORS[sc], label=sc, s=40, alpha=0.8,
                edgecolors="white", linewidth=0.5,
            )
        for parish, grp in sub.groupby("Parish"):
            cx, cy = grp["lon"].mean(), grp["lat"].mean()
            ax.annotate(
                parish, (cx, cy), fontsize=7, fontstyle="italic", color="gray",
                ha="center", va="bottom", xytext=(0, 6), textcoords="offset points",
            )
        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.legend(title="Sub-county", fontsize=8, title_fontsize=9)
        ax.set_aspect("equal")
        ax.grid(True, alpha=0.3)
    fig.suptitle(
        f"QCF Uganda — Village Locations (n={len(valid)} plotted, {missing_n} missing coordinates)",
        fontsize=13, fontweight="bold", y=1.02,
    )
    plt.tight_layout()
    fig.savefig(PLOTS / "village_map.png", dpi=150, bbox_inches="tight")
    print("Saved village_map.png")
    plt.close()


# --- Plot 2: Clusters by distance threshold ---
def plot_clusters_by_distance():
    coords_km = valid[["lat", "lon"]].values * 111
    Z = linkage(coords_km, method="complete")
    thresholds = np.arange(0.5, 15.5, 0.5)
    counts = {k: [] for k in ["All", "Amuria", "Bulambuli"]}
    for t in thresholds:
        labels = fcluster(Z, t=t, criterion="distance")
        valid["cluster"] = labels
        counts["All"].append(valid["cluster"].nunique())
        counts["Amuria"].append(valid[valid["District"] == "Amuria"]["cluster"].nunique())
        counts["Bulambuli"].append(valid[valid["District"] == "Bulambuli"]["cluster"].nunique())

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(thresholds, counts["All"], "k-o", ms=4, label="All", linewidth=2)
    ax.plot(thresholds, counts["Amuria"], "--s", color="#E63946", ms=4, label="Amuria")
    ax.plot(thresholds, counts["Bulambuli"], "--^", color="#457B9D", ms=4, label="Bulambuli")
    ax.set_xlabel("Distance threshold (km)", fontsize=11)
    ax.set_ylabel("Number of clusters", fontsize=11)
    ax.set_title("Number of Geographic Clusters by Distance Threshold", fontsize=13, fontweight="bold")
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xticks(range(0, 16))
    fig.tight_layout()
    fig.savefig(PLOTS / "clusters_by_distance.png", dpi=150, bbox_inches="tight")
    print("Saved clusters_by_distance.png")
    plt.close()


# --- Plot 3: All villages colored by district ---
def plot_villages_all():
    fig, ax = plt.subplots(figsize=(10, 8))
    for district, color in DISTRICT_COLORS.items():
        sub = valid[valid["District"] == district]
        ax.scatter(
            sub["lon"], sub["lat"], c=color, s=30, alpha=0.7,
            edgecolors="white", linewidth=0.3, label=district,
        )
    for _, r in valid.iterrows():
        ax.annotate(
            r["Village"], (r["lon"], r["lat"]),
            fontsize=4, color="gray", alpha=0.8,
            xytext=(2, 2), textcoords="offset points",
        )
    mid_lon = (valid[valid["District"] == "Amuria"]["lon"].max() + valid[valid["District"] == "Bulambuli"]["lon"].min()) / 2
    mid_lat = (valid["lat"].min() + valid["lat"].max()) / 2
    ax.annotate("~98 km apart", (mid_lon, mid_lat), fontsize=11, color="#555555", ha="center", fontstyle="italic")
    ax.set_xlabel("Longitude", fontsize=11)
    ax.set_ylabel("Latitude", fontsize=11)
    ax.set_title(f"All Villages by District (n={len(valid)})", fontsize=13, fontweight="bold")
    ax.legend(fontsize=10)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(PLOTS / "villages_all.png", dpi=150, bbox_inches="tight")
    print("Saved villages_all.png")
    plt.close()


# --- Plot 4: Villages sized by estimated households ---
def plot_villages_by_size():
    df = pd.read_csv(ROOT / "raw" / "villages_clean.csv")
    df = df.dropna(subset=["lat", "est_hh_per_village"])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6), gridspec_kw={"width_ratios": [1, 1.3], "wspace": 0.15})

    for district, ax, title in [
        ("Amuria", ax1, "Amuria (drought)"),
        ("Bulambuli", ax2, "Bulambuli (flooding)"),
    ]:
        sub = df[df["District"] == district]
        sizes = sub["est_hh_per_village"]
        sc = ax.scatter(
            sub["lon"], sub["lat"],
            s=sizes * 1.5, c=sizes, cmap="YlOrRd", alpha=0.8,
            edgecolors="black", linewidth=0.5, vmin=0, vmax=250,
        )
        for _, r in sub.iterrows():
            lbl_color = "white" if district == "Amuria" else "gray"
            ax.annotate(
                f'{r["est_hh_per_village"]:.0f}',
                (r["lon"], r["lat"]),
                fontsize=5, color=lbl_color, ha="center", va="bottom",
                xytext=(0, 5), textcoords="offset points",
            )
        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.set_aspect("equal")
        ax.grid(True, alpha=0.3)

    fig.suptitle(
        "Village Locations Sized by Estimated Households",
        fontsize=13, fontweight="bold",
    )
    fig.subplots_adjust(bottom=0.15)
    cbar_ax = fig.add_axes([0.3, 0.05, 0.4, 0.02])
    cbar = fig.colorbar(sc, cax=cbar_ax, orientation="horizontal")
    cbar.set_label("Estimated HH per village", fontsize=10)
    fig.savefig(PLOTS / "villages_by_size.png", dpi=150, bbox_inches="tight")
    print("Saved villages_by_size.png")
    plt.close()


if __name__ == "__main__":
    plot_village_map()
    plot_clusters_by_distance()
    plot_villages_all()
    plot_villages_by_size()
