# FirstAid AI — prototype

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Install Streamlit:

   ```bash
   py -m pip install streamlit
   ```

4. Start the app:

   ```bash
   py -m streamlit run app.py
   ```

5. Your browser should open the local app.

## What this version does

- Collects a structured injury description.
- Checks a small set of emergency and prompt-assessment warning signs.
- Shows conservative, general first-aid guidance.
- Does not call an LLM, diagnose, store answers, or analyze images.

## Important limitations

This is a hackathon prototype, not a medical device or a substitute for professional care.
Its warning-sign checklist is incomplete and must be reviewed by qualified clinicians before
any real-world use. It should not be used to decide that an injury is safe or minor.
For an emergency in Romania, call 112.
