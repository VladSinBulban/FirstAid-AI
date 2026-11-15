# FirstAid AI — safety-focused prototype

## Run locally

1. Use Python 3.10 or newer.
2. Create and activate a virtual environment.
3. Install dependencies:

   ```powershell
   py -m pip install -r requirements.txt
   ```

4. Create a `.env` file using `.env.example` as a template.
5. Start the app:

   ```powershell
   py -m streamlit run app.py
   ```

## Run tests

```powershell
py -m unittest discover -s tests -v
```

## Architecture

- `backend/assessment.py`: conservative keyword screening for a limited set of explicit warning signs and injury locations.
- `backend/questions.py`: deterministic, area-specific follow-up questions that are not repeated.
- `backend/chat_safety.py`: static emergency response.
- `backend/ai.py`: Gemini primary provider and Groq fallback.
- `backend/first_aid.py`: conservative educational guidance catalogue.
- `backend/triage.py`: existing structured triage prototype.

## Important limitations

This is a hackathon prototype, not a medical device, diagnostic tool, or clinically validated triage system. Keyword matching is incomplete and can miss warning signs or misinterpret language. A negative result does not mean an injury is safe. Do not use it to decide whether someone needs care.

The application should be reviewed by qualified clinicians before any real-world use. For emergencies in Romania, call 112. Minors should involve a trusted adult in injury assessment and care.
