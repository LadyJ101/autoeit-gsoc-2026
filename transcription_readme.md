# Transcription Readme

**Purpose**
This document records how audio → text transcriptions were produced for the AutoEIT submission, what corrections were made (and which were not), and known issues to help reviewers reproduce and audit the transcripts.

## ASR system used
- **Model / Service:** Whisper (open-source) or specify cloud ASR if used.
- **Model size / version:** e.g., `whisper-medium` (replace with actual model used).
- **Language setting:** Spanish (`es`) where supported.
- **Decoding settings:** beam size / temperature / task (if applicable). Example: `beam_size=5`, `temperature=0.0`.

## Transcription policy (what we keep vs what we correct)
- **Verbatim requirement:** Transcripts reflect the learner's exact production, including disfluencies (filled pauses, false starts, repetitions).
- **Allowed ASR corrections:** Only clear ASR misrecognitions that are unambiguously wrong. Corrections are minimal and documented in `Transcription_corrected`.
- **Not corrected:** Participant grammar, vocabulary errors, morphological errors, dialectal variants, or intended hesitations.
- **Filler handling:** Fillers such as `um`, `uh`, `mm` are preserved in `Transcription_raw`. A cleaned version with optional filler removal is available in `Transcription_clean`.

## File columns and meaning
- **Stimulus:** target sentence prompt.
- **Audio_filename:** original audio file name (if present).
- **Transcription_raw:** raw ASR output (verbatim).
- **Transcription_corrected:** minimal manual corrections for ASR errors only.
- **Transcription_clean:** normalized text used for scoring.
- **Notes:** short note on issues (low volume, overlap, heavy noise, dialectal pronunciation).

## Known issues and limitations
- **Background noise / overlap:** some files have low SNR; these are flagged in Notes.
- **Dialectal Spanish:** regional pronunciations may reduce ASR accuracy; flagged examples are included in the audit CSV.
- **Short utterances:** very short responses sometimes produce unstable ASR output; these are highlighted in the audit.

## Reproducibility
To reproduce transcripts:
1. Install the ASR environment (see `requirements.txt`).
2. Run the ASR command used (example): `whisper --model medium --language es --task transcribe <audiofile>`.
3. Postprocess with the cleaning script in `src/utils` or the cleaning function in `src/scoring_engine.py`.

## Contact
If anything is unclear about transcription choices, contact: **joyabioye884@gmail.com**
