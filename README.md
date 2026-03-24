# AutoEIT GSoC 2026 Submission

Author: Joy Abioye  
Email: joyabioye884@gmail.com

## What is included
- src/: scoring pipeline (rubric, scorer, utils, CLI)
- notebooks/scoring_demo.ipynb : executed notebook demonstrating the pipeline
- notebooks/scoring_demo.pdf : PDF export of the notebook with outputs
- data/AutoEIT_Sample_Transcriptions_for_Scoring_scored_complete.xlsx : input dataset
- data/borderline_audit.csv : flagged borderline rows for human review
- outputs/scored_output.xlsx : automated scores (sentence-level)
- outputs/scored_summary.csv : summary statistics
- requirements.txt : pinned dependencies
- C

## How to reproduce
1. Clone the repo and switch to branch `feat/autoeit-gsoc-2026-scoring`.
2. Create a virtual environment and install:
pip install -r requirements.txt
3. Run scoring (example):
bash run.sh data/AutoEIT_Sample_Transcriptions_for_Scoring_scored_complete.xlsx outputs/scored_output.xlsx outputs/scored_summary.csv
4. Open `notebooks/scoring_demo.ipynb` to view the demonstration.

Contact: joyabioye884@gmail.com
