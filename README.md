# DA3408 — AI Operations Lab · Module 1 Assignment

**Experiment Management & Reproducibility**

| | |
|---|---|
| Student | Vrishab A V — **DA24B033** |
| Q4 partner | VNV Sri Harsha — **DA24B034** |
| Roles in Q4 | This repository is **Partner A**'s. Sri Harsha acted as **Partner B** and reproduced the run. |
| Demo video | *(link — see "Video" below)* |
| AI use disclosure | [`AI_DISCLOSURE.md`](AI_DISCLOSURE.md) |

---

## 1. What is in this repository

```
.
├── README.md                     you are here
├── AI_DISCLOSURE.md              AI use declaration (course Fair Use policy)
├── writeup.pdf                   the graded write-up (Q1 answers, Q2 analysis + screenshot)
├── environment.yml               conda/mamba environment
├── requirements.txt              equivalent pip pins (virtualenv route)
│
├── files.csv.dvc                 Q3 — DVC pointer for the versioned dataset
├── Q3/
│   └── transcript.txt            Q3 — terminal proof of the v2 → v1 → v2 rollback
│
├── Q1/answers.md                 Q1 — technical-debt diagnosis
├── Q2/
│   ├── Q2_MNIST.ipynb            Q2 — MLP + MNIST sweep, MLflow-instrumented (outputs saved)
│   ├── analysis.md               Q2 — written analysis
│   └── evidence/                 Q2 — MLflow run-comparison screenshot
│
├── Q4/
│   ├── make_dataset.py           builds the 10k-sample MNIST subset
│   ├── train.py                  the tracked training run (Partner A + Partner B both run this)
│   ├── log_partner_note.py       writes Partner B's verification note onto Partner A's run
│   ├── RUN_RECORD.md             Partner A's authoritative record of the run
│   ├── PARTNER_INSTRUCTIONS.md   what Partner B was given (and nothing else)
│   ├── PARTNER_VERIFICATION.md   Partner B's report — authored and committed by Sri Harsha
│   ├── data/mnist_subset.npz.dvc DVC pointer, committed in the same commit as train.py
│   └── evidence/                 commit contents, authorship log, MLflow screenshots
│
└── .dvc/                         DVC config + the committed cache objects (see §5)
```

Files **not** in Git, by design: `files.csv` and `Q4/data/mnist_subset.npz` are DVC-managed
(their `.dvc` pointers are tracked instead), the raw Q3 image folder is an intermediate,
and local MLflow state (`mlflow.db`, `mlruns/`) is machine-specific.

---

## 2. Setup

Either route works; both install identical scientific package versions.

**conda / mamba**

```bash
mamba env create -f environment.yml
mamba activate aiops-m1
```

**virtualenv**

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Verify:

```bash
python -c "import sklearn, mlflow, numpy, pandas; print(sklearn.__version__, mlflow.__version__, numpy.__version__, pandas.__version__)"
dvc --version
```

> **Note on the interpreter.** `environment.yml` pins Python 3.11; the recorded Q4 run was
> produced on Python 3.14.4. Every scientific package is pinned identically. Partner B built
> from `requirements.txt` on Python 3.14 — see `Q4/RUN_RECORD.md` for why this matters to the
> reproduced metric.

**Clone location.** Clone to a native Linux path. DVC's cache uses hardlinks, which a mounted
NTFS drive does not support.

---

## 3. Q1 — Technical debt diagnosis

Written answers: [`Q1/answers.md`](Q1/answers.md), also reproduced in `writeup.pdf`.

---

## 4. Q2 — MLflow experiment comparison

