import streamlit as st

st.set_page_config(
    page_title="FirstAid AI — prototype",
    page_icon="🩹",
    layout="centered",
)

st.title("🩹 FirstAid AI")
st.caption("A first-aid guidance prototype — not a diagnosis or a replacement for a healthcare professional.")

st.warning(
    "If someone is unconscious, having trouble breathing, has severe bleeding, "
    "or may have a life-threatening injury, call 112 in Romania (or your local emergency number) now. "
    "Get a trusted adult immediately. Do not wait for this app."
)

st.markdown(
    """
This prototype uses a **fixed safety checklist**, not an AI diagnosis. It is deliberately cautious:
when an answer suggests a potentially serious injury, it recommends getting medical help.
"""
)

st.header("1. Tell us what happened")
injury_area = st.selectbox(
    "Where is the injury?",
    ["Ankle / foot", "Leg / knee", "Arm / wrist / hand", "Shoulder", "Head / neck / back", "Other"],
)
mechanism = st.selectbox(
    "How did it happen?",
    [
        "Twist or awkward landing",
        "Fall or direct impact",
        "Collision during sport",
        "Cut or puncture",
        "I am not sure",
        "Something else",
    ],
)
when = st.radio(
    "When did it happen?",
    ["Just now", "Within the last 24 hours", "More than 24 hours ago"],
)

st.header("2. What are you experiencing?")
st.caption("Choose every option that applies. If you are unsure, choose the safer / more urgent option.")

red_flags = {
    "Severe bleeding that will not stop": False,
    "Bone visible through a wound": False,
    "The injured limb or joint looks badly deformed or is at an unusual angle": False,
    "Fingers or toes are blue, very pale, cold, or numb": False,
    "Unconsciousness, confusion, seizure, or difficulty staying awake": False,
    "Trouble breathing or chest pain": False,
    "Serious head, neck, or back injury": False,
}

urgent_flags = {
    "I cannot use the injured limb normally": False,
    "I cannot put weight on the injured foot or leg": False,
    "Pain is severe or getting worse": False,
    "There is a lot of swelling or bruising": False,
    "Movement is very limited": False,
    "There is an open wound (but not severe bleeding)": False,
}

selected_red = []
selected_urgent = []

left, right = st.columns(2)
with left:
    st.subheader("Emergency warning signs")
    for label in red_flags:
        if st.checkbox(label, key=f"red_{label}"):
            selected_red.append(label)

with right:
    st.subheader("Needs prompt medical assessment")
    for label in urgent_flags:
        if st.checkbox(label, key=f"urgent_{label}"):
            selected_urgent.append(label)

pain_level = st.select_slider(
    "How strong is the pain?",
    options=["No pain", "Mild", "Moderate", "Severe"],
    value="Mild",
)
extra = st.text_area(
    "Anything else you want to mention? (Optional)",
    placeholder="Describe symptoms in your own words. Do not include your full name, address, or other identifying details.",
)

st.header("3. Get guidance")

if st.button("Assess urgency", type="primary", use_container_width=True):
    st.divider()

    if selected_red:
        st.error("EMERGENCY — get help now")
        st.markdown(
            """
**Call 112 in Romania now**, or ask someone nearby to call. Get a trusted adult immediately.

- Do not wait for an online assessment or keep chatting with the app.
- Avoid moving the injured area unnecessarily.
- Do not try to straighten a deformed limb, put a joint back in place, or push a visible bone back in.
- Follow the emergency operator's instructions.
"""
        )
        st.caption("This result is triggered by the warning signs you selected.")

    elif selected_urgent or pain_level == "Severe":
        st.warning("PROMPT MEDICAL ASSESSMENT — involve an adult and get checked")
        st.markdown(
            """
Your answers include symptoms that can occur with injuries needing professional assessment.
A sprain, fracture, or dislocation can be difficult to distinguish without an examination.

**What to do while arranging help:**
- Stop the activity and avoid putting weight on or using the injured part.
- Keep it supported in the position that feels most comfortable.
- A cold pack wrapped in a towel may help with pain and swelling. Never put ice directly on skin.
- Do not attempt to straighten the limb or put a joint back in place.
- Tell a parent, guardian, school nurse, teacher, or another trusted adult and arrange medical assessment promptly.

If the area becomes blue, pale, cold or numb, the injury becomes deformed, or the person becomes very unwell, call 112.
"""
        )
    else:
        st.info("LOWER URGENCY BASED ON THE ANSWERS — keep monitoring")
        st.markdown(
            """
Your answers did not select one of this prototype's urgent warning signs. That **does not rule out**
a fracture or another injury.

- Stop activities that cause pain and rest the injured area.
- A cold pack wrapped in a towel may help with discomfort or swelling. Never put ice directly on skin.
- Tell a trusted adult what happened.
- Get medical advice if pain, swelling, bruising, or difficulty using the area develops, persists, or gets worse.

If you are worried, unsure, or the injury feels more serious than these questions capture, choose medical assessment.
"""
        )

    st.divider()
    st.subheader("A note about privacy")
    st.write(
        "This prototype does not save your answers or send them to an AI service. "
        "Avoid entering identifying details."
    )

st.markdown("---")
st.caption(
    "Prototype only. Not for diagnosis, treatment decisions, or emergencies. "
    "The checklist is incomplete and must be reviewed by qualified medical professionals before real-world use."
)

with st.expander("Sources used to shape this prototype"):
    st.markdown(
        """
- [American Heart Association / American Red Cross — 2024 First Aid Guidelines](https://cpr.heart.org/en/resuscitation-science/2024-first-aid-guidelines)
- [NHS — Broken ankle](https://www.nhs.uk/conditions/broken-ankle/)
- [British Red Cross — Broken bones and fractures](https://www.redcross.org.uk/first-aid/learn-first-aid/broken-bone)
- [WHO — Ethics and governance of AI for health](https://www.who.int/publications/i/item/9789240084759)
"""
    )
