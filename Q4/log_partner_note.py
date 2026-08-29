"""
Q4 step 4 — Partner B runs this to log the verification note onto
Partner A's original MLflow run.

Example
-------
python log_partner_note.py \
    --tracking-uri http://100.x.y.z:5000 \
    --run-id <A's run_id> \
    --my-accuracy 0.9485 \
    --their-accuracy 0.9485 \
    --verifier "Partner Name (ROLLNO)"
"""
import argparse
from mlflow import MlflowClient

TOLERANCE = 0.005  # absolute accuracy; state this in the write-up


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--tracking-uri", required=True)
    p.add_argument("--run-id", required=True, help="Partner A's original run_id")
    p.add_argument("--my-accuracy", type=float, required=True)
    p.add_argument("--their-accuracy", type=float, required=True)
    p.add_argument("--verifier", required=True)
    p.add_argument("--notes", default="")
    args = p.parse_args()

    delta = args.my_accuracy - args.their_accuracy
    matched = abs(delta) <= TOLERANCE

    verdict = (
        f"REPRODUCED by {args.verifier}. "
        f"Original accuracy={args.their_accuracy:.4f}, "
        f"reproduced accuracy={args.my_accuracy:.4f}, "
        f"delta={delta:+.4f}, tolerance=+/-{TOLERANCE}. "
        f"Result: {'MATCH' if matched else 'MISMATCH'}."
    )
    if args.notes:
        verdict += f" Notes: {args.notes}"

    client = MlflowClient(tracking_uri=args.tracking_uri)
    client.set_tag(args.run_id, "partner_verification", verdict)
    client.set_tag(args.run_id, "verified_by", args.verifier)
    client.set_tag(args.run_id, "reproduced_accuracy", f"{args.my_accuracy:.4f}")

    print(verdict)
    print(f"\nTags written to run {args.run_id}")


if __name__ == "__main__":
    main()
