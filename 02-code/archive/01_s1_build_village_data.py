import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"

xls = pd.ExcelFile(RAW / "20260420___Amuria & Bulambuli  Village selection_v2.xlsx")

# --- Villages ---
v = pd.read_excel(xls, sheet_name=0)
v.columns = v.columns.str.strip()
if "Coordiantes" in v.columns:
    v.rename(columns={"Coordiantes": "Coordinates"}, inplace=True)


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


v["lat"], v["lon"] = zip(*v["Coordinates"].apply(parse_coords))
v.drop(columns=["Coordinates"], inplace=True)

# --- Population ---
pop = pd.read_excel(xls, sheet_name=1)
pop = pop.dropna(subset=["Parish"]).copy()
pop["District"] = pop["District"].ffill()
pop["Subcounty"] = pop["Subcounty"].ffill()
pop.rename(columns={
    "Total HHs": "parish_total_hhs",
    "Total Population": "parish_total_pop",
    "Av. HH size": "parish_avg_hh_size",
    "HH population": "parish_hh_pop",
}, inplace=True)
pop["Parish_upper"] = pop["Parish"].str.upper().replace({"NAMEZI": "NAMEZE"})

# --- Village counts per parish ---
v["Parish_upper"] = v["Parish"].str.upper()
village_counts = v.groupby("Parish_upper").size().reset_index(name="parish_n_villages")
pop = pop.merge(village_counts, on="Parish_upper", how="left")
pop["est_hh_per_village"] = (pop["parish_total_hhs"] / pop["parish_n_villages"]).round(1)

# --- Merge ---
pop_cols = ["Parish_upper", "parish_total_hhs", "parish_total_pop", "parish_hh_pop",
            "parish_avg_hh_size", "parish_n_villages", "est_hh_per_village"]
df = v.merge(pop[pop_cols], on="Parish_upper", how="left")
df.drop(columns=["Parish_upper"], inplace=True)

out = RAW / "villages_clean.csv"
df.to_csv(out, index=False)
print(f"Saved {out}")
print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print(f"\n{df.head(10).to_string()}")
