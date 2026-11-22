# Detecting Fake Websites with Machine Learning

F21DL Data Mining and Machine Learning — Group Coursework, Group 15.

## What is here

| Path | Contents |
|---|---|
| `Notebook/DataMining&MachineLearning_Coursework_01.ipynb` | Steps 01–09: questions and hypotheses (R1), cleaning, graphs, feature selection, clustering, classical models, decision tree, neural networks, final comparison (R2–R4) |
| `Notebook/Phishing_Image_CNN_Pipeline.ipynb` | The screenshot experiments (RQ4 / H4): acquisition, cleaning, four convolutional networks |
| `Documents/Report/main.tex` | The report, IEEEtran journal class, A4 |
| `Datasets/PhiUSIIL_Phishing_URL_Dataset.csv` | The tabular dataset, committed because it is 57 MB |
| `Guide/` | The module brief and the dataset licence list |

## The datasets

Three published datasets, across two views of the problem. Full citations are in the report's
bibliography; nothing here is redistributed beyond the single CSV that is committed.

### 1. Tabular — PhiUSIIL Phishing URL Dataset

- Source: UCI Machine Learning Repository, ID 967.
- Reference: A. Prasad and S. Chandra, *PhiUSIIL: A diverse security profile empowered phishing URL
  detection framework based on similarity index and incremental learning*, Computers & Security,
  vol. 136, Art. no. 103545, 2024.
- Licence: CC BY 4.0.
- Shape: 235,795 rows × 56 columns — 50 numeric features, 4 text columns (`URL`, `Domain`, `TLD`,
  `Title`), 1 identifier (`FILENAME`) and the `label` target.
- Class balance: 134,850 legitimate (label 1), 100,945 phishing (label 0), so always answering
  "legitimate" scores 57.19 %.
- Provenance: legitimate half from the Tranco top one million domains, phishing half from public
  reports. A snapshot, not a live view.

### 2. Screenshots, primary — Zenodo, Phishing and Legitimate Websites Dataset

- Source: Zenodo, record 23477065, version 2.0, published 19 October 2026.
- Version DOI: `10.5281/zenodo.23477065`. Concept DOI (all versions): `10.5281/zenodo.21379701`.
- Reference: D. K. Yadav, M. Tejash, S. Panda, P. Mishra, S. Nayak and A. A. Sekh, *Phishing and
  Legitimate Websites Dataset*, version 2.0, Zenodo, 2026.
- Licence: CC BY 4.0 — attribution and a licence link are required.
- Archive: `Phishing dataset V2.0.zip`, 4.48 GB, ZIP64, laid out as
  `Phishing dataset/image/{legitimate,phishing}/*.png`.
- Screenshots: 21,311 (12,241 legitimate, 9,070 phishing). Counts verified against the archive's own
  central directory.

Version 1.0 of the same record (DOI `10.5281/zenodo.21379702`) contains only 7,062 screenshots, of
which 1,777 are phishing. It is **not** the version used here, because it cannot support the
8,000-per-class balance in Step 04.

### 3. Screenshots, supplementary — Phishpedia benchmark

- Source: the Phishpedia project, `phish_sample_30k.zip` and `benign_sample_30k.zip`.
- Reference: Y. Lin *et al.*, *Phishpedia: A hybrid deep learning based approach to visually
  identify phishing webpages*, USENIX Security 2021.
- Licence: Custom / research use only. Not redistributed, and not usable commercially.
- Screenshots: 70,429 (40,922 legitimate, 29,507 phishing).

The two screenshot sources give 91,740 raw images, 61,375 after cleaning.

## The report

`Documents/Report/main.tex` builds `Documents/Report/F21DL_Group15_Report.pdf` with `./build.sh`
(two `pdflatex` passes). The layout is chosen to meet the submission rules in the module brief:

| Requirement | How it is met |
|---|---|
| IEEE template | `IEEEtran` journal class, IEEE numeric citations, `Fig. n` / `Table I` numbering |
| Maximum 6 pages of body | Body runs pages 2–7; title page, references and appendices fall outside the limit |
| A4, margins ≥ 1.27 cm | A4 throughout; measured margins are 1.43 cm (left/right), 1.92 cm (top), 1.51 cm (bottom) |
| Minimum font size 11 pt | Body, abstract, captions, tables and references are all set at 11 pt |
| Required sections | Introduction, Related Work, Dataset Description and Analysis, Experimental Setup, Results, Discussion, Conclusion |
| Contribution appendix | Appendix C, taken from the notebook header and the commit history |

Every figure is regenerated from the saved outputs of the two notebooks, so the numbers in the report and
the numbers in the notebook cannot drift apart. Three figures and eight tables appear; the report keeps
only the visuals that carry an argument, as the brief asks.

## Reproducing

```bash
python3 -m pip install -r requirements.txt
jupyter lab Notebook/
```

Both notebooks are run top to bottom.

- The tabular notebook needs `Datasets/PhiUSIIL_Phishing_URL_Dataset.csv`, which is committed.
- The screenshot notebook fetches Zenodo record 23477065 by DOI at Step 02, so no manual download and
  no cloud-drive account are needed. It stores images in `Datasets/combined_images/`, which is
  deliberately outside version control. The download is about 4.5 GB; on a slow link, fetch the
  archive once and leave it in the project root, and Step 02 will reuse it.
- Setting `USE_PHISHPEDIA = False` in Step 02 runs on the Zenodo record alone. The corpus then falls
  to 21,311 images and every figure from Step 04 onward must be regenerated.

## Notes on reuse

- All three datasets are licensed for research reuse and all are attributed in the report.
- The working report file is `Documents/Report/main.tex`; build it from that directory.
- Backups made while updating the dataset references end in `.orig.bak`.
