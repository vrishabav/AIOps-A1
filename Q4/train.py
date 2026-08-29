"""
Q4 — Capstone training script (Partner A authors, Partner B reruns).

Logs to MLflow: parameters incl. seed, per-epoch metrics, final metrics,
a git_commit tag, and the model artifact. Optionally registers the model
and promotes it to Staging.

Run from inside the Q4/ directory, with an MLflow tracking server running.

Usage
-----
Partner A (registers the model):
    python train.py --seed 42 --register --run-name q4-partnerA-seed42

Partner B (reproduction, logs to their OWN local MLflow):
    python train.py --seed 42
"""
import argparse
import subprocess

import numpy as np
import mlflow
import mlflow.sklearn
from mlflow import MlflowClient
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, f1_score

# MLflow 3.x serialises sklearn models with skops, which refuses to load
# optimizer objects unless they are explicitly declared trusted.
SKOPS_TRUSTED = ["sklearn.neural_network._stochastic_optimizers.AdamOptimizer"]


def git_commit_hash():
    """Exact commit that produced this run — the traceability link from Q1/Q3."""
    try:
        h = subprocess.check_output(["git", "rev-parse", "HEAD"],
                                    stderr=subprocess.DEVNULL).decode().strip()
        dirty = subprocess.call(["git", "diff", "--quiet"],
                                stderr=subprocess.DEVNULL) != 0
        return h + ("-dirty" if dirty else "")
    except Exception:
        return "unknown"


def promote(client, name, version):
    """
    MLflow 3.x removed stages in favour of aliases. Try the classic stages API
    first (works on MLflow 2.x), then fall back to an alias.
    Both mechanisms are covered in Lecture 3, section 4.3.
    """
    try:
        client.transition_model_version_stage(
            name=name, version=version, stage="Staging",
            archive_existing_versions=True,
        )
        return "stage=Staging (classic stages API)"
    except Exception:
        client.set_registered_model_alias(name=name, alias="staging",
                                          version=version)
        return "alias=@staging (MLflow 3.x aliases API; stages removed)"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data", default="data/mnist_subset.npz")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--lr", type=float, default=0.003)
    p.add_argument("--batch-size", type=int, default=32)
    p.add_argument("--hidden", type=int, default=128)
    p.add_argument("--max-iter", type=int, default=30)
    p.add_argument("--tracking-uri", default="http://localhost:5000")
    p.add_argument("--experiment", default="q4-capstone")
    p.add_argument("--run-name", default=None)
    p.add_argument("--register", action="store_true",
                   help="Register the model and promote to Staging (Partner A only)")
    p.add_argument("--model-name", default="mnist-mlp")
    args = p.parse_args()

    mlflow.set_tracking_uri(args.tracking_uri)
    mlflow.set_experiment(args.experiment)

    d = np.load(args.data)
    X = d["X"].astype("float32") / 255.0
    y = d["y"].astype("int64")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=args.seed)

    with mlflow.start_run(run_name=args.run_name) as run:
        # ---- parameters (seed is required by Q4) ----
        mlflow.log_params({
            "seed": args.seed,
            "learning_rate_init": args.lr,
            "batch_size": args.batch_size,
            "hidden_layer_sizes": (args.hidden,),
            "max_iter": args.max_iter,
            "data_path": args.data,
        })

        # ---- lineage tags (git_commit is required by Q4) ----
        mlflow.set_tag("git_commit", git_commit_hash())
        mlflow.set_tag("team", "data-science")

        model = MLPClassifier(
            hidden_layer_sizes=(args.hidden,),
            learning_rate_init=args.lr,
            batch_size=args.batch_size,
            max_iter=args.max_iter,
            early_stopping=True,
            validation_fraction=0.1,
            n_iter_no_change=args.max_iter,
            random_state=args.seed,
        )
        model.fit(X_train, y_train)

        # ---- per-epoch metrics (time series in the UI) ----
        for step, (loss, val) in enumerate(
                zip(model.loss_curve_, model.validation_scores_)):
            mlflow.log_metric("train_loss", loss, step=step)
            mlflow.log_metric("val_accuracy", val, step=step)

        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        f1 = f1_score(y_test, preds, average="macro")
        mlflow.log_metrics({"accuracy": acc, "f1_macro": f1})

        # ---- model artifact (always logged, per Q4) ----
        mlflow.sklearn.log_model(
            model,
            name="model",
            skops_trusted_types=SKOPS_TRUSTED,
            registered_model_name=args.model_name if args.register else None,
        )

        run_id = run.info.run_id
        print("\n--- RUN COMPLETE ---")
        print(f"run_id     = {run_id}")
        print(f"accuracy   = {acc:.4f}")
        print(f"f1_macro   = {f1:.4f}")
        print(f"git_commit = {git_commit_hash()}")

    if args.register:
        client = MlflowClient()
        versions = client.search_model_versions(f"name='{args.model_name}'")
        v = max(int(x.version) for x in versions)
        how = promote(client, args.model_name, v)
        print(f"Registered {args.model_name} v{v} -> {how}")


if __name__ == "__main__":
    main()
