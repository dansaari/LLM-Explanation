import streamlit as st
import pandas as pd
import os

# ── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(page_title="Your Recommendations", page_icon="🥗", layout="centered")


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


# ── Load pre-generated explanations from CSV ──────────────────────────────────
@st.cache_data
def load_explanations():
    """Load the frozen CSV of explanations. Cached so it only reads once."""
    path = 'data/explanations_FROZEN.csv'
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path)


# ── Persona display names ─────────────────────────────────────────────────────
PERSONA_NAMES = {
    'maria':  ('Maria',  45, 'Cardiovascular Health'),
    'james':  ('James',  32, 'High Protein Diet'),
    'leila':  ('Leila',  28, 'Weight Loss'),
    'david':  ('David',  55, 'Diabetic Management'),
    'sophie': ('Sophie', 38, 'General Healthy Eating'),
    'aisha':  ('Aisha',  34, 'Low Fat Diet'),
}


# ── NutriScore colour mapping ─────────────────────────────────────────────────
NUTRI_COLOURS = {
    'A': '#2E7D32',  # dark green
    'B': '#7CB342',  # light green
    'C': '#FBC02D',  # yellow
    'D': '#F57C00',  # orange
    'E': '#C62828',  # red
}


# ── Page content ──────────────────────────────────────────────────────────────
persona_key = st.session_state.persona_key
name, age, goal = PERSONA_NAMES[persona_key]


st.title("Your Personalised Recommendations")
st.markdown(
    f"Showing recommendations as **{name}**, age {age}, with a focus on **{goal}**."
)
st.markdown("---")

# after computing name, age, goal
# ── Persona profile the participant is evaluating for ─────────────────────────
PERSONA_PROFILES = {
    'maria':  ('low-sodium',                'American and European'),
    'james':  ('dairy-free',                'European and American'),
    'leila':  ('vegan',                     'European and American'),
    'david':  ('diabetic, low-carb',        'Asian and European'),
    'sophie': ('no specific restrictions',  'European and American'),
    'aisha':  ('dairy-free',                'American and Asian'),
}
diet, cuisine = PERSONA_PROFILES[persona_key]

st.markdown(
    f"""
    <div style='
        background: linear-gradient(180deg, #17212B 0%, #141B24 100%);
        border: 1px solid #2A3644;
        border-radius: 14px;
        padding: 28px 30px;
        margin: 12px 0 6px 0;
    '>
        <div style='display:flex; align-items:center; gap:10px; margin-bottom:18px;'>
            <span style='width:9px; height:9px; border-radius:50%; background:#5EB3F0; display:inline-block;'></span>
            <span style='font-size:0.82em; letter-spacing:0.04em; color:#7E93A8; text-transform:uppercase;'>Reviewer brief</span>
        </div>
        <div style='font-size:1.45em; font-weight:600; color:#F5F8FB; margin-bottom:4px;'>
            {name}
        </div>
        <div style='font-size:0.98em; color:#9FB3C6; margin-bottom:22px;'>
            {age} years old · focus on {goal.lower()}
        </div>
        <div style='display:flex; flex-wrap:wrap; gap:22px 40px; margin-bottom:22px;'>
            <div>
                <div style='font-size:0.8em; color:#7E93A8; margin-bottom:3px;'>Dietary needs</div>
                <div style='font-size:1.02em; color:#E8EEF4; font-weight:500;'>{diet}</div>
            </div>
            <div>
                <div style='font-size:0.8em; color:#7E93A8; margin-bottom:3px;'>Cuisine preference</div>
                <div style='font-size:1.02em; color:#E8EEF4; font-weight:500;'>{cuisine}</div>
            </div>
        </div>
        <div style='font-size:0.97em; color:#B8C7D6; line-height:1.6; border-top:1px solid #2A3644; padding-top:18px;'>
            As you read each explanation, judge how well it serves {name}'s profile — rather than your own food preferences.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Load and filter to this persona's 5 recipes
df = load_explanations()
if df.empty:
    st.error(
        "No explanations found. The data file is missing. "
        "Please contact the researcher."
    )
    st.stop()

persona_recipes = df[df['persona_key'] == persona_key].reset_index(drop=True)

if len(persona_recipes) == 0:
    st.error(f"No recommendations found for {name}.")
    st.stop()

# Save the recipes for the survey page to reference
st.session_state.shown_recipes = persona_recipes['recipe_title'].tolist()

st.markdown("---")

# ── Show each recipe card ─────────────────────────────────────────────────────
st.markdown(f"Here are five recipes selected for you. Read each one carefully — "
            f"you will be asked about the explanations on the next page.")
st.markdown(" ")

for i, row in persona_recipes.iterrows():
    nutri = row['nutri_grade']
    colour = NUTRI_COLOURS.get(nutri, '#666666')

    with st.container(border=True):
        # Title and NutriScore badge in one row
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"### {i + 1}. {row['recipe_title']}")
        with col2:
            st.markdown(
                f"<div style='background-color:{colour}; color:white; "
                f"padding:8px; border-radius:8px; text-align:center; "
                f"font-weight:bold; font-size:1.2em;'>"
                f"NutriScore<br>{nutri}</div>",
                unsafe_allow_html=True,
            )

        # Recipe details in two columns
        st.markdown(" ")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Calories:** {row['calories']:.0f} per serving")
            st.markdown(f"**Protein:** {row['protein_g']:.1f} g")
            st.markdown(f"**Sodium:** {row['sodium_mg']:.0f} mg")
        with c2:
            st.markdown(f"**Total fat:** {row['total_fat_g']:.1f} g")
            st.markdown(f"**Sugars:** {row['sugars_g']:.1f} g")
            st.markdown(f"**Fiber:** {row['fiber_g']:.1f} g")

        st.markdown(" ")

        # Ingredients (from the frozen CSV, cleaned for display)
        st.markdown(" ")
        import ast
        try:
            ingredients = ast.literal_eval(row['ingredients_display']) if isinstance(row['ingredients_display'], str) else row['ingredients_display']
        except (ValueError, SyntaxError):
            ingredients = []
        if ingredients:
            st.markdown(f"**Ingredients:** {', '.join(ingredients)}")

        st.markdown(" ")
        st.markdown("**Why this recipe was recommended:**")
        st.info(row['explanation'])

        # Link to the full recipe
        if pd.notna(row.get('recipe_url', None)) and row.get('recipe_url'):
            st.markdown(f"[View the full recipe ↗]({row['recipe_url']})")

# ── Continue button ───────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "When you have read all five explanations, click below to rate them."
)
if st.button("Continue to survey →", type="primary"):
    st.switch_page("pages/3_Survey.py")