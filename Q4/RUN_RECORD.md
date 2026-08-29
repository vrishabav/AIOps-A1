# Q4 — Run Record (Partner A)

Fill every angle-bracket field after your `train.py --register` run completes.
This file is the entire contract between you and your partner.

| Field | Value |
|---|---|
| Partner A | Vrishab A V (DA24B033) |
| Partner B | <name (rollno)> |
| **Q4 commit SHA** | `<git rev-parse HEAD>` |
| **MLflow run_id** | `<run_id printed by train.py>` |
| Experiment | `q4-capstone` |
| Registered model | `mnist-mlp` version `<n>`, stage **Staging** |

## Recorded metrics

| Metric | Value |
|---|---|
| accuracy | `<0.xxxx>` |
| f1_macro | `<0.xxxx>` |

## Environment actually used

```
python           <e.g. 3.11.9>
scikit-learn     <e.g. 1.5.2>
mlflow           <e.g. 3.1.0>
numpy            <e.g. 1.26.4>
OS               <e.g. Ubuntu 22.04 on WSL2>
```

## Dataset

| | |
|---|---|
| Path | `Q4/data/mnist_subset.npz` |
| md5 | `<md5sum output>` |
| Shape | X = (10000, 784) uint8, y = (10000,) int64 |
| DVC pointer | `Q4/data/mnist_subset.npz.dvc`, committed in the SHA above |

## Reproduction tolerance

Stated tolerance: **±0.005 absolute accuracy**.

`MLPClassifier` with a fixed `random_state` on a fixed split is deterministic
for a given scikit-learn version; the tolerance covers BLAS threading and minor
version differences.

## Partner B result

| Field | Value |
|---|---|
| Reproduced accuracy | `<0.xxxx>` |
| Delta | `<+/-0.xxxx>` |
| Verdict | `<MATCH / MISMATCH>` |
| Partner run_id | `<run_id>` |
| Notes | `<any discrepancy>` |
