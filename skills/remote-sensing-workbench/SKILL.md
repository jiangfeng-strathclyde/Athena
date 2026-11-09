---
license: MIT
name: remote-sensing-workbench
description: >-
  Remote sensing image understanding and workstation skills for Earth observation machine learning missions: open data sources and licensing verification, pre-processing and leak-proof classification practices, assessment of calibres and multiples seed Agreement, common baseline spectra, periodical writing./Earth observation/Geospatial ML for the selection of topics, experimental design, baseline selection, assessment or writing.
version: 1.0.0
---

# Remote Sensing Workbench（Remote sensing/Earth observation ML Workstations)

## Trigger scene

- Remote sensing image classification/Split/Change detection/Reverse/Methodology and experimental design of tasks such as time series predictions;
- Select open data sets, pre-processing tubes, space/Time-sharing;
- (b) The establishment of a baseline spectrometry for the assessment of the caliber and comparison of the indicators;
- Face TGRS/GRSL/ISPRS/RSE It's the writing of periodicals and charts.

## 1. Data sources and licences (cantoned before use)

| Category | Common open source | Verification point |
|---|---|---|
| Optical Multispectral | Sentinel-2、Landsat 8/9、MODIS | Open permission; cloud cover version; processing level (L1C/L2A） |
| SAR | Sentinel-1、ALOS-2（by project) | Polarization/Orbital orientation consistency; spot noise disposal statements |
| High speed./Topography | SRTM、Copernicus DEM | Resolution & Baseline (EGM96/EGM08） |
| Meteorological/Hydrological | ERA5、GPM、GNSS Open site network | re-analyse version; time resolution and re-sampling |
| Description/Benchmark | Open competitions and benchmark data sets | Training/Test whether the division is official; prohibition of mixing across divisions |

Red wire:**Check the permissions and versions before any data source is written to the paper**；The versions are considered to be different data sets and not mixed.

## 2. Pre-treatment and leak-proof separation

- Radiation/Geometric correction, coordinate system I (declaration) CRS (b) In relation to re-sampling methods;
- Division must be space-proof from the relevant leaks: priority **scene-held-out / Area set aside**，instead of random pixel slices; time-series tasks **Time set.**；Both are reported separately;
- patch Crop needs to state overlap rates and boundary processing; statistics (average)/(b) Calculated only within training discounts;
- Damage/Cloud loss.-free Samples are excluded by pre-registration rules and the original rows are retained without fractions.

## 3. Assessment calibre

- Split/Classification:mIoU、F1、OA、Kappa (a) Simultaneous reporting;**patch Level and scene Separated calibres.**，Not mixed;
- Returns/Retro:RMSE/MAE/R² and indicates the unit and sample level;
- More seed（≥3）Report! mean ± std；Single seed The result can only be taken into account and noted;
- At least coverage against baseline spectrum: classic network (U-Net、DeepLabv3+、HRNet）+ Transformer Yes (%)SegFormer/Swin Yes)
  + The target journal is close. 2 The annual mainstream approach; absences are stated in terms of scope and cause.

## 4. Writing and charting agreement (periodical direction)

- Methodology stratification: overall network + Modular panels, based on the publication of papers in targeted periodicals;
- Qualitative result grid“Multiple rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows, rows”To match the two-column content; the chart follows the initial references in the body of the text;
- Study of narratives“Mechanism → Inherent meaning of structure → Mathematical nature → Indication → Empty/Frequency access.”(a) The chain organization methodology;
- No undefined symbols appear in the summary; conclusions such as complexity are expressed in natural languages.

## 5. Output

- `DATA_CARD.md`：Data source, version, permission, division, calibre statement;
- `EVAL_PROTOCOL.md`：Indicators, levels,seed Number, baseline spectrum and absence statement;
- List of chapter skeletons and graphs at the writing stage.

## Red wires (to be added to the warehouse's main red line)

- Parameters, coordinates, resolution of non-constructed sensors; markers without certainty UNCERTAIN and verification;
- No, I'm not. patch/scene、No, I'm not. campaign calibre; number of reports indicated hierarchy;
- You're not allowed to start a new training./New forwards; aircraft costs are reported before the list.

## Collaborative skills Retrieval `research-lit` / `semantic-scholar`；Chasing `novelty-check`；Experimental planning `experiment-plan`；
Chart `paper-figure` / `data-profile-and-plot`；Digital audits `paper-claim-audit`。
