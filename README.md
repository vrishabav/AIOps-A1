# DA3408 — AI Ops Lab · Module 1 Assignment

Experiment Management & Reproducibility · **Vrishab A V (DA24B033)**
Q4 partner: **VNV Sri Harsha (DA24B034)** — this repository is Partner A's; he acted as Partner B.

| Deliverable | Where |
|---|---|
| Write-up | [`writeup.pdf`](writeup.pdf) |
| Q1 answers | [`Q1/Q1_Answers.pdf`](Q1/Q1_Answers.pdf) |
| Q2 screenshot, analysis, logging code | [`Q2/Q2_Answers.pdf`](Q2/Q2_Answers.pdf) |
| Q3 rollback terminal output | [`Q3/transcript.txt`](Q3/transcript.txt) |
| Q4 run record & partner verification | [`Q4/RUN_RECORD.md`](Q4/RUN_RECORD.md), [`Q4/PARTNER_VERIFICATION.md`](Q4/PARTNER_VERIFICATION.md), [`Q4/evidence/`](Q4/evidence) |
| Demo video (Q2 + Q3) | [`Q2+Q3 Video.mp4`](Q2+Q3%20Video.mp4) — in this repo, no external access needed |
| AI use disclosure | [`AI_DISCLOSURE.md`](AI_DISCLOSURE.md) |

---

## Layout

```
Q1/Q1_Answers.pdf              Q1 answers
Q2/Q2_MNIST.ipynb              Q2 notebook, MLflow-instrumented (outputs saved)
Q2/Q2_Answers.pdf              Q2 deliverables
files.csv.dvc                  Q3 dataset pointer
Q3/transcript.txt              Q3 rollback proof
Q4/make_dataset.py             builds the 10k MNIST subset
Q4/train.py                    the tracked training run
Q4/log_partner_note.py         writes Partner B's note onto Partner A's run
Q4/data/mnist_subset.npz.dvc   dataset pointer, committed with train.py
Q4/PARTNER_INSTRUCTIONS.md     what Partner B was given, and nothing else
Q4/evidence/                   commit contents, authorship, MLflow screenshots
.dvc/                          DVC config + committed cache objects
```

`files.csv` and `Q4/data/mnist_subset.npz` are DVC-managed, so only their `.dvc` pointers are
in Git. Local MLflow state (`mlflow.db`, `mlruns/`) is machine-specific and not committed.

## Setup

```bash
mamba env create -f environment.yml && mamba activate aiops-m1
# or:  python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

`environment.yml` pins Python 3.11 as a floor; both the recorded run and Partner B's
reproduction were executed on 3.14.4 with the pinned package versions.

## Running each question

**Q2** - start a tracking server, then run the notebook top to bottom (experiment
`mnist-classifier`):

```bash
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 0.0.0.0 --port 5000
```

**Q3** —-the DVC cache objects for both dataset versions are committed, so this works from a
bare clone with no credentials:

```bash
dvc checkout;                     wc -l files.csv    # 2801  (v2)
git checkout v1 -- files.csv.dvc; dvc checkout
                                  wc -l files.csv    # 1801  (v1)
git checkout main -- files.csv.dvc && dvc checkout   # back to 2801
```

**Q4** — reproduce Partner A's run:

```bash
dvc checkout
md5sum Q4/data/mnist_subset.npz     # b50dac761e0135c47104e195c592c9db
cd Q4 && python train.py --seed 42  # accuracy 0.9485
```

Run `c806a73763e144b7834aad916e6ee5df` (experiment `q4-capstone`) was produced at commit
`91f6346`, which contains `train.py` and `Q4/data/mnist_subset.npz.dvc` together — see
[`Q4/evidence/q4_commit_contents.txt`](Q4/evidence/q4_commit_contents.txt). The model is
registered as `mnist-mlp` v1 in **Staging**. Partner B reproduced it at 0.9520 against a
pre-declared ±0.005 tolerance; details in `Q4/RUN_RECORD.md`.
