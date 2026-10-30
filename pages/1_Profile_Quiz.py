import streamlit as st

st.set_page_config(page_title="Profile Quiz", page_icon="🥗", layout="centered")

if not st.session_state.get('consent_given', False):
    st.warning("Please start from the welcome page.")
    if st.button("Go to welcome page"):
        st.switch_page("app.py")
    st.stop()

# ── Personas (must match the frozen explanation set exactly) ──────────────────
TEST_PERSONAS = {
    'maria':  {'name': 'Maria',  'age': 45,
               'health_goal': 'Cardiovascular Health',
               'dietary_restrictions': ['low-sodium'],
               'cuisine_preferences': ['american', 'european'],
               'disliked_ingredients': ['anchovies', 'sardines'],
               'allergies': []},
    'james':  {'name': 'James',  'age': 32,
               'health_goal': 'High Protein Diet',
               'dietary_restrictions': ['dairy-free'],
               'cuisine_preferences': ['european', 'american'],
               'disliked_ingredients': [],
               'allergies': ['peanuts']},
    'leila':  {'name': 'Leila',  'age': 28,
               'health_goal': 'Weight Loss',
               'dietary_restrictions': ['vegan'],
               'cuisine_preferences': ['european', 'american'],
               'disliked_ingredients': [],
               'allergies': []},
    'david':  {'name': 'David',  'age': 55,
               'health_goal': 'Diabetic Management',
               'dietary_restrictions': ['diabetic', 'low-carb'],
               'cuisine_preferences': ['asian', 'european'],
               'disliked_ingredients': ['blue cheese'],
               'allergies': []},
    'sophie': {'name': 'Sophie', 'age': 38,
               'health_goal': 'General Healthy Eating',
               'dietary_restrictions': [],
               'cuisine_preferences': ['european', 'american'],
               'disliked_ingredients': ['tree nuts'],
               'allergies': ['tree nuts']},
    'aisha':  {'name': 'Aisha',  'age': 34,
               'health_goal': 'Low Fat Diet',
               'dietary_restrictions': ['dairy-free'],
               'cuisine_preferences': ['american', 'asian'],
               'disliked_ingredients': ['mayonnaise'],
               'allergies': []},
}


def find_closest_persona(user_answers):
    """Map the participant to the persona whose health goal they selected.
    Each of the six personas has a unique health goal, so the stated goal
    deterministically identifies the closest persona."""
    for key, persona in TEST_PERSONAS.items():
        if user_answers['health_goal'] == persona['health_goal']:
            return key, persona
    # fallback (shouldn't happen since options == persona goals)
    first = list(TEST_PERSONAS.keys())[0]
    return first, TEST_PERSONAS[first]


st.title("Tell us about your food preferences")
st.markdown(
    "Answer these short question. Your answer will be used to match you with "
    "a profile that shapes your recommendations. This takes about a minute."
)
st.markdown("---")

# Question 1 — Health goal (primary discriminator)
health_goal = st.radio(
    "**1. What is your main food-related health goal?**",
    options=[
        'Cardiovascular Health',
        'High Protein Diet',
        'Weight Loss',
        'Diabetic Management',
        'General Healthy Eating',
        'Low Fat Diet',
    ],
    index=None,
)

st.markdown("---")

ready = health_goal is not None

if not ready:
    st.info("Please select your main health goal to continue.")
else:
    if not st.session_state.get('persona_matched', False):
        if st.button("Find my recommendations", type="primary"):
            user_answers = {
                'health_goal': health_goal,
                'dietary_restrictions': [],
                'cuisine_preferences': [],
                'allergies': [],
                'dislikes': [],
            }
            persona_key, persona = find_closest_persona(user_answers)
            st.session_state.persona_key = persona_key
            st.session_state.user_answers = user_answers
            st.session_state.matched_persona = persona
            st.session_state.persona_matched = True
            st.rerun()
    else:
        persona = st.session_state.matched_persona
        st.success(
            f"Based on your answer you will explore recommendations as "
            f"**{persona['name']}**, who shares your focus on "
            f"**{persona['health_goal'].lower()}**."
        )
        st.markdown(" ")
        if st.button("Continue to recommendations →", type="primary"):
            st.switch_page("pages/2_Recommendations.py")