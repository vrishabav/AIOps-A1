# AI Disclosure

**Student:** Vrishab A V (DA24B033)

---

## 1. Which tools were used

| Tool | Role |
|---|---|
| **Claude (Anthropic)** | Primary assistant across all four questions: code scaffolding, debugging, and documentation drafting. |
| **Gemini (Google)** | Earlier drafts of the DVC SSH-remote setup, and a first version of the Q4 training script that was later replaced. |

---

## 2. How they were used

### Q2

AI was used to confirm the MLflow 3.x `log_model` signature and to resolve a `skops` `UntrustedTypesFoundException` raised when serialising the fitted model. 

### Q3

AI was used to verify my command sequence and explain the local SSH-remote setup (sshd, `authorized_keys`, `dvc remote modify … keyfile`), as well as to identify any issues beforehand. All commands were executed and recorded by me, as in `Q3/transcript.txt` and the submission video.

### Q4

AI was used to write `make_dataset.py`, `train.py` and `log_partner_note.py` for boilerplate to log the commands by my partner, and to discuss the repository layout. Claude was also used to find the exact places it had helped me with debugging, as mentioned below:

- `skops` serialisation error on `mlflow.sklearn.log_model`;
- the MLflow stages-vs-aliases deprecation in 3.x, and which API the registry actually accepted;
- a `.gitignore` rule (`data/` vs `/data/`) that was hiding `Q4/data/` from DVC;
- a dataset that was being normalised twice (saved as pre-divided float32 *and* divided again in `train.py`), which would have quietly produced near-chance accuracy;
- an MLflow server that had been started against the wrong SQLite backend.

### Documentation and review

AI was used to ensure the repository aligned with requirements from the assignment text, as well as to draft boiletplate for `environment.yml`, `requirements.txt`, `RUN_RECORD.md`, and to draft `README.md`, as well as to draft this disclosure (which has been completely rewritten by me from the original draft). That audit found two defects I had missed (subsequently fixed): `Q4/evidence/` was untracked, and a full `git checkout v1` in a fresh clone removes the committed DVC cache objects, so the rollback had to be demonstrated with the pointer-only form documented in `README.md`.
The LaTeX write-up templates were given by AI but all answers and analysis inside it were written by me manually.

## 3. Impact and Accountability

AI assistance shortened boilerplate writing and debugging cycles substantially, and the independent audit ensured that two reproducibility defects were caught. All cognitive wwork and engineering decisions, as well as learning, were done by me. Every number reported comes from a run done by me or my partner, and every terminal transcript is output I copied or screenshotted from my terminal.
