
# Q4 — Run Record (Partner A)

| Field | Value |

|---|---|

| Partner A | Vrishab A V (DA24B033) |

| Partner B | Harsha (DA24B034) |

| **Q4 commit SHA** | `91f6346042127b0648eb770f2c3c79c464097160` |

| **MLflow run_id** | `c806a73763e144b7834aad916e6ee5df` |

| Experiment | `q4-capstone` |

| Registered model | `mnist-mlp` version 1 |

| Promotion | `stage=Staging` (classic stages API) |

## Recorded metrics

| Metric | Value |

|---|---|

| accuracy | 0.9485 |

| f1_macro | 0.9481 |

## Environment actually used

    python           3.14.4

    scikit-learn     1.9.0

    mlflow           3.15.1

    numpy            2.5.2

    pandas           2.3.3

    OS               Ubuntu (WSL2)

Partner B should build from `environment.yml` (python 3.11) or

`requirements.txt`. The scientific package versions are pinned identically;

only the interpreter minor version differs.

## Dataset

| | |

|---|---|

| Path | `Q4/data/mnist_subset.npz` |

| md5 | `b50dac761e0135c47104e195c592c9db` |

| Shape | X = (10000, 784) uint8, y = (10000,) int64 |

| DVC pointer | `Q4/data/mnist_subset.npz.dvc`, committed in the SHA above |

The DVC cache object for this file is committed to the repository, so

`git clone` followed by `dvc checkout` restores the data with no remote access

and no credentials.

## Reproduction tolerance

**+/-0.005 absolute accuracy.** `MLPClassifier` with a fixed `random_state` on a

fixed split is deterministic for a given scikit-learn version; the tolerance

covers BLAS threading and minor version differences.

## Self-verification

A clean clone into `/tmp` reproduced the run exactly:

dataset md5 matched, `accuracy = 0.9485`, `f1_macro = 0.9481`, delta 0.0000.

## Note on model promotion

MLflow 3.15.1 still accepts `transition_model_version_stage` but emits a

deprecation warning; stages are slated for removal in favour of aliases.

`train.py` attempts stages first and falls back to

`set_registered_model_alias(alias="staging")`. Both mechanisms are covered in

Lecture 3, section 4.3.

## Partner B result

| Field | Value |

|---|---|

| Reproduced accuracy | `<0.xxxx>` |

| Delta | `<+/-0.xxxx>` |

| Verdict | `<MATCH / MISMATCH>` |

| Partner run_id | `<run_id>` |

| Notes | `<any discrepancy>` |

