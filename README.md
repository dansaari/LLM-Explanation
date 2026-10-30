# Grounded LLM explanations for healthy food recommendations

Code and study materials for the master's thesis *Grounded LLM explanations for healthy food recommendations: a design science study of user perception and verification* 

The project builds a recipe recommender that explains each recommendation in plain language with a large language model (LLM), checks every explanation against the facts it was generated from, and evaluates the explanations with users.

![Python 3.11](https://img.shields.io/badge/python-3.11-blue)
![Streamlit 1.57](https://img.shields.io/badge/streamlit-1.57-red)
![Licence: MIT](https://img.shields.io/badge/licence-MIT-green)

## Contents

- [Study design](#study-design)
- [Repository structure](#repository-structure)
- [The study application](#the-study-application)
- [The pipeline notebook](#the-pipeline-notebook)
- [Data](#data)
- [Citation](#citation)
- [Licence](#licence)

## Study design

![Study design: the artefact, the human evaluation and the grounding verification](docs/images/study_design.png)

The artefact recommends five recipes from the HUMMUS dataset to each of six personas, each with a distinct health goal. Gemma 4 31B writes a short explanation for every recommendation from a fixed set of verified facts. The explanations contain no numbers: exact nutrition values are shown in a separate panel instead.

The explanations are evaluated in two layers:

1. **Human evaluation.** Participants answer one question about their main health goal, are matched to the persona with that goal, and rate that persona's five explanations on a twelve-item survey.
2. **Grounding verification and judge validation.** Each explanation is split into claims. Two LLM judges from different model families check every claim against the facts given to the generator, and a third model decides their disagreements. The judges are then tested with 48 planted errors and against a blind annotation of 152 claims by three people.

## Repository structure

```
.
├── app.py                        Welcome and consent page of the study app
├── pages/
│   ├── 1_Profile_Quiz.py         Health-goal question and persona matching
│   ├── 2_Recommendations.py      Persona brief and five recipe cards
│   ├── 3_Survey.py               Twelve-item survey and open question
│   └── 4_Thank_You.py            Saves the response to Google Sheets
├── data/
│   └── explanations_FROZEN.csv   The 30 explanations shown to participants
├── data_exploration.ipynb        The full pipeline, from data cleaning to judge validation
├── docs/images/                  Figures used in this README
├── requirements.txt              Packages for the study app
└── requirements-notebook.txt     Additional packages for the notebook
```

## The study application

The app is a multi-page Streamlit application. It is kept exactly as it was used in the study (September 2026).

<p align="center">
  <img src="docs/images/app_recipe_card.png" alt="A recipe card from the study application" width="460">
</p>

<p align="center"><em>A recipe card for the high-protein persona: Nutri-Score badge, exact nutrition values, ingredients and the number-free explanation.</em></p>

### Run it locally

```bash
git clone https://github.com/dansaari/Food-explainer.git
cd Food-explainer
python -m venv venv
source venv/bin/activate          # on Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

The app reads its explanations from `data/explanations_FROZEN.csv`, so it runs without any API keys. Saving responses needs a Google service account. Without one, the app runs normally and the last page reports that the response could not be saved. To enable saving, copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and fill in your own values. The secrets file is excluded from version control.

## The pipeline notebook

`data_exploration.ipynb` contains the whole pipeline. Its sections map to the thesis as follows.

| Notebook section | What it does | Thesis |
| --- | --- | --- |
| 1 to 2 | Load and clean HUMMUS | 3.4.1 |
| 3 to 6 | Tag mappings, personas, recommender, diversity check | 3.4.2, Appendix 1 |
| 7 | Explanation generation (30 study and 72 validation explanations) | 3.4.3 |
| 8 | Functional tests of the hard constraints | Appendix 1 |
| 9 to 13 | Judge setup, claim-level judging, grounding verdicts, agreement | 3.4.4, 3.5.2, 4.3 |
| 14 | Adversarial cases with planted errors | 3.5.2, 4.4.4 |
| 15 | Freezing the study set | 3.4.3 |
| 16 | Annotation workbook, development findings, third judge | 3.5.2, 4.4 |

### Models

All models were accessed through Lehmus AI, an OpenAI-compatible gateway provided by the university.

| Role | Model | Settings |
| --- | --- | --- |
| Generator | Gemma 4 31B | Default temperature; one model for the whole set |
| Judge 1 | Qwen3.6-35B-A3B | Temperature 0 |
| Judge 2 | GPT-OSS 120B | Temperature 0 |
| Third model for disagreements | Muse-Glimmer-30B-NVFP4 | Temperature 0 |

LLM output varies between runs, so a re-run will not reproduce the frozen explanations word for word.

### Run it

```bash
pip install -r requirements.txt -r requirements-notebook.txt
```

Create a `.env` file in the repository root (excluded from version control):

```
LEHMUS_API_KEY=...
LEHMUS_BASE_URL=...
LEHMUS_API_KEY_2=...      # only needed for the third model in section 16
```

Then place the HUMMUS recipe file in `data/` (see below) and run the notebook from the top.

## Data

| Data | In this repository | Notes |
| --- | --- | --- |
| HUMMUS recipes (`pp_recipes.csv`) | No | Download from the [HUMMUS data set repository](https://gitlab.com/felix134/connected-recipe-data-set) and place it in `data/`. Its terms of use apply. |
| Frozen study explanations | Yes | `data/explanations_FROZEN.csv`: the 30 explanations, their facts and nutrition values. Recipe titles and links refer to Food.com. |
| Validation explanations, claims, judge verdicts, adversarial cases | No | Produced by the notebook. |
| Survey responses | No | Individual responses are not published. Aggregate results are reported in the thesis. |

No personal information was collected. Participants were matched to a persona by their answer to one question, and no participant data was sent to a language model.


## Citation

If you use this code, please cite the thesis:

> Daniel Saari. 2026. Grounded LLM explanations for healthy food recommendations: a design science study of user perception and verification. Master's thesis. Oulu University of Applied Sciences.

GitHub also offers a citation from `CITATION.cff` under **Cite this repository** on the repository page.

The recipe data comes from:

> Bölz, F., Nurbakova, D., Calabretto, S., Gerl, A., Brunie, L. & Kosch, H. 2023. HUMMUS: A linked, healthiness-aware, user-centered and argument-enabling recipe data set for recommendation. In Proceedings of the 17th ACM Conference on Recommender Systems (RecSys '23). ACM, Singapore.

## Licence

The code and the frozen explanations are released under the [MIT Licence](LICENSE). The HUMMUS data set and the Food.com recipes it is built on are not part of this licence and remain subject to their own terms.
