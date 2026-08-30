# Q4 — Partner B Verification Report

| Field | Value |
|---|---|
| Verifier (Partner B) | VNV Sri Harsha (DA24B034) |
| Repository owner (Partner A) | Vrishab A V (DA24B033) |
| Branch checked out | `main` |
| Commit at time of run | `85151ac95ae1ecea2c67d439e3ea213653d3f64e` |
| Q4 reference commit | `91f6346042127b0648eb770f2c3c79c464097160` (ancestor of `main`; `train.py` and the dataset pointer are unchanged between the two) |
| Date | 2026-08-29 |

## Procedure followed

Only the commands permitted by the assignment were used. No information about
the environment or the dataset was requested from Partner A.

1. `git clone` of the repository, then worked on `main`.
2. `dvc checkout` — the dataset was restored from the DVC cache committed in the
   repository. No `dvc pull`, no remote credentials, no network access needed
   for the data.
3. Dataset integrity verified by md5.
4. Environment built from the repository's `requirements.txt` into a fresh
   virtualenv.
5. `python train.py --seed 42 --run-name repro-by-partnerB` executed with no
   modifications to the script.

## Dataset verification

| | |
|---|---|
| Path | `Q4/data/mnist_subset.npz` |
| Expected md5 (from `RUN_RECORD.md`) | `b50dac761e0135c47104e195c592c9db` |
| Observed md5 | `b50dac761e0135c47104e195c592c9db` |
| Result | **MATCH — byte-identical** |

## Result

| Metric | Partner A recorded | Reproduced | Delta |
|---|---|---|---|
| accuracy | 0.9485 | 0.9520 | +0.0035 |
| f1_macro | 0.9481 | 0.9519 | +0.0038 |


**Both runs differed by 0.0035 in accuracy, which is within the acceptable stated tolerance of 0.005 for reproducible runs on an MLP.**

Supporting values from the reproduction run:

- final `train_loss` = 0.0037326818777041
- best `val_accuracy` = 0.95625
- all six logged parameters identical to Partner A's run
  (`seed=42`, `learning_rate_init=0.003`, `batch_size=32`,
  `hidden_layer_sizes=(128,)`, `max_iter=30`,
  `data_path=data/mnist_subset.npz`)

## Environment used for reproduction

| Package / System | Version |
|---|---|
| Python | 3.14.4 |
| scikit-learn | 1.9.0 |
| MLflow | 3.15.1 |
| NumPy | 2.5.2 |
| OS | Ubuntu 26.04 LTS |

## MLflow evidence

| | |
|---|---|
| Reproduction run_id (Partner B's server) | `6894dd604b6a408cb88ec18acf27f1c0` |
| Experiment | `q4-capstone` |
| `git_commit` tag on that run | `85151ac95ae1ecea2c67d439e3ea213653d3f64e` |
| Note written to Partner A's run | `c806a73763e144b7834aad916e6ee5df` |
| Method | Live cross-machine write via `log_partner_note.py` against Partner A's tracking server over the local network |
| Tags written | `partner_verification`, `verified_by`, `reproduced_accuracy` |

## Conclusion

Reproduced; code, dataset and environment specification were used and made to get the same results on a different device.
