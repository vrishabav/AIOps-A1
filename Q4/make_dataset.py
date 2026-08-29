"""
Q4 — Build the DVC-tracked dataset.

Downloads MNIST once, takes a deterministic 10,000-sample stratified subset,
and saves it as a compressed .npz (~2 MB) so it can be versioned with DVC and
travel with the repository.

Run ONCE, then `dvc add` the output. Your partner never runs this.
"""
import argparse
import numpy as np
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="data/mnist_subset.npz")
    p.add_argument("--n", type=int, default=10000)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    print("Fetching MNIST from OpenML (this takes a minute)...")
    X, y = fetch_openml("mnist_784", version=1, return_X_y=True,
                        as_frame=False, parser="auto")

    # uint8 keeps the file small; train.py rescales to [0, 1]
    X = X.astype(np.uint8)
    y = y.astype(np.int64)

    X_sub, _, y_sub, _ = train_test_split(
        X, y, train_size=args.n, stratify=y, random_state=args.seed
    )

    np.savez_compressed(args.out, X=X_sub, y=y_sub)
    print(f"Wrote {args.out}: X={X_sub.shape} {X_sub.dtype}, y={y_sub.shape}")


if __name__ == "__main__":
    main()