Six runs, sweeping **learning rate** × **batch size** on a 10,000-sample stratified MNIST
subset with an `MLPClassifier` (replacing the starter script's IRIS + RandomForest).

**To reproduce**

```bash
# from the directory holding your MLflow backing store — one line, no backslashes
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 0.0.0.0 --port 5000
```

The banner must read `Uvicorn running on http://0.0.0.0:5000`. Then run
`Q2/Q2_MNIST.ipynb` top to bottom. It logs to experiment `mnist-classifier`.

**Results** (all six runs; the notebook's saved outputs contain the same table)

| Run | learning_rate_init | batch_size | accuracy | f1_macro |
|---|---|---|---|---|
| mlp-lr0.003-bs32 | 0.003 | 32 | **0.9485** | 0.9481 |
| mlp-lr0.003-bs256 | 0.003 | 256 | 0.9395 | 0.9391 |
| mlp-lr0.0003-bs32 | 0.0003 | 32 | 0.9345 | 0.9339 |
| mlp-lr0.03-bs256 | 0.03 | 256 | 0.9325 | 0.9321 |
| mlp-lr0.0003-bs256 | 0.0003 | 256 | 0.9210 | 0.9201 |
| mlp-lr0.03-bs32 | 0.03 | 32 | 0.9125 | 0.9118 |

Analysis: [`Q2/analysis.md`](Q2/analysis.md). Screenshot of the MLflow run-comparison table:
`Q2/evidence/`. The logging code added to the starter script is the `train_and_log` function
in the notebook, also quoted in `writeup.pdf`.

---

## 5. Q3 — DVC data versioning and rollback

`files.csv` is a single-column CSV of file names extracted from the class `data.zip`.

| Version | Git tag | Lines | DVC md5 |
|---|---|---|---|
| v1 | `v1` (`750cf1f`) | 1801 (1800 rows + header) | `95839a3394a3b15774dc5d69795d09ad` |
| v2 | `v2` (`b7031ed`) | 2801 (2800 rows + header) | `b5cde184a192001267273ecfff86cd3f` |

**Remote.** An SSH remote is configured in `.dvc/config`
(`ssh://vrishab-av@localhost/home/vrishab-av/dvcstore`, with `keyfile` set). It is a private
host and is **not reachable by an evaluator**, so the DVC cache objects for both versions are
also committed to this repository. `dvc checkout` therefore works from a bare clone with no
credentials and no network access — no `dvc pull` needed.

**Rollback — verified from a fresh clone of this repository:**

```bash
git clone <this repo> verify && cd verify
dvc checkout
wc -l files.csv                        # 2801   (v2)

git checkout v1 -- files.csv.dvc       # move the pointer to v1
dvc checkout                           # DVC moves the bytes
wc -l files.csv                        # 1801   (v1) — matches v1 exactly

git checkout main -- files.csv.dvc && dvc checkout
wc -l files.csv                        # 2801   (back to v2)
```

Full terminal output: [`Q3/transcript.txt`](Q3/transcript.txt).

> **Why the pointer-only form.** A full `git checkout v1` also rewinds the working tree to a
> commit that predates the committed `.dvc/cache/` objects, removing them from disk — the
> subsequent `dvc checkout` then fails with a missing-cache error, and `dvc pull` cannot
> recover it because the remote is a private host. Checking out only `files.csv.dvc` moves the
> pointer while leaving the cache in place. It is the same two-step mechanism the assignment
> asks for — `git checkout` moves the *pointer*, `dvc checkout` moves the *bytes* — and it is
> the form used in the DVC documentation. The video demonstrates the full-tree variant on the
> original working copy, where the cache is present locally and both forms succeed.

---

## 6. Q4 — End-to-end reproducibility drill

**Partner A: Vrishab A V (DA24B033) — this repository.**
**Partner B: VNV Sri Harsha (DA24B034).**

### What Partner A did

```bash
cd Q4
python make_dataset.py                                   # 10k-sample MNIST subset, uint8
dvc add data/mnist_subset.npz
git add data/mnist_subset.npz.dvc train.py ...           # code + pointer in ONE commit
python train.py --seed 42 --register --run-name q4-partnerA-seed42
```

`train.py` logs six parameters (including `seed`), per-epoch `train_loss` and `val_accuracy`,
final `accuracy` and `f1_macro`, a `git_commit` tag, a `team` tag, and the model artifact. It
then registers `mnist-mlp` and transitions version 1 to **Staging**.

| | |
|---|---|
| Commit | `91f6346042127b0648eb770f2c3c79c464097160` |
| MLflow run | `c806a73763e144b7834aad916e6ee5df`, experiment `q4-capstone` |
| accuracy / f1_macro | 0.9485 / 0.9481 |
| Registered model | `mnist-mlp` v1 → **Staging** |
| Dataset md5 | `b50dac761e0135c47104e195c592c9db` |

The same-commit requirement is evidenced in
[`Q4/evidence/q4_commit_contents.txt`](Q4/evidence/q4_commit_contents.txt) — `git show --stat`
of that commit lists `Q4/train.py` and `Q4/data/mnist_subset.npz.dvc` together.

### What Partner B did

Given only this repository and [`Q4/PARTNER_INSTRUCTIONS.md`](Q4/PARTNER_INSTRUCTIONS.md) —
no communication about the environment or the data — Sri Harsha cloned, ran `dvc checkout`,
built an environment from `requirements.txt`, and reran `train.py --seed 42`.

| Metric | Partner A | Partner B | Delta |
|---|---|---|---|
| accuracy | 0.9485 | 0.9520 | +0.0035 |
| f1_macro | 0.9481 | 0.9519 | +0.0038 |

Stated tolerance **±0.005 absolute accuracy** → **MATCH**. His report, authored and committed
by him, is [`Q4/PARTNER_VERIFICATION.md`](Q4/PARTNER_VERIFICATION.md); his commit appears in
[`Q4/evidence/authorship_log.txt`](Q4/evidence/authorship_log.txt).

He then wrote the verification note onto Partner A's run over the local network:

```bash
python log_partner_note.py --tracking-uri http://<partner-A>:5000 \
  --run-id c806a73763e144b7834aad916e6ee5df ...
```

adding the tags `partner_verification`, `verified_by` and `reproduced_accuracy`. Screenshots
of the run, the registry stage and those tags are in `Q4/evidence/`.

### Reproducing it yourself

```bash
git clone <this repo> && cd <repo>
dvc checkout
md5sum Q4/data/mnist_subset.npz        # b50dac761e0135c47104e195c592c9db
mamba env create -f environment.yml && mamba activate aiops-m1
cd Q4 && python train.py --seed 42
```

---

## 7. A note on MLflow evidence

MLflow's tracking state lives in a local SQLite database and is not committed (it is
machine-specific and would not be meaningful in a clone). The screenshots in `Q2/evidence/`
and `Q4/evidence/` are therefore the record of what the tracking server showed. Everything
they display is reproducible by following §4 and §6.

---

## 8. Video

*(2–5 minute demo — link here.)*

---

## 9. AI use

See [`AI_DISCLOSURE.md`](AI_DISCLOSURE.md), per the course Fair and Responsible Use of AI
policy.
