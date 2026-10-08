# Gate 9.6 — Cold-replay test, without re-opening final holdout

Workflow: `.github/workflows/gate9-6-cold-audit.yml`.

A clean Linux/Windows environment downloads UCI with the known raw checksum,
regenerates **only 264 train + 88 validation** and checks frozen split hashes.
No `test.csv` file is produced or required.

It then executes the original experiment code (K2–8 × Raw/Log1p × 10 seeds,
**140 fits on train split only**, 630 adjusted Rand index pairs) in a
**temporary directory**, not into canonical `reports/`. A precise schema,
row-key, text and numeric comparison validates `runs.csv`,
`stability_pairs.csv`, `selection_evidence.csv` and the 14-row
`review_table.csv` against evidence frozen before the one-shot final test.

The only permitted `fit` calls are **candidate train-only replay**, in temp;
no D011 final model rebuild, no freeze, no final evaluation, and no
`data/processed/test.csv` creation or read. The Git diff guard checks that
`models/`, canonical experiment evidence and final-profile CSV/JSON remain
unchanged. Additional tests compare sklearn joblib to JSON nearest-centroid
predictions on **352 development only** and protect against retraining.

**Important limitation:** this verifies the ability to regenerate **development
evidence** and reuse the frozen model; it does **not** claim byte-for-byte
regeneration of `models/model.joblib` (that would require fitting a second
final model), nor does it re-evaluate the held-out test.

### Local run (new checkout)

```powershell
python -m pip install -r ml/requirements.txt
python -m ml.src.download_data
python -m ml.src.prepare_development_only
python -m pytest ml/tests/test_experiments.py ml/tests/test_review_experiments.py ml/tests/test_final_profile.py -q
python -m ml.src.verify_cold_repro
```

Do not run `ml:finalize` or `ml:freeze`. Check workflow result for
Windows and Linux before declaring a reproducibility gate PASS.
