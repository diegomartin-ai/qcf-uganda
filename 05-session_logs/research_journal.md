# QCF Uganda — Research Journal

Project: Cash for Climate Adaptation in Uganda (Quadrature Climate Foundation)

---

## Program Reference (consolidated from MELP, LaTeX draft, Tech Brief)

### Program overview
- **Funder**: Quadrature Climate Foundation (QCF)
- **Implementer**: GiveDirectly
- **Location**: Bulambuli District (flooding, waterlogging) and Amuria District (drought), Uganda
- **Start date**: June 1, 2026
- **Recipients**: ~11,801 adults across targeted villages (saturation within selected villages — all eligible adults enrolled)
- **Transfer**: $644 USD per recipient in two tranches: $50 token after enrollment → $594 lump sum several weeks later
- **Reporting**: First report October 2026, final report October 2027

### Theory of change
Cash relaxes liquidity and capital constraints → households make forward-looking livelihood investments supporting ex-ante climate adaptation. Allocation depends on beliefs about future climate risk. Five spending channels:
1. **Expand** existing livelihoods (more of the same) — standard LLS pathway
2. **Diversify** into new income-generating activities — standard LLS pathway
3. **Resilience** investments in existing livelihoods (drought-tolerant crops, irrigation, raised storage) — climate adaptation pathway
4. **General consumer durables** (furniture, housing) — standard LLS pathway
5. **Climate-protective durable assets** (roofing, drainage, elevated storage) — climate adaptation pathway

Central distinction: income expansion (channels 1, 2, 4) vs. reducing climate exposure (channels 3, 5). Transfer size constraints mean these may compete.

### Research questions and three-arm design
- **Q1 (cash effect)**: What is the effect of unconditional LLS cash transfers vs. no cash on behavioral outcomes at 3 months? → Group 1 vs. Group 3, cluster-level randomization
- **Q2 (baraza framing)**: What is the effect of climate-adaptation-framed Baraza vs. standard Baraza? → Group 1 vs. Group 2c, cluster-level randomization
- **Q3 (plus components)**: What is the additional effect of light-touch plus components (historical climate info, adaptation aspirations planning)? → Group 2a vs. 2b vs. 2c, household-level randomization within Group 2

| Arm | Description | Cash timing | Baraza type |
|-----|-------------|-------------|-------------|
| **Group 1** | Standard LLS | Early (Jun–Nov 2026) | Default "Community Empowerment" |
| **Group 2** | LLS + climate plus | Early (Jun–Nov 2026) | Climate adaptation framing |
| **Group 3** | Standard LLS | Delayed | Default "Community Empowerment" |

### Group 2 sub-arms (household-level, equal 1/3 probability)

