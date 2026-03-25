# notebooks/run_scoring_demo.py
"""
Small demo runner to execute the scoring script and print a concise audit summary.
Intended to be run from the repository root.

Usage (from repo root):
    python notebooks/run_scoring_demo.py
"""

import subprocess
import sys
from pathlib import Path
import pandas as pd

# Paths (adjust if your filenames differ)
INPUT_XLSX = "data/AutoEIT Sample Transcriptions for Scoring.xlsx"
OUTPUT_XLSX = "outputs/scored_output.xlsx"
AUDIT_CSV = "data/scoring_audit_changes_rebuilt.csv"
SCORER = "run_scoring.py"

def run_scoring():
    cmd = [sys.executable, SCORER, "--input", INPUT_XLSX, "--output", OUTPUT_XLSX, "--audit", AUDIT_CSV]
    print("Running scorer:")
    print(" ".join(cmd))
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("=== Scorer stdout ===")
    print(res.stdout)
    if res.returncode != 0:
        print("=== Scorer stderr ===")
        print(res.stderr)
        raise SystemExit(f"Scorer failed with exit code {res.returncode}")

def print_audit_summary():
    p = Path(AUDIT_CSV)
    if not p.exists():
        print(f"Audit file not found: {p}")
        return
    df = pd.read_csv(p)
    print(f"\nTOTAL_AUDIT_ROWS: {len(df)}")
    if "sheet_name" in df.columns:
        print("\nTop 5 sheets with most changes:")
        print(df["sheet_name"].value_counts().head(5).to_string())
    else:
        print("No sheet_name column in audit CSV.")
    print("\nRepresentative audit rows (up to 5):")
    cols = []
    for c in ("sheet_name", "Score_before", "Score_manual", "Score_auto", "Stimulus_clean", "Transcription_clean"):
        if c in df.columns:
            cols.append(c)
    if not cols:
        # fallback: show first 5 columns
        cols = list(df.columns[:5])
    print(df[cols].head(5).to_string(index=False))

def main():
    try:
        run_scoring()
    except Exception as e:
        print("Scoring run failed:", e)
        return
    try:
        print_audit_summary()
    except Exception as e:
        print("Failed to read/print audit summary:", e)

if __name__ == "__main__":
    main()
