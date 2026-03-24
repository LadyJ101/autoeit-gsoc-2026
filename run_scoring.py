#!/usr/bin/env python3
"""
run_scoring.py

Simple, transparent scoring script for AutoEIT Test II.
Reads an input Excel workbook (one sheet per participant), cleans text,
computes token and character similarity, assigns Score_manual, and writes:
 - scored workbook (Excel)
 - audit CSV with rows that changed in this run

Usage:
  python run_scoring.py --input "data/AutoEIT Sample Transcriptions for Scoring.xlsx" \
                       --output "data/AutoEIT Sample Transcriptions for Scoring_scored_complete.xlsx" \
                       --audit "data/scoring_audit_changes_rebuilt.csv"
"""

import argparse
import pandas as pd
import re
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

def clean_text(s):
    if pd.isna(s):
        return ""
    if not isinstance(s, str):
        s = str(s)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.lower()
    s = re.sub(r"[^0-9a-z\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def token_similarity(a, b):
    ta = [t for t in a.split() if t]
    tb = [t for t in b.split() if t]
    if not ta and not tb:
        return 1.0
    if not ta or not tb:
        return 0.0
    set_a = set(ta)
    set_b = set(tb)
    inter = set_a.intersection(set_b)
    return (2.0 * len(inter)) / (len(set_a) + len(set_b))

def char_similarity(a, b):
    if not a and not b:
        return 1.0
    return SequenceMatcher(None, a, b).ratio()

THRESHOLDS = {
    "exact_match": 1.0,
    "high_token": 0.90,
    "high_char": 0.90,
    "mid_token": 0.60,
}

def assign_score(stim_clean, trans_clean):
    if stim_clean == trans_clean and stim_clean != "":
        return 4
    t_sim = token_similarity(stim_clean, trans_clean)
    c_sim = char_similarity(stim_clean, trans_clean)
    if t_sim >= THRESHOLDS["high_token"] and c_sim >= THRESHOLDS["high_char"]:
        return 3
    if t_sim >= THRESHOLDS["mid_token"]:
        return 2
    if trans_clean.strip() != "":
        return 1
    return 0

def process_workbook(input_path, output_path, audit_path,
                     stimulus_col_candidates=None, transcription_col_candidates=None):
    input_path = Path(input_path)
    output_path = Path(output_path)
    audit_path = Path(audit_path)

    sheets = pd.read_excel(input_path, sheet_name=None)
    changed_rows = []

    out_sheets = {}
    for sheet_name, df in sheets.items():
        df = df.copy()
        stim_col = None
        trans_col = None

        # Try exact matches
        for cand in (stimulus_col_candidates or ["stimulus", "stimulus_clean", "prompt", "target"]):
            for c in df.columns:
                if c.lower() == cand.lower():
                    stim_col = c
                    break
            if stim_col:
                break

        for cand in (transcription_col_candidates or ["transcription", "transcription_clean", "response", "utterance"]):
            for c in df.columns:
                if c.lower() == cand.lower():
                    trans_col = c
                    break
            if trans_col:
                break

        # Fallback substring detection
        if stim_col is None:
            for c in df.columns:
                if "stim" in c.lower() or "prompt" in c.lower() or "target" in c.lower():
                    stim_col = c
                    break

        if trans_col is None:
            for c in df.columns:
                if "trans" in c.lower() or "response" in c.lower() or "utter" in c.lower():
                    trans_col = c
                    break

        if stim_col is None or trans_col is None:
            raise ValueError(
                f"Could not detect stimulus/transcription columns in sheet '{sheet_name}'. "
                f"Columns found: {list(df.columns)}"
            )

        df["Stimulus_clean"] = df[stim_col].apply(clean_text)
        df["Transcription_clean"] = df[trans_col].apply(clean_text)

        prev_score_col = None
        for c in df.columns:
            if c.lower() in ("score_manual", "score_before", "score"):
                prev_score_col = c
                break

        df["Score_before"] = df[prev_score_col] if prev_score_col else pd.NA
        df["Score_manual"] = df.apply(
            lambda r: assign_score(r["Stimulus_clean"], r["Transcription_clean"]), axis=1
        )

        mask_changed = (df["Score_before"].isna()) | (df["Score_before"] != df["Score_manual"])
        changed = df.loc[mask_changed].copy()
        if not changed.empty:
            changed["sheet_name"] = sheet_name
            changed_rows.append(changed)

        out_sheets[sheet_name] = df

    # Write scored workbook
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for name, out_df in out_sheets.items():
            out_df.to_excel(writer, sheet_name=name, index=False)

    # Write audit CSV
    if changed_rows:
        audit_df = pd.concat(changed_rows, ignore_index=True)
        cols = ["sheet_name", "Score_before", "Score_manual", "Stimulus_clean", "Transcription_clean"]
        other_cols = [c for c in audit_df.columns if c not in cols]
        audit_df = audit_df[[c for c in cols if c in audit_df.columns] + other_cols]
        audit_df.to_csv(audit_path, index=False)
    else:
        pd.DataFrame(columns=[
            "sheet_name", "Score_before", "Score_manual",
            "Stimulus_clean", "Transcription_clean"
        ]).to_csv(audit_path, index=False)

    total_changed = sum(len(df) for df in changed_rows) if changed_rows else 0
    print("Input workbook:", input_path)
    print("Scored workbook written to:", output_path)
    print("Audit CSV written to:", audit_path, f"(rows changed: {total_changed})")

def main():
    parser = argparse.ArgumentParser(description="Run scoring pass on AutoEIT workbook.")
    parser.add_argument("--input", required=True, help="Input Excel workbook (one sheet per participant).")
    parser.add_argument("--output", required=True, help="Output scored workbook path.")
    parser.add_argument("--audit", required=True, help="Output audit CSV path (changed rows).")
    args = parser.parse_args()

    process_workbook(args.input, args.output, args.audit)

if __name__ == "__main__":
    main()
