# README Tests and Quick Validation

**Purpose**
Short, exact steps to validate the scoring pipeline and inspect the audit. Use these when running locally, in Codespace, or in Colab.

## Quick prerequisites
- Python 3.10+ recommended
- Install pinned dependencies: `pip install -r requirements.txt`
- Input workbook path: `data/AutoEIT Sample Transcriptions for Scoring.xlsx`
- Runner script: `run_scoring.py` at repo root

## Run scoring one command
From the repository root run:
python run_scoring.py --input "data/AutoEIT Sample Transcriptions for Scoring.xlsx" --output "outputs/scored_output.xlsx" --audit "data/scoring_audit_changes_rebuilt.csv"


## Expected outputs
- `outputs/scored_output.xlsx` — workbook with same sheets plus added columns:
  - `Stimulus_clean`, `Transcription_clean`, `Score_before` (if present), `Score_manual` or `Score_auto`
- `data/scoring_audit_changes_rebuilt.csv` — CSV with rows where automated score differs from previous/human score or where no previous score existed

## Quick checks after run
1. Preview first 20 lines of audit:
head -n 20 data/scoring_audit_changes_rebuilt.csv
2. Summary snippet to run in Python or a notebook:
```python
import pandas as pd, pathlib
p = pathlib.Path("data/scoring_audit_changes_rebuilt.csv")
if not p.exists():
    print("AUDIT_NOT_FOUND")
else:
    df = pd.read_csv(p)
    print("TOTAL_AUDIT_ROWS:", len(df))
    if 'sheet_name' in df.columns:
        print(df['sheet_name'].value_counts().head(3))
    print(df.head(3).to_string(index=False))
## If many audit rows appear
- Inspect the first 20 audit rows to identify the common failure mode.
- Make a single targeted change (one threshold or add one filler token) and re-run.
- Record the change in this file under a Tuning log section.

## Tuning log example
- 2026-03-25: lowered `high_token` from 0.90 to 0.85 to reduce false negatives.

## Contact
If you need help reproducing these steps, contact: **joyabioye884@gmail.com**

---

### Step‑by‑step GitHub web UI instructions (novice‑proof)
1. **Open the repo page** in your browser and sign in to GitHub.  
2. **Switch branch**: click the branch selector, choose `feat/autoeit-gsoc-2026-scoring`.  
3. **Add file**: click **Add file** → **Create new file**.  
4. **Name file**: in **Name your file…** type exactly `README_tests.md`.  
5. **Paste content**: click the editor area and paste the entire content from the **Exact file content** block above.  
6. **Commit**:
   - Scroll down to **Commit new file**.
   - In **Commit message** enter: `docs: add README_tests.md with validation steps`.
   - Ensure **Commit directly to the feat/autoeit-gsoc-2026-scoring branch** is selected.
   - Click **Commit new file**.
7. **Verify**:
   - After commit you’ll see the file view. Confirm the filename at the top is `README_tests.md`.
   - Click the repo name to return to root and confirm the file appears in the file list.

---

### How to confirm it worked (two checks)
- **Visual check:** open `README_tests.md` in the web UI and scan the content.  
- **History check:** click **History** on the file page to confirm the commit message.

---

### Next single baby step for you (do this now)
**Create `README_tests.md` on GitHub using the steps above.**  
When done, reply **done** and I will give the next single action: either (A) prepare a one‑cell notebook snippet to add to `notebooks/scoring_demo.ipynb` that runs the scorer and prints the audit summary, or (B) prepare one precise tuning edit (one YAML change) likely to reduce the most common audit errors. Choose **A** or **B** after you say **done**.
