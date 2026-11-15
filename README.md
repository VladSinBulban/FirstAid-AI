# 🩹 FirstAid AI

**Clear guidance. Safer next steps.**

FirstAid AI is a conversational first-aid information prototype designed to help users understand potential injuries, recognize warning signs, and identify appropriate next steps.

> **Disclaimer:** FirstAid AI is an experimental prototype, not a medical device or clinically validated diagnostic tool. It does not replace professional medical advice or emergency services.

## 🚀 Try the application

**[Launch FirstAid AI](https://firstaidaifr.streamlit.app/)**

## ✨ Features

- Conversational first-aid information.
- Context-aware follow-up questions.
- Injury-area identification.
- Deterministic emergency screening.
- Predefined emergency messaging.
- AI-generated educational responses.
- Response safety validation.
- Gemini primary AI provider with Groq fallback.
- Dark, responsive Streamlit interface.

## 🛠️ Technology

- Python
- Streamlit
- Google Gemini API
- Groq API
- Google Gen AI SDK
- python-dotenv

## 🧠 How it works

FirstAid AI combines deterministic safety logic with generative AI.

1. The user describes an injury or situation.
2. The application screens for supported warning signs.
3. It identifies the reported injury area.
4. It asks relevant follow-up questions.
5. The AI generates an educational response.
6. The response is checked against application safety constraints.

## 🧪 Testing

The repository includes automated unit tests covering:

- Assessment and injury identification
- Contextual question selection
- Emergency handling
- First-aid guidance
- Triage logic
- AI response safety

## ⚠️ Limitations

This project is a hackathon prototype. Its screening logic is limited and can miss warning signs or misunderstand descriptions. It cannot diagnose injuries, rule out emergencies, or guarantee that its guidance is appropriate.

For emergencies, contact local emergency services. In Romania, call **112**.

## 📂 Project structure

```text
FirstAid-AI/
├── app.py
├── backend/
├── frontend/
├── data/
├── tests/
├── .streamlit/
├── requirements.txt
└── README.md
```

## 🔐 Local setup

1. Clone the repository:

```bash
git clone https://github.com/VladSinBulban/FirstAid-AI.git
cd FirstAid-AI
```

2. Create and activate a virtual environment.

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure your API keys in a local `.env` file:

```env
GEMINI_API_KEY=your_gemini_key
GROQ_API_KEY=your_groq_key
```

5. Start the application:

```bash
streamlit run app.py
```

Never commit your `.env` file or expose API keys.

## 🙌 Credits

- Google Gemini API — primary AI provider.
- Groq API — fallback AI provider.
- OpenAI ChatGPT — development assistance and debugging.
- Streamlit and the other listed Python libraries — application infrastructure.

No external patient dataset is claimed for this prototype.

---

**Repository:** [GitHub](https://github.com/VladSinBulban/FirstAid-AI)  
**Live application:** [FirstAid AI](https://firstaidaifr.streamlit.app/)