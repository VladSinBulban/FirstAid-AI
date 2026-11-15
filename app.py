import streamlit as st

from backend.ai import (
    generate_reply,
    AIConfigurationError,
    AIResponseError,
)
from backend.assessment import analyze_conversation, analyze_message
from backend.chat_safety import (
    EMERGENCY_MESSAGE,
    parse_emergency_confirmation,
)
from backend.questions import get_next_question
from backend.response_safety import validate_ai_response
from frontend.styles import apply_styles


st.set_page_config(
    page_title="FirstAid AI",
    page_icon="🩹",
    layout="centered",
)


# -------------------------------
# VISUAL THEME
# -------------------------------

apply_styles()


# -------------------------------
# SESSION STATE
# -------------------------------

DEFAULTS = {
    "messages": [],
    "conversation_started": False,
    "injury_area": "general",
    "asked_question_ids": [],
    "current_question_id": None,
    "emergency_confirmed": False,
    "awaiting_vision_clarification": False,
    "ai_retry_pending": False,
    "ai_response_pending": False,
    "assessment_notice_shown": False,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# -------------------------------
# STATIC SAFETY MESSAGES
# -------------------------------

PROMPT_ASSESSMENT_MESSAGE = (
    "**Please tell a trusted adult and arrange prompt medical assessment.** "
    "A chat assistant cannot determine how serious an injury is. "
    "Stop the activity and do not force movements that cause pain."
)

ASSESSMENT_STOP_MESSAGE = (
    "Thanks for answering. Please prioritize getting help from a trusted adult "
    "and a healthcare professional rather than continuing this chat."
)

VISION_CLARIFICATION = (
    "Do you mean **you can't see the injured area**, or that **your eyesight "
    "itself has suddenly changed**? Please reply `area` or `eyesight`."
)


def add_assistant_message(content: str):
    st.session_state.messages.append(
        {"role": "assistant", "content": content}
    )


def add_emergency_message():
    st.session_state.emergency_confirmed = True
    st.session_state.ai_retry_pending = False
    st.session_state.ai_response_pending = False
    add_assistant_message(EMERGENCY_MESSAGE)


def show_assessment_if_needed(urgent_flags):
    if urgent_flags and not st.session_state.assessment_notice_shown:
        add_assistant_message(PROMPT_ASSESSMENT_MESSAGE)
        st.session_state.assessment_notice_shown = True


def add_next_question():
    question = get_next_question(
        st.session_state.injury_area,
        set(st.session_state.asked_question_ids),
    )

    if question is None:
        st.session_state.current_question_id = None
        st.session_state.ai_response_pending = True
        return

    st.session_state.asked_question_ids.append(question["id"])
    st.session_state.current_question_id = question["id"]
    add_assistant_message(question["question"])


def apply_answer_to_previous_question(question_id, answer):
    """Interpret yes/no only in the context of the exact question asked."""
    if answer is None:
        return

    if question_id in {
        "leg_weakness",
        "loss_consciousness",
    } and answer is True:
        add_emergency_message()
        return

    urgent_yes = {
        "leg_numbness",
        "head_neck_impact",
        "knee_swelling",
        "foot_swelling",
        "arm_deformity",
        "arm_sensation",
        "shoulder_shape",
        "neurological_symptoms",
    }

    urgent_no = {
        "walking_ability",
        "weight_bearing",
        "arm_use",
    }

    if (question_id in urgent_yes and answer is True) or (
        question_id in urgent_no and answer is False
    ):
        show_assessment_if_needed(["concerning_follow_up_answer"])


# -------------------------------
# AI RESPONSE
# -------------------------------

def respond_with_ai():
    st.session_state.ai_response_pending = False

    with st.chat_message("assistant"):
        with st.spinner("Preparing a response..."):
            try:
                reply = generate_reply(st.session_state.messages)

                is_valid, validation_reason = validate_ai_response(reply)

                if not is_valid:
                    print(
                        "[FirstAid AI] Response rejected by safety check: "
                        f"{validation_reason}"
                    )
                    reply = (
                        "I can't safely provide a more specific response "
                        "based on the information collected. Please discuss "
                        "the injury with a trusted adult and seek medical "
                        "advice if symptoms are severe, worsening, or limit "
                        "normal movement."
                    )

                st.markdown(reply)

                st.session_state.messages.append(
                    {"role": "assistant", "content": reply}
                )
                st.session_state.ai_retry_pending = False

            except AIConfigurationError as error:
                st.error(f"AI configuration problem: {error}")
                st.session_state.ai_retry_pending = False

            except AIResponseError:
                st.error("The AI services are temporarily unavailable.")
                st.caption(
                    "Your conversation is saved. You can retry without "
                    "sending your message again."
                )
                st.session_state.ai_retry_pending = True


# -------------------------------
# HEADER
# -------------------------------

st.markdown(
    """
    <div class="fa-brand-row">
        <div class="fa-mark">+</div>
        <div>
            <div class="fa-brand-name">FirstAid AI</div>
            <div class="fa-brand-subtitle">Clear guidance. Safer next steps.</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if not st.session_state.conversation_started:
    st.markdown(
        '<div class="fa-eyebrow"><span class="fa-eyebrow-dot"></span> First-aid companion</div>',
        unsafe_allow_html=True,
    )
    st.title("What's bothering you?")
    st.markdown(
        '<div class="fa-intro">Tell me what happened. I’ll help you think through the next safe step, one question at a time.</div>',
        unsafe_allow_html=True,
    )
else:
    st.title("Your conversation")

st.markdown(
    '<div class="fa-safety-note"><span>✳</span><span><strong>Need emergency help?</strong> Call 112 in Romania. Don’t wait for a response from this app.</span></div>',
    unsafe_allow_html=True,
)


# -------------------------------
# DISPLAY CHAT HISTORY
# -------------------------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -------------------------------
# PROCESS PENDING AI RESPONSE
# -------------------------------

if st.session_state.ai_response_pending:
    respond_with_ai()


# -------------------------------
# RETRY
# -------------------------------

if st.session_state.ai_retry_pending and not st.session_state.emergency_confirmed:
    if st.button("Retry response", type="primary", use_container_width=True):
        st.session_state.ai_retry_pending = False
        st.session_state.ai_response_pending = True
        st.rerun()


# -------------------------------
# USER INPUT
# -------------------------------

if not st.session_state.emergency_confirmed:
    prompt = st.chat_input(
        "Describe what's happening..."
        if not st.session_state.conversation_started
        else "Reply here..."
    )

    if prompt:
        previous_question_id = st.session_state.current_question_id

        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        latest = analyze_message(prompt)
        conversation = analyze_conversation(st.session_state.messages)

        if not st.session_state.conversation_started:
            st.session_state.conversation_started = True
            st.session_state.injury_area = latest["injury_area"]
        elif (
            st.session_state.injury_area == "general"
            and latest["injury_area"] != "general"
        ):
            st.session_state.injury_area = latest["injury_area"]

        # Scan every new message and retain earlier warning signs.
        if conversation["emergency_flags"]:
            add_emergency_message()

        # "I can't see" is ambiguous. Clarify instead of interpreting it as yes/no.
        elif latest["ambiguous_vision"] and not st.session_state.awaiting_vision_clarification:
            st.session_state.awaiting_vision_clarification = True
            add_assistant_message(VISION_CLARIFICATION)

        elif st.session_state.awaiting_vision_clarification:
            lower = prompt.lower()

            if "eyesight" in lower or "vision" in lower:
                st.session_state.awaiting_vision_clarification = False
                add_emergency_message()
            elif "area" in lower or "injury" in lower or "body" in lower:
                st.session_state.awaiting_vision_clarification = False
                if st.session_state.assessment_notice_shown:
                    add_assistant_message(ASSESSMENT_STOP_MESSAGE)
                else:
                    add_next_question()
            else:
                add_assistant_message(
                    "Please choose one: `area` if you cannot see the injured "
                    "body part, or `eyesight` if your vision itself has changed."
                )

        else:
            st.session_state.current_question_id = None

            answer = parse_emergency_confirmation(prompt)
            apply_answer_to_previous_question(previous_question_id, answer)

            if not st.session_state.emergency_confirmed:
                show_assessment_if_needed(conversation["urgent_flags"])

                # Once a concerning injury has been identified, ask at most
                # one focused safety question and then stop the chat flow.
                if (
                    st.session_state.assessment_notice_shown
                    and previous_question_id is not None
                ):
                    add_assistant_message(ASSESSMENT_STOP_MESSAGE)
                else:
                    add_next_question()

        st.rerun()


# -------------------------------
# FOOTER
# -------------------------------

st.markdown("---")
st.caption(
    "Prototype only. This tool does not diagnose injuries or rule out serious "
    "conditions. It is not a substitute for professional medical care."
)
