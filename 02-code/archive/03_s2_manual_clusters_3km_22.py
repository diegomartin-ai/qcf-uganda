"""
Manual cluster assignment for QCF Uganda randomization.

Base: 3km geographic clusters (complete linkage).
Manual adjustments:
  - Amuria C9 (2 villages, 1.54 km apart): split into individual units
  - Amuria C10 (4 villages): split — AARATOM+OGWETE stay together (0.02 km),
    KATINE and ASILANG become individual units
  - Amuria C16 (2 villages, 1.89 km apart): split into individual units
  - Bulambuli: keep 3km clusters as-is
"""

import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"

df = pd.read_csv(RAW / "villages_clean.csv")
valid = df.dropna(subset=["lat"]).copy()

# 3km geographic clusters
coords_km = valid[["lat", "lon"]].values * 111
Z = linkage(coords_km, method="complete")
valid["manual_cluster"] = fcluster(Z, t=3.0, criterion="distance").astype(str)

# --- Amuria manual splits ---
am = valid["District"] == "Amuria"

# C9: split AKAMURIEI and OPADOI into individual units
valid.loc[am & (valid["Village"] == "AKAMURIEI"), "manual_cluster"] = "9a"
valid.loc[am & (valid["Village"] == "OPADOI"), "manual_cluster"] = "9b"

# C10: AARATOM+OGWETE stay together (10a), KATINE+ASILANG together (10b)
valid.loc[am & (valid["Village"].isin(["AARATOM", "OGWETE"])), "manual_cluster"] = "10a"
valid.loc[am & (valid["Village"].isin(["KATINE", "ASILANG"])), "manual_cluster"] = "10b"

# C12: split NAIKURO and OMODOI into individual units
valid.loc[am & (valid["Village"] == "NAIKURO"), "manual_cluster"] = "12a"
valid.loc[am & (valid["Village"] == "OMODOI"), "manual_cluster"] = "12b"

# C16: split ONGUTOI and AKERIAU into individual units
valid.loc[am & (valid["Village"] == "ONGUTOI"), "manual_cluster"] = "16a"
valid.loc[am & (valid["Village"] == "AKERIAU"), "manual_cluster"] = "16b"

# --- Bulambuli manual splits ---
bul = valid["District"] == "Bulambuli"

# C6: split — KISIYOPO+BIRINDA (south, 0.45 km) vs MABONO+MADUWA+MASEJESE (north)
valid.loc[bul & (valid["Village"].isin(["KISIYOPO", "BIRINDA"])), "manual_cluster"] = "6a"
valid.loc[bul & (valid["Village"].isin(["MABONO", "MADUWA", "MASEJESE"])), "manual_cluster"] = "6b"

# Merge back
df = df.merge(
    valid[["District", "Parish", "Village", "manual_cluster"]],
    on=["District", "Parish", "Village"],
    how="left",
)

out = RAW / "villages_with_clusters.csv"
df.to_csv(out, index=False)

# Summary
print(f"Saved {out}\n")
for district in ["Amuria", "Bulambuli"]:
    sub = df[df["District"] == district]
    clusters = sorted(sub["manual_cluster"].dropna().unique(), key=lambda x: (len(x), x))
    n_villages = sub["manual_cluster"].notna().sum()
    print(f"{district}: {len(clusters)} clusters, {n_villages} villages")
    for c in clusters:
        csub = sub[sub["manual_cluster"] == c]
        villages = ", ".join(csub["Village"].tolist())
        print(f"  {c:>4}: {len(csub)}v — {villages}")
    print()

total = df["manual_cluster"].nunique()
print(f"Total clusters: {total}")
