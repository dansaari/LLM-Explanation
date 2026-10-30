import streamlit as st

# ── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Food Recommendation Explanation Study",
    page_icon="🥗",
    layout="centered"
)

# ── Initialise session state ──────────────────────────────────────────────────
if 'consent_given' not in st.session_state:
    st.session_state.consent_given = False
if 'persona_key' not in st.session_state:
    st.session_state.persona_key = None
if 'ratings' not in st.session_state:
    st.session_state.ratings = {}

# ── Welcome page ──────────────────────────────────────────────────────────────
st.title("Food Recommendation Explanation Study")

st.markdown("""
### Welcome and thank you for taking part.

This is a master's thesis study on how AI-generated explanations 
can help people make food choices. You will:

1. Answer a short profile quiz
2. View 5 personalised recipe recommendations with explanations
3. Rate the explanations on a short survey (about 5 minutes)

**Total time:** approximately 7-10 minutes.

---

### Your data and privacy

- No personally identifiable information is collected.
- Your responses are anonymous and used only for this thesis.
- The food recommendations are simulated for research purposes — 
  please do not act on them as real dietary advice.

---
""")

consent = st.checkbox(
    "I have read the above and consent to take part in this study.",
    value=st.session_state.consent_given
)

if consent:
    st.session_state.consent_given = True
    if st.button("Begin the study", type="primary"):
        st.switch_page("pages/1_Profile_Quiz.py")
else:
    st.info("Please check the consent box above to continue.")

st.markdown("---")
st.caption("Master's thesis")