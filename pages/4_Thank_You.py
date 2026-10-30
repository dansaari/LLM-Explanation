import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# ── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(page_title="Thank you", page_icon="✅", layout="centered")

# ── Block direct access ───────────────────────────────────────────────────────
if not st.session_state.get('survey_submitted', False):
    st.warning("Please complete the survey first.")
    if st.button("Go to welcome page"):
        st.switch_page("app.py")
    st.stop()


# ── Google Sheets connection ──────────────────────────────────────────────────
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# Column order for the sheet — matches the header row exactly
COLUMNS = [
    'participant_id', 'timestamp', 'persona_key', 'matched_health_goal',
    'u1', 'u2', 'u3', 's1', 's2', 's3', 't1', 't2', 't3', 'c1', 'c2', 'c3',
    'open_response',
    'user_goal_given', 'user_restrictions_given', 'user_cuisines_given',
    'user_allergies_given', 'user_dislikes_given',
]


def get_worksheet():
    """Authorise and return the first worksheet of the configured Sheet."""
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=SCOPES
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_url(st.secrets["sheet_url"])
    ws = sheet.sheet1
    # Ensure a header row exists (only writes it once, when sheet is empty)
    if ws.row_count == 0 or not ws.get_all_values():
        ws.append_row(COLUMNS, table_range="A1")
    return ws


def save_response_once():
    """Save the participant's response to Google Sheets, exactly once."""
    if st.session_state.get('response_saved', False):
        return True  # already saved this session

    persona_key = st.session_state.get('persona_key')
    user_answers = st.session_state.get('user_answers', {})
    responses = st.session_state.get('survey_responses', {})

    now = datetime.now()
    participant_id = f"P-{now.strftime('%Y-%m-%d-%H%M%S')}"

    persona_meta = {
        'maria': 'Cardiovascular Health', 'james': 'High Protein Diet',
        'leila': 'Weight Loss', 'david': 'Diabetic Management',
        'sophie': 'General Healthy Eating', 'aisha': 'Low Fat Diet',
    }

    row = {
        'participant_id': participant_id,
        'timestamp': now.strftime('%Y-%m-%d %H:%M:%S'),
        'persona_key': persona_key,
        'matched_health_goal': persona_meta.get(persona_key, 'unknown'),
        'u1': responses.get('u1', ''), 'u2': responses.get('u2', ''),
        'u3': responses.get('u3', ''), 's1': responses.get('s1', ''),
        's2': responses.get('s2', ''), 's3': responses.get('s3', ''),
        't1': responses.get('t1', ''), 't2': responses.get('t2', ''),
        't3': responses.get('t3', ''), 'c1': responses.get('c1', ''),
        'c2': responses.get('c2', ''), 'c3': responses.get('c3', ''),
        'open_response': responses.get('open_response', ''),
        'user_goal_given': user_answers.get('health_goal', ''),
        'user_restrictions_given': ', '.join(user_answers.get('dietary_restrictions', [])),
        'user_cuisines_given': ', '.join(user_answers.get('cuisine_preferences', [])),
        'user_allergies_given': ', '.join(user_answers.get('allergies', [])),
        'user_dislikes_given': ', '.join(user_answers.get('dislikes', [])),
    }

    try:
        ws = get_worksheet()
        ws.append_row(
            [str(row[col]) for col in COLUMNS],
            table_range="A1",
            value_input_option="RAW",
        )
        st.session_state.response_saved = True
        st.session_state.participant_id = participant_id
        return True
    except Exception as e:
        # Don't crash the participant — record the failure for the researcher
        st.session_state.save_error = str(e)
        st.session_state.participant_id = participant_id
        return False


saved_ok = save_response_once()

# ── Thank you content ─────────────────────────────────────────────────────────
st.title("Thank you for taking part 🙏🏿")

if saved_ok:
    st.markdown(
        """
Your responses have been saved. They will be used as part of a master's thesis
on AI-generated food recommendation explanations.

You may now close this window.
"""
    )
else:
    # Participant still sees a graceful message; you get the diagnostic.
    st.markdown(
        """
Thank you — your part is complete. You may now close this window.
"""
    )
    st.caption(
        "Note: there was a technical issue recording the response automatically. "
        "If you are the researcher, check the app logs."
    )
    with st.expander("Technical details (researcher only)"):
        st.code(st.session_state.get('save_error', 'unknown error'))

st.markdown("---")
st.caption(
    f"Your anonymous participation ID: "
    f"**{st.session_state.get('participant_id', 'unknown')}**"
)

with st.expander("Questions about this study?"):
    st.markdown(
        """
If you have any questions about the study, you can contact the researcher
through the channel by which you received the link to this study.

Your responses are anonymous. No identifying information was collected.
"""
    )