| Sub-arm | Intervention | Channel | Timing |
|---------|-------------|---------|--------|
| **2a** | Historical climate information messages | SMS (recipient's preferred language) | 1–4 weeks after token, before LLS |
| **2b** | Adaptation aspirations planning | In-person visit (~10–15 min, non-directive) | 1–4 weeks after token, before LLS |
| **2c** | Neither (control within Group 2) | — | — |

Key constraints: randomization at enrollment (not delivery) to avoid baseline contamination; plus delivery anchored to token confirmation, not calendar dates; field officers blinded to sub-arm logic; SMS content finalized ~June 18, aspirations script ~June 16.

### Estimation equations

**Q1** (cash effect, cluster-level):
$$Y_{iv} = α + β D_v^{(1)} + γ Y_{iv,baseline} + δ X_{iv} + ε_{iv}$$
SEs clustered at village level. No village FEs (treatment assigned at village level).

**Q2** (baraza framing, cluster-level):
$$Y_{iv} = α + β D_v^{(2c)} + γ Y_{iv,baseline} + δ X_{iv} + ε_{iv}$$
SEs clustered at village level. No village FEs.

**Q3** (plus components, household-level):
$$Y_{iv} = α + β D_i^{(2a)} + γ Y_{iv,baseline} + δ X_{iv} + μ_v + ε_{iv}$$
Village FEs included (randomization within villages). SEs clustered at village level.

### Indicators

**Standard LLS (15):** (1) food, (2) household consumables, (3) children's education, (4) consumer durables, (5) savings/debt, (6) livelihood investments, (7) healthcare, (8) food insecurity %, (9) dietary diversity ≥5 groups %, (10) psychological well-being score, (11) income-generating activity %, (12) hours worked/week, (13) increased income-generating activity %, (14) productive/non-productive asset ownership %, (15) total debt and savings value.

**Non-standard climate adaptation (10+1):**
- *0. Experienced climate shock* — % reporting shock + timing
- *I. Expectations & Constraints:* (1) perceived ability to prepare, (2) priority support needed
- *II. Allocation Choices:* (3) livelihood investment–expansion, (4) livelihood investment–diversification, (5) livelihood investment–resilience
- *III. Structural Adjustment:* (6) climate-related occupational change, (7) climate-related migration
- *IV. Spillovers & System Effects:* (8) individual investments with community spillovers, (9) positive coping in response to shock, (10) maladaptive coping (charcoal burning, bush burning, wetland encroachment)

**Primary outcomes:** livelihood investment spending (continuous, UGX) and % diversifying (binary).

### M&E design
- 30% of recipients surveyed (~3,540 HH) at baseline and endline — panel design (same HH both waves)
- Baseline at enrollment before first transfer; endline ~3 months after final transfer
- In-person surveys, ~30 minutes
- Simple random sampling at baseline; same recipients re-surveyed at endline

### Power calculation parameters (Session 2 calibration — to be updated with baseline)

**ICC ranges (from 14-study synthesis):**
- Livelihood investment / income diversification: 0.05 (low), 0.10 (medium), 0.15 (high)
- Most relevant Uganda estimate: ICC = 0.07 (ICAN-ICAR 2025)
- Food security: 0.01–0.05

**Baseline parameters:**
- Livelihood investment: mean 75,000 UGX/month, SD 112,500 UGX (CV = 1.5)
- Diversification rate: 20% baseline
- Food insecurity: 60% baseline
- Panel ANCOVA gain: ρ = 0.5
- Survey rate: 30% of HH per settlement → ~16 HH surveyed per cluster (weighted avg)

### Known limitations (from MELP)
1. No direct shock tracking between baseline and endline
2. No non-recipient comparison group — staggered design (G1 vs. G3) provides cash comparison
3. Limited cross-program comparability (no identical default LLS indicators in matched setting)
4. Baraza labeling integrated into design, not separately estimated
5. 3-month endline may miss longer-term adaptation outcomes

### Key references in draft
- Haushofer & Shapiro (2016): Kenya GD trial, ICC ~0.06, effects 0.25 SD
- Egger et al. (2022): Kenya GD general equilibrium, spatial spillovers documented, ICC ~0.10
- McIntosh & Zeitlin (2022): Rwanda, ICC ~0.05
- Aggarwal et al. (2023): Malawi, 18pp business ownership increase, ICC ~0.06–0.07
- ICAN-ICAR (2025): Uganda, ICC = 0.07
- Blattman et al. (2014): Northern Uganda, monthly earnings mean $20 SD $34
- SAGE (2012): Uganda extreme-poor monthly consumption ~40,600 UGX
- Thomas (2020): labeling/messaging effects typically 0.10–0.25 SD

---

## Session 1: April 20–21, 2026

### Data ingestion
- Read village selection file: 140 villages across 2 districts (Amuria: 16, Bulambuli: 124), 3 sub-counties, 15 parishes
- Read QCF MELP (14 pages): program design, theory of change, indicators, M&E plan
- Read QCF Visual Arms: timeline, power calcs, RACI, intervention prioritization
- Read GIZ Cash for Conservation concept note (separate program, DRC): extracted 25 comments, mapped indicators from QCF MELP

### GIZ logframe (side task)
- Drafted 5 conservation-specific indicators for GIZ concept note (refined from QCF MELP)
- Created `raw/GIZ_Project_Logframe.xlsx`

### Design documentation
- Created design summary covering program overview, three-arm design, research questions, identification strategy, theory of change, all 25 indicators, limitations, reporting timeline
- Content now lives in `drafts/QCF_Uganda.tex`

### Data quality assessment
- 16 villages with missing coordinates (all Bulambuli) — confirmed no public GPS exists, need field collection
- 6 duplicate village names across parishes — resolved with programs team
- Coordinate formatting issues (leading colons, multiple coords) — mostly fixed in v2
- Drafted and sent data quality validation message to field team

### Geographic analysis
- Created village maps (by district, by sub-county, by parish)
- Ran hierarchical clustering: Bulambuli villages densely packed (124 → 8 clusters at 3 km), Amuria spread out (16 → 9 clusters at 3 km)
- Two districts ~98 km apart — no cross-district spillover risk

### Key decisions
- Primary outcomes: livelihood investment spending ($, continuous) and % diversifying (binary)
- Q1 (cash effect): cluster-randomized at village level
- Q2 (plus effect): individual-randomized at household level within Group 2

---

## Session 2: April 22, 2026

### Data update
- Programs team provided v2 file: 134 villages (6 duplicates removed), column name fixed
- UBOS-NPHC 2024 parish-level population data added
- Built `raw/villages_clean.csv`: 134 rows × 12 columns
- Key finding: Amuria ~222 HH/village, Bulambuli ~29 HH/village (ratio 7.8:1)

### ICC literature review (deep research)
- Synthesized empirical ICCs from 14 studies across East Africa
- Recommended ranges: 0.05–0.15 for livelihood investment, 0.05–0.12 for diversification
- Most relevant Uganda estimate: ICC = 0.07 (ICAN-ICAR 2025)
- Egger et al. (2022) spillover warning: treatment effects cross village boundaries in dense settings

### Baseline parameters (deep research)
- Power Calcs sheet used Kenya data (mean $70–$120); our population is much poorer
- SAGE Uganda extreme-poor: monthly HH consumption ~40,600 UGX
- Adopted: mean 75,000 UGX, SD 112,500 UGX for livelihood investment; 20% baseline diversification rate

### Power calculations
- Built power calculation code with MDE curves across ICC scenarios
- At 56 clusters/arm (village-level): MDE 0.15–0.21 SD — well powered
- At 9 clusters/arm (22-cluster design): MDE 0.30–0.45 SD — within range of prior GD effects but tighter
- Q2 (household-level, ~149/sub-arm): MDE 0.28 SD — likely underpowered for labeling effects

### Spillover analysis and clustering
- Showed village-level randomization creates severe spillover problem in Bulambuli (neighbors in different arms)
- Parish-level randomization doesn't help — parishes overlap geographically (some within 100m)
- Tested geographic clustering at 1km, 2km, 3km thresholds
- Manual adjustment: split spread-out Amuria clusters, split one Bulambuli mid-range cluster
- Final: **22 clusters (13 Amuria + 9 Bulambuli)**
- Randomized into 3 arms (2:1:2 ratio, stratified by district, seed=2026)

### LaTeX draft
- Created `drafts/QCF_Uganda.tex` with:
  - Introduction, Data (placeholders)
  - Empirical Strategy: design, hypotheses/equations, cluster construction, power calculations
  - Appendices: program design, MELP indicators, power calculation parameters (ICC + baseline tables)
  - Full bibliography
- 20 pages, all 10 figures, compiles cleanly

### Coauthor package
- Created `share_with_coauthor/` with single code file (`qcf_analysis.py`), one data file (`villages_clean.csv`), PDF, and numbered figures
- Code is self-contained: change ROOT path and run

### Files
| File | Description |
|---|---|
| `raw/villages_clean.csv` | Clean village data with population estimates |
| `raw/villages_with_clusters.csv` | Village data with cluster + arm assignments |
| `code/plots.py` | Village maps (4 plots) |
| `code/build_village_data.py` | Merges village + population data |
| `code/build_clusters.py` | Cluster construction + randomization |
| `code/power_calculations.py` | Power calcs + randomization plots (6 plots) |
| `drafts/QCF_Uganda.tex` | Paper draft |
| `drafts/references.bib` | Bibliography |
| `share_with_coauthor/` | Self-contained package for coauthor |

### Open items
- 15 villages still missing GPS coordinates (need field collection)
- Baseline data will update power calculation parameters
- Literature review section is a placeholder
- Q2 power is tight — may need to discuss with QCF whether exploratory framing is acceptable

---

## Session 3: April 28, 2026

### Randomization redesign
- Revisited the Session 2 clustering approach (22 clusters at 3km with manual splits)
- Identified that `est_hh_per_village` is not a true village-level variable — it's `parish_total_hhs / parish_n_villages`, constant within parish — so it cannot be used for stratification
- Evaluated stratification options: district is the only viable stratification variable given available data
- Parish cannot be used for stratification because 14 of 39 geographic clusters span multiple parishes

### New clustering: 1km threshold
- Switched from 3km manual clusters to **1km automatic clusters** (complete linkage hierarchical clustering)
- Result: **39 clusters (14 Amuria + 25 Bulambuli)** — nearly doubles the number of randomization units vs the 22-cluster design
- 14 clusters span multiple parishes, confirming parish boundaries don't respect geographic proximity in Bulambuli
- Cluster sizes range from 1 to 13 villages (median 2)

### Dropped villages (15, all Bulambuli — missing GPS)

| Parish | Villages |
|--------|----------|
| Buluganya | Bwakuye, Nakakyele, Namakyele |
| Mabugu | Disi A, Disi B |
| Namunane | Namagungu |
| Nataba | Manyololo, Mashelusi, Nataaba, Zessosomi |
| Gamatimbei | Marama T.C |
| Kisekye | Indaiga, Rungodo |
| Lusaso | Gamashelo |
| Namisuni | Nalufudu |

- Final sample: **119 villages in 39 clusters**
- Notable: 4 of 6 Nataba parish villages are missing — parish nearly unrepresented

### Final randomization (source of truth)
- Stratified by **district**, balanced allocation across 3 arms (seed=2026)
- Each cluster = one baraza → **39 barazas total**

| | G1: Standard early | G2: Adaptation+plus | G3: Standard delayed | Total |
|---|---|---|---|---|
| Amuria | 5c, 6v | 5c, 5v | 4c, 5v | 14c, 16v |
| Bulambuli | 9c, 43v | 8c, 24v | 8c, 36v | 25c, 103v |
| **Total** | **14c, 49v** | **13c, 29v** | **12c, 41v** | **39c, 119v** |

- Village counts are imbalanced across arms due to variable cluster sizes — re-randomization could improve this

### Data pipeline
- Created `process/` folder — raw data is never modified
- Exported `process/villages_randomized.csv`: 119 villages with cluster assignments, arm, group (G1/G2/G3), arm labels, and empty `baseline_month` column for programs team

### Plots
- Created `plots/randomization/geo_clusters_1km_39.png`: cluster identity map (colored by cluster ID, sized by est. HH/village) — intermediate step showing cluster construction
- Created `plots/randomization/randomization_1km_39.png`: **final randomization map** (colored by treatment arm, G1/G2/G3) — this is the current source-of-truth visualization for the design

### Communication to programs team (sent April 28)
Message sent to Samantha (ML), Moshi Israel, Michael (MOG) requesting:
1. **Village list validation** — are 119 villages correct? Any missing or to be excluded?
2. **Dropped villages** — should the 15 excluded villages be included? If yes, share GPS coordinates
3. **Operational feasibility** — can you run 39 barazas (one per cluster, up to 13 villages per baraza)?
4. **Baseline timing** — fill in `baseline_month` column in attached file; staggered enrollment is fine

Attached: `villages_randomized.csv`

### Files
| File | Description |
|---|---|
| `process/villages_randomized.csv` | Randomized village data (119 villages, 39 clusters, 3 arms) |
| `code/plot_clusters_1km.py` | Clustering, randomization, export, and both plots |
| `plots/randomization/geo_clusters_1km_39.png` | Cluster identity map (intermediate — shows cluster construction) |
| `plots/randomization/randomization_1km_39.png` | **Final randomization map by treatment arm (source-of-truth visualization)** |

### Open items
- Awaiting programs team confirmation on village list, 39 barazas feasibility, and baseline timing
- 15 villages still need GPS coordinates or formal exclusion decision
- Village count imbalance across arms — consider re-randomization
- Power calculations need updating for 39-cluster design (vs previous 22-cluster)
- Baseline data collection will update power calculation parameters

---

## Session 4: April 30, 2026

### Plus components: Sub-arm 2b (Adaptation Aspirations Planning)

#### Literature review
Read and synthesized 5 papers on aspirations interventions:
1. **Orkin et al. (2023)** — 80-min aspirations + planning workshop cross-randomized with GD cash in Kenya. Workshop alone: +22% productive inputs, +11% revenue. But workshop + cash ≈ cash alone (cash itself raises aspirations, crowding out the workshop). Full exercise script in Appendix C.2: best possible selves → goal-setting → implementation intentions → obstacle anticipation → mental contrasting. Participants drew goals, received calendar + sticker.
2. **Macours & Vakis (2016)** — Nicaragua CCT. Exposure to successful female leaders sustained higher investments 2 years post-program. Mechanism: social interaction, not structured exercise.
3. **McKenzie, Mohpal & Yang (2021)** — **Cautionary tale.** Philippines RCT, 8-session "dream big" aspirations treatment. Participants achieved only 5% of savings goals → frustration → 15% less borrowing, 37% less business investment, reduced locus of control. Aspirations set too high backfire.
4. **Beaman, Duflo, Pande & Topalova (2012)** — India, female leadership quotas. Gender gap in aspirations closed 25–32% after two election cycles with female leader. Role model effect, not policy changes. Requires sustained exposure.
5. **Macours & Vakis (2009)** — Working paper version of 2016 paper. Same findings measured during intervention.

#### Design decisions
- Climate-specific framing (not domain-general like Orkin et al.)
- Script explicitly mentions the cash transfer as a resource
- Written Planning Sheet given to recipient (goal + first step)
- FO records all answers (goal, first step, obstacle, backup, motivation) for research data
- 10-minute target duration, 5 steps
- No video/vignette — purely self-directed, FO is facilitator only
- Plain English script, FO translates on the fly
- Feasibility check in goal-setting step to prevent frustration effect (McKenzie et al.)
- "Do NOT encourage big dreams" explicitly in FO instructions

#### Documents created
| File | Description |
|---|---|
| `pluses/aap/aap_field_script.md` | Full field script: FO instructions + 5-step exercise + Planning Sheet template + data fields |
| `pluses/aap/aap_field_script.docx` | Word doc version of the script (for sharing with team) |
| `pluses/aap/aap_fo_training_guide.md` | 90-min FO training session: agenda, script walkthrough, 6 common mistakes, 2 practice scenarios (Bulambuli/Amuria), debrief checklist, quick reference card |
| `pluses/aap/aap_design_log.md` | Design log: plan, literature summary, design decisions, known risks, resolved questions |

#### Known risks (to pre-register)
- **Crowding-out**: Cash alone raises aspirations (Orkin et al.). 2b delivered after token, before LLS — cash may already activate the mechanism. Null result on 2b vs. 2c is consistent with this.
- **Frustration**: If goals set too high, exercise could backfire (McKenzie et al.). Script includes feasibility check to mitigate.
- **Low dosage**: 10 min, no video, no group, no follow-up = ~1/8 of Orkin et al.'s 80-min workshop. Effect sizes, if any, will be smaller.

#### Papers renamed and organized in `pluses/aap/`
- `Orkin_et_al_2023_Aspirations_Planning_Workshop_Kenya.pdf`
- `Macours_Vakis_2016_Leaders_Aspirations_Investment_Nicaragua.pdf`
- `Macours_Vakis_2009_Social_Interactions_Aspirations_Nicaragua.pdf`
- `McKenzie_Mohpal_Yang_2021_Aspirations_Frustration_Philippines.pdf`
- `Beaman_Duflo_Pande_Topalova_2012_Female_Leadership_Aspirations_India.pdf`

#### Communication
- Sent AAP script (Word doc) to team for feedback, explaining the design, what it's based on (Orkin et al. adapted, McKenzie et al. frustration safeguard), and requesting input on: script flow, 10-min feasibility, Planning Sheet printing, FO instructions, anything missing
- Training guide ready to share once script is finalized

### Key context for next session
- **To get up to speed**: read `session_logs/research_journal.md` — contains full program reference (MELP, design, indicators, parameters) and all session logs
- **AAP design details**: read `pluses/aap/aap_design_log.md` — contains all design decisions, literature, risks, resolved questions, and open items
- **Current script**: `pluses/aap/aap_field_script.md`
- **FO training**: `pluses/aap/aap_fo_training_guide.md`
- **Randomization source of truth**: Session 3 in this journal (39 clusters, 119 villages, district-stratified)
- **Raw data**: `data/raw/villages_clean.csv` (134 villages, 15 missing GPS)
- **Processed data**: `process/villages_randomized.csv` (119 villages with arm assignments)

### Open items
- **Awaiting feedback** on AAP script from team
- Sub-arm 2a (Historical Climate Information SMS) content still needs design — deadline ~June 18
- Planning Sheet needs physical design/printing
- Awaiting programs team confirmation on village list, barazas, and baseline timing (from Session 3)
- Power calculations need updating for 39-cluster design
- Q3 power for household-level comparison needs recalculation with updated Group 2 village counts (13 clusters, 29 villages)
- LaTeX draft (`drafts/QCF_Uganda.tex`) needs updating from 22-cluster to 39-cluster design

---

## Session 5: May 3, 2026

### Allocation ratio fix
- Discovered that Session 3 randomization code used **1:1:1 allocation** (14/13/12 clusters) instead of the intended **2:1:2 ratio** from the MELP and Session 2 design
- Root cause: `np.tile([1, 2, 3], ...)` in `plot_clusters_1km.py` tiled equally instead of respecting the 2:1:2 ratio
- Fixed to exact proportional assignment: `floor(n/5)` for G2, remainder split evenly between G1 and G3
- **Final allocation: 16 / 7 / 16 clusters (G1/G2/G3)**

| | G1: Standard early | G2: Adaptation+plus | G3: Standard delayed | Total |
|---|---|---|---|---|
| Amuria | 6c, 6v | 2c, 3v | 6c, 7v | 14c, 16v |
| Bulambuli | 10c, 37v | 5c, 29v | 10c, 37v | 25c, 103v |
| **Total** | **16c, 43v** | **7c, 32v** | **16c, 44v** | **39c, 119v** |

- Rationale: maximizes Q1 power (G1 vs G3, 16 vs 16 clusters) where cluster-level variation matters most; Q3 (within G2) is household-level so fewer G2 clusters is acceptable

### Power calculations updated for 39-cluster / 16-7-16 design

| Question | Comparison | Clusters/arm | MDE (continuous) | MDE (binary) |
|---|---|---|---|---|
| **Q1** (cash) | G1 vs G3 | 16 vs 16 | 0.25–0.36 SD | 10–15 pp |
| **Q2** (baraza) | G1 vs G2 | 16 vs 7 | 0.37–0.55 SD | underpowered |
| **Q3** (plus) | 2a vs 2b vs 2c | HH-level, ~313/arm | 0.19 SD | 7.8 pp |

- Substantial improvement over old 22-cluster design (was 0.30–0.45 SD for Q1)
- Q2 remains exploratory — labeling effects typically 0.10–0.25 SD (Thomas 2020)
- Weighted avg HH surveyed/cluster: 29.3

### Missing-GPS villages
- 15 Bulambuli villages with missing coordinates now **included** in `QCF_cluster_village_assignation.csv` with `note` = "Programs getting the latitude and longitude"
- Previously these were silently dropped — now programs team can see the full 134-village list

### Code consolidation
- Merged all scripts into single `02-code/qcf_analysis.py`: data → clustering → randomization → export → power calculations → plots
- Old scripts archived in `02-code/archive/` with chronological numbering:
  - `01_s1_build_village_data.py`
  - `02_s1_village_maps_and_spillover_demos.py`
  - `03_s2_manual_clusters_3km_22.py`
  - `04_s2_power_calcs_22_clusters.py`
  - `05_s3_auto_clusters_1km_39.py`

### Data file renames
- `villages_clean.csv` → `QCF_raw_clean_list.csv`
- `villages_randomized.csv` → `QCF_cluster_village_assignation.csv`
- Dropped `villages_with_clusters.csv` (was `villages_clean.csv` + stale Session 2 cluster columns)

### LaTeX draft v2
- Created `QCF_region_assignment_v2.tex` (v1 archived)
- Moved to appendix: Fig 1 (villages_all), Figs 5–7 (geo clustering at 1/2/3 km), Fig 8 (22-cluster assignment)
- Reordered: Geographic Clustering now before Spillover Problem
- Updated Section 3.3.3 (Cluster Assignment): 1km, 39 clusters, new figure
- Updated Section 3.3.4 (Randomization): 2:1:2, new figure + allocation summary table with notation note
- Updated Section 3.4 (Power): all MDE numbers for 16 clusters/arm
- Updated estimation equations: cluster counts (16, 16 vs 7, ~313 HH/sub-arm)
- Removed seed from all plot titles and figure captions
- Compiles cleanly with bibtex (20 pages)

### Presentation slides created
- `QCF_Visual_Arms_Updated.pptx` — three-arm staggered rollout with 16/7/16 allocation
- `QCF_Outcomes_Measurement.pptx` — why we measure short-term behavioral outcomes, mapped to theory of change

### Project folder reorganization
```
qcf/
├── 00-intial docs/
├── 01-data/
│   ├── raw/QCF_raw_clean_list.csv
│   └── process/QCF_cluster_village_assignation.csv
├── 02-code/
│   ├── qcf_analysis.py
│   └── archive/
├── 03-outputs/plots/
│   ├── clustering/       ← active cluster + randomization maps
│   ├── power/            ← MDE curves
│   ├── spillover-demos/  ← illustrative plots for draft
│   └── archive/          ← old 22-cluster plots
├── 04-pluses-scripts/
├── 05-session_logs/
├── 06-drafts/
│   ├── QCF_region_assignment_v2.tex
│   ├── references.bib
│   ├── figures/
│   └── archive/version_April20_2026/
└── 07-share_with_coauthor/
```

### Key context for next session
- **To get up to speed**: read `05-session_logs/research_journal.md`
- **Randomization source of truth**: this session (39 clusters, 16/7/16, 119 villages)
- **Single code file**: `02-code/qcf_analysis.py`
- **Raw data**: `01-data/raw/QCF_raw_clean_list.csv`
- **Processed data**: `01-data/process/QCF_cluster_village_assignation.csv`
- **Current draft**: `06-drafts/QCF_region_assignment_v2.tex`
- **AAP design**: `04-pluses-scripts/aap/aap_design_log.md`

### Open items
- **Awaiting feedback** on AAP script from team
- **Awaiting programs team confirmation** on village list, 39-baraza feasibility, baseline timing, and 15 missing GPS villages
- Sub-arm 2a (Historical Climate Information SMS) content still needs design — deadline ~June 18
- Planning Sheet needs physical design/printing
- Programs team received old 1:1:1 allocation file on April 28 — **need to send updated 16/7/16 file** and confirm no operational planning was based on old assignments
- Baseline data will update power calculation parameters
