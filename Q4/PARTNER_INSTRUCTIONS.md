# Q4 — Reproduction Instructions for Partner B

You are reproducing Partner A's training run. **Per the assignment, no
communication about the environment or the data is allowed** — everything you
need is in this repository. If something here is insufficient, that is a finding
worth recording, not a reason to message me.

Partner A: **Vrishab A V (DA24B033)**

---

## 0. Prerequisites

- `git`
- `mamba` or `conda`
- A Linux / WSL / macOS shell

Clone into a **native Linux path** (e.g. `~/`), not a mounted Windows drive —
DVC's cache relies on hardlinks that NTFS does not support.

---

## 1. Clone and check out the exact commit

```bash
git clone <REPO_URL> aiops-partner-check
cd aiops-partner-check
git checkout <Q4_COMMIT_SHA>
git log -1 --oneline
```

`<Q4_COMMIT_SHA>` is given at the top of `Q4/RUN_RECORD.md`. This is the commit
that contains both the training code and the `.dvc` pointer for the dataset.

---

## 2. Restore the dataset

```bash
dvc checkout
ls -lh Q4/data/mnist_subset.npz
md5sum Q4/data/mnist_subset.npz
```

The DVC cache objects are committed to this repository, so `dvc checkout`
restores the data with no network access and no credentials. Compare the md5
against the value recorded in `Q4/RUN_RECORD.md`.

If `dvc checkout` reports missing cache files, run `dvc pull` and tell me it
failed — that is a reproducibility defect and should go in your note.

---

## 3. Build the environment

```bash
mamba env create -f environment.yml
mamba activate aiops-m1
python -c "import sklearn, mlflow; print(sklearn.__version__, mlflow.__version__)"
```

The printed versions must match those recorded in `Q4/RUN_RECORD.md`. A
different scikit-learn minor version can shift the metric slightly; note it if
so.

---

## 4. Rerun the training script

Log to **your own** local MLflow — do not point at my server for this step.

```bash
cd Q4
mlflow server --backend-store-uri sqlite:///mlflow.db \
              --default-artifact-root ./mlruns \
              --host 127.0.0.1 --port 5000 &

python train.py --seed 42
```

It prints `run_id`, `accuracy`, and `f1_macro`. Expected wall time: ~2 minutes.

Compare your `accuracy` against the value in `Q4/RUN_RECORD.md`.
**Stated tolerance: ±0.005 absolute accuracy.**

Take a screenshot of your run in the MLflow UI.

---

## 5. Log your verification note on my run

This is the only step that touches my machine. I will send you a tracking URI
when my server is up (a Tailscale address, or a LAN address if we are on the
same hotspot).

```bash
python log_partner_note.py \
  --tracking-uri http://<ADDRESS>:5000 \
  --run-id <MY_RUN_ID_from_RUN_RECORD.md> \
  --their-accuracy <accuracy from RUN_RECORD.md> \
  --my-accuracy <your reproduced accuracy> \
  --verifier "Your Name (YOUR_ROLLNO)" \
  --notes "any discrepancy or environment difference"
```

Confirm the tag appears on my run in the MLflow UI, and screenshot it.

**If you cannot reach my server:** run the same command against your own
tracking URI so the note is logged somewhere, screenshot it, and send me the
exact verdict string. I will apply it to my run and document the fallback. Do
not spend more than ten minutes on network debugging.

---

## 6. What to send back

1. Your reproduced `accuracy` and `f1_macro`
2. Your `run_id`
3. Screenshot of your MLflow run
4. Screenshot of the note on my run (or the verdict string, if you used the fallback)
5. Any step above that did not work as written

Thanks — and send me the same for your repo so I can reciprocate.
