import streamlit as st

# ── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(page_title="Survey", page_icon="📝", layout="centered")

# ── Block direct access ───────────────────────────────────────────────────────
if not st.session_state.get('consent_given', False):
    st.warning("Please start from the welcome page.")
    if st.button("Go to welcome page"):
        st.switch_page("app.py")
    st.stop()

if st.session_state.get('persona_key') is None:
    st.warning("Please complete the profile quiz first.")
    if st.button("Go to profile quiz"):
        st.switch_page("pages/1_Profile_Quiz.py")
    st.stop()

# ── Survey items by construct ─────────────────────────────────────────────────
# 4 constructs x 3 items = 12 Likert items
# Wording mirrors the survey design fixed in Chapter 3.

# The matched persona's name, for use in the item wording
PERSONA_DISPLAY = {
    'maria': 'Maria', 'james': 'James', 'leila': 'Leila',
    'david': 'David', 'sophie': 'Sophie', 'aisha': 'Aisha',
}
persona_name = PERSONA_DISPLAY.get(st.session_state.get('persona_key'), 'this user')

SURVEY_ITEMS = {
    'Perceived Usefulness': [
        ('u1', "The explanations helped me understand why each recipe was recommended."),
        ('u2', "The explanations gave enough information to judge whether the recipes suited "
               f"{persona_name}."),
        ('u3', f"The explanations clearly connected each recipe to {persona_name}'s health goal "
               "and preferences."),
    ],
    'Satisfaction': [
        ('s1', "I was satisfied with the quality of the explanations."),
        ('s2', f"The explanations felt well-tailored to {persona_name} rather than generic."),
        ('s3', "I would want explanations like these in a food recommendation app I use regularly."),
    ],
    'Perceived Accuracy and Trust': [
        ('t1', "The nutritional information in the explanations seemed accurate."),
        ('t2', f"The explanations were consistent with {persona_name}'s dietary profile as shown."),
        ('t3', "I felt confident the explanations were based on reliable information."),
    ],
    'Clarity': [
        ('c1', "The explanations were easy to understand."),
        ('c2', "The explanations were the right length, not too long and not too short."),
        ('c3', "The language used in the explanations was natural and readable."),
    ],
}

LIKERT = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']

# ── Page UI ───────────────────────────────────────────────────────────────────
st.title("How would you rate the explanations?")
st.markdown(
    "Please rate how strongly you agree or disagree with each statement below. "
    "Think about the explanations you just read for all five recipes."
)
st.markdown("---")

# Initialise the dictionary that will hold all responses
if 'survey_responses' not in st.session_state:
    st.session_state.survey_responses = {}

# ── Render each construct as a section ────────────────────────────────────────
all_answered = True

for construct_name, items in SURVEY_ITEMS.items():
    st.subheader(construct_name)
    for item_id, question_text in items:
        response = st.radio(
            question_text,
            options=LIKERT,
            index=None,
            key=item_id,
            horizontal=True,
        )
        if response is None:
            all_answered = False
        else:
            st.session_state.survey_responses[item_id] = response
    st.markdown(" ")

st.markdown("---")

# ── Open-ended question ───────────────────────────────────────────────────────
st.subheader("Final question")
open_response = st.text_area(
    "Is there anything about the explanations that you found particularly "
    "helpful or unhelpful? Please describe in your own words. (Optional)",
    height=150,
    key='open_question',
)
st.session_state.survey_responses['open_response'] = open_response

st.markdown("---")

# ── Submit button ─────────────────────────────────────────────────────────────
if not all_answered:
    st.info("Please answer all 12 rating questions above to submit.")
else:
    if st.button("Submit my responses", type="primary"):
        st.session_state.survey_submitted = True
        st.switch_page("pages/4_Thank_You.py")