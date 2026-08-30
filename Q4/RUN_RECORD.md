# Q4 — Run Record (Partner A)

| Field | Value |
|---|---|
| Partner A | Vrishab A V (DA24B033) |
| Partner B | VNV Sri Harsha (DA24B034) |
| **Q4 commit SHA** | `91f6346042127b0648eb770f2c3c79c464097160` |
| **MLflow run_id** | `c806a73763e144b7834aad916e6ee5df` |
| Experiment | `q4-capstone` |
| Run name | `q4-partnerA-seed42` |
| Registered model | `mnist-mlp` version 1 |
| Promotion | `stage=Staging` (classic stages API) |

## Recorded metrics

| Metric | Value |
|---|---|
| accuracy | 0.9485 |
| f1_macro | 0.9481 |

## What was logged

| Kind | Keys |
|---|---|
| Parameters | `seed`, `learning_rate_init`, `batch_size`, `hidden_layer_sizes`, `max_iter`, `data_path` |
| Per-epoch metrics | `train_loss`, `val_accuracy` (logged with `step=`) |
| Final metrics | `accuracy`, `f1_macro` |
| Tags | `git_commit`, `team` |
| Artifact | `model/` (sklearn flavour, logged via `mlflow.sklearn.log_model`) |

## Environment actually used (Partner A)

    python           3.14.4
    scikit-learn     1.9.0
    mlflow           3.15.1
    numpy            2.5.2
    pandas           2.3.3
    dvc              3.67.1
    OS               Ubuntu (WSL2)

Partner B should build from `environment.yml` (Python 3.11) or `requirements.txt`. The
scientific package versions are pinned identically; only the interpreter minor version
differs.

## Dataset

| Field | Value |
|---|---|
| Path | `Q4/data/mnist_subset.npz` |
| md5 | `b50dac761e0135c47104e195c592c9db` |
| Shape | X = (10000, 784) uint8, y = (10000,) int64 |
| DVC pointer | `Q4/data/mnist_subset.npz.dvc`, committed in the SHA above |

The DVC cache object for this file is committed to the repository, so `git clone` followed by
`dvc checkout` restores the data with no remote access and no credentials.

The array is stored as **uint8** and rescaled by `/255.0` exactly once, inside `train.py`.
(An earlier `make_dataset.py` normalised at save time as well, which would have double-scaled
the inputs and silently collapsed accuracy to roughly chance level.)

## Reproduction tolerance

**±0.005 absolute accuracy.** `MLPClassifier` with a fixed `random_state` on a fixed split is
deterministic for a given scikit-learn version and BLAS configuration; the tolerance covers
BLAS threading differences across machines and the interpreter minor-version difference.

## Self-verification (Partner A)

A clean clone into `/tmp` reproduced the run exactly on the same machine: dataset md5 matched,
`accuracy = 0.9485`, `f1_macro = 0.9481`, delta 0.0000.

## Note on model promotion

MLflow 3.15.1 still accepts `transition_model_version_stage` but emits a deprecation warning;
stages are slated for removal in favour of aliases. `train.py` attempts the classic stages API
first and falls back to `set_registered_model_alias(alias="staging")`. The recorded run used
the classic stages API, so the registry shows `mnist-mlp` v1 in **Staging**.

## Partner B result

| Field | Value |
|---|---|
| Verifier | VNV Sri Harsha (DA24B034) |
| Partner B run_id | `6894dd604b6a408cb88ec18acf27f1c0` (his own tracking server) |
| Reproduced accuracy | 0.9520 |
| Reproduced f1_macro | 0.9519 |
| Delta (accuracy) | +0.0035 |
| Delta (f1_macro) | +0.0038 |
| **Verdict** | **MATCH** — inside the stated ±0.005 tolerance |
| Dataset md5 observed | `b50dac761e0135c47104e195c592c9db` — byte-identical |

**Explanation of the discrepancy.** The seed, the split and the dataset bytes were identical,
so the difference is not in the data or the sampling. Two environment differences remain:
Partner B ran on Python 3.14 built from `requirements.txt` rather than the 3.11 pinned in
`environment.yml`, and the two machines have different BLAS libraries and thread counts.
`MLPClassifier`'s minibatch gradient sums are floating-point order-dependent, so a different
threading layout changes the low-order bits of the weight updates and can move the final
accuracy by a few samples out of 2000 (0.0035 ≈ 7 test samples). Pinning
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1` on both machines would test this
directly; it was not run.

Partner B's full report: [`PARTNER_VERIFICATION.md`](PARTNER_VERIFICATION.md), authored and
committed by him.

## Verification note written back to this run

Partner B ran `log_partner_note.py` against Partner A's tracking server over the local
network, writing these tags onto run `c806a73763e144b7834aad916e6ee5df`:

| Tag | Meaning |
|---|---|
| `partner_verification` | verdict string (MATCH, with the tolerance) |
| `verified_by` | VNV Sri Harsha (DA24B034) |
| `reproduced_accuracy` | 0.9520 |

Screenshot: `evidence/04_partnerA_verification_tags.png`.
