
import os
from functools import lru_cache

from dotenv import load_dotenv
from google import genai
from google.genai import types
from groq import Groq


load_dotenv()

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL", "gemini-3.8-flash"
).strip()

GROQ_MODEL = os.getenv(
    "GROQ_MODEL", "openai/gpt-oss-120b"
).strip()

REQUEST_TIMEOUT = 30.0


SYSTEM_INSTRUCTION = """
You are FirstAid AI, a cautious first-aid information assistant.

IMPORTANT APPLICATION DESIGN:
- The application performs its own deterministic safety screening and asks
  its own focused follow-up questions.
- Do NOT repeat a generic emergency yes/no checklist.
- Do NOT ask another follow-up question in your final response.
- Do NOT override or contradict the application's safety messages.
- The application is a prototype, not a diagnostic or clinically validated
  triage system.

YOUR ROLE:
- Briefly summarize what the user described without diagnosing.
- Explain uncertainty clearly.
- Use calm, simple language.
- Encourage a trusted adult to help the user obtain professional assessment
  when symptoms are severe, worsening, or interfere with normal use.
- Never claim to be a doctor or healthcare professional.

SAFETY:
- Never diagnose a fracture, sprain, dislocation, concussion, or other condition.
- Never say an injury is definitely harmless or that serious injury is ruled out.
- Never recommend medication or medication doses.
- Never recommend compression, elevation, or other treatment unless the
  application has supplied specific, approved guidance for that injury.
- Never recommend straightening a limb or putting a joint back into place.
- Never recommend homemade casts or risky procedures.
- Never invent medical instructions.
- Never encourage a minor to hide an injury from adults.
- If the user describes an emergency, direct them to call 112 in Romania
  or their local emergency number and get a trusted adult immediately.

STYLE:
- Keep the response under 100 words.
- Do not use long lists.
- Do not add a new question.
- Do not imply that this chat can rule out serious injury.
"""


class AIConfigurationError(Exception):
    pass


class AIResponseError(Exception):
    pass


@lru_cache(maxsize=1)
def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return None

    return genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            timeout=int(REQUEST_TIMEOUT * 1000)
        ),
    )


@lru_cache(maxsize=1)
def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return None

    return Groq(
        api_key=api_key,
        timeout=REQUEST_TIMEOUT,
        max_retries=1,
    )


def prepare_gemini_contents(messages):
    contents = []

    for message in messages:
        role = (
            "model"
            if message["role"] == "assistant"
            else "user"
        )

        contents.append(
            types.Content(
                role=role,
                parts=[
                    types.Part.from_text(
                        text=message["content"]
                    )
                ],
            )
        )

    return contents


def generate_with_gemini(messages):
    client = get_gemini_client()

    if client is None:
        raise AIConfigurationError(
            "Gemini API key is not configured."
        )

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prepare_gemini_contents(messages),
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.2,
            max_output_tokens=350,
        ),
    )

    reply = response.text

    if not reply or not reply.strip():
        raise AIResponseError(
            "Gemini returned an empty response."
        )

    return reply.strip()


def generate_with_groq(messages):
    client = get_groq_client()

    if client is None:
        raise AIConfigurationError(
            "Groq API key is not configured."
        )

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_INSTRUCTION,
            },
            *[
                {
                    "role": message["role"],
                    "content": message["content"],
                }
                for message in messages
            ],
        ],
        temperature=0.2,
        max_tokens=350,
    )

    reply = response.choices[0].message.content

    if not reply or not reply.strip():
        raise AIResponseError(
            "Groq returned an empty response."
        )

    return reply.strip()


def generate_reply(messages):
    if not messages:
        raise ValueError(
            "Conversation history cannot be empty."
        )

    errors = []

    # Try Gemini first.
    if os.getenv("GEMINI_API_KEY"):
        try:
            reply = generate_with_gemini(messages)

            print("[FirstAid AI] Response generated using Gemini.")

            return reply

        except Exception as error:
            print(
                "[FirstAid AI] Gemini failed: "
                f"{type(error).__name__}: {error}"
            )

            errors.append("Gemini")

    # Try Groq if Gemini fails.
    if os.getenv("GROQ_API_KEY"):
        try:
            reply = generate_with_groq(messages)

            print("[FirstAid AI] Response generated using Groq.")

            return reply

        except Exception as error:
            print(
                "[FirstAid AI] Groq failed: "
                f"{type(error).__name__}: {error}"
            )

            errors.append("Groq")

    if not os.getenv("GEMINI_API_KEY") and not os.getenv("GROQ_API_KEY"):
        raise AIConfigurationError(
            "No AI API keys configured. Check your .env file."
        )

    raise AIResponseError(
        "All configured AI providers failed. "
        "Please try again later."
    )
