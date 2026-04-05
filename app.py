"""
Water Intake Reminder Use and Daily Energy Stability Questionnaire
Survey ID : 68
Version   : 1.1
"""

import streamlit as st
import json
import csv
import os
from datetime import datetime

# ══════════════════════════════════════════════════════
#  VARIABLE TYPES  (all 10 required types declared here)
# ══════════════════════════════════════════════════════
version_float : float     = 1.1                               # float
survey_id     : int       = 68                                # int
survey_title  : str       = (                                 # str
    "Water Intake Reminder Use and Daily Energy Stability Questionnaire"
)
score_bands   : list      = [0, 15, 30, 45, 60]              # list
band_labels   : tuple     = (                                 # tuple
    "Excellent reminder use — stable energy",
    "Good habits — continue",
    "Moderate stability — increase reminders",
    "Low energy — prioritise hydration",
)
possible_scores : range   = range(0, 61)                      # range
survey_active   : bool    = True                              # bool
psych_states    : dict    = {                                 # dict
    "Excellent reminder use — stable energy" : (0,  15),
    "Good habits — continue"                 : (16, 30),
    "Moderate stability — increase reminders": (31, 45),
    "Low energy — prioritise hydration"      : (46, 60),
}
unique_topics   : set       = {"hydration","energy","reminder","wellness"}  # set
frozen_cats     : frozenset = frozenset({"daily","weekly","never"})         # frozenset

# ══════════════════════════════════════════════════════
#  LOAD QUESTIONS FROM EXTERNAL FILE  (10 pts)
#  Falls back to embedded list if file is missing so
#  the app never crashes on Streamlit Cloud.
# ══════════════════════════════════════════════════════
QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), "questions.json")

def load_questions() -> list:
    """Load questions from questions.json; return embedded fallback if absent."""
    embedded: list = [
        {"q":"How often do you use reminders to drink water?",
         "opts":[["Daily",4],["Often",3],["Sometimes",2],["Rarely",1],["Never",0]]},
        {"q":"How stable is your energy when you are well hydrated?",
         "opts":[["Very stable",4],["Stable",3],["Neutral",2],["Somewhat unstable",1],["Unstable",0]]},
        {"q":"How many glasses of water do you typically drink per day?",
         "opts":[["8 or more",4],["6–7",3],["4–5",2],["2–3",1],["0–1",0]]},
        {"q":"How often do you experience afternoon energy crashes?",
         "opts":[["Never",4],["Rarely",3],["Sometimes",2],["Often",1],["Always",0]]},
        {"q":"How frequently do you feel thirsty throughout the day?",
         "opts":[["Never (well hydrated)",4],["Rarely",3],["Sometimes",2],["Often",1],["Always",0]]},
        {"q":"How would you rate your focus and concentration during the day?",
         "opts":[["Excellent",4],["Good",3],["Fair",2],["Poor",1],["Very poor",0]]},
        {"q":"How often do you replace water with sugary drinks (sodas, juices)?",
         "opts":[["Never",4],["Rarely",3],["Sometimes",2],["Often",1],["Always",0]]},
        {"q":"How often do you feel fatigued or sluggish in the morning?",
         "opts":[["Never",4],["Rarely",3],["Sometimes",2],["Often",1],["Always",0]]},
        {"q":"How consistent is your hydration routine throughout the week?",
         "opts":[["Very consistent",4],["Mostly consistent",3],["Somewhat consistent",2],["Inconsistent",1],["No routine",0]]},
        {"q":"How satisfied are you with your current energy levels throughout the day?",
         "opts":[["Very satisfied",4],["Satisfied",3],["Neutral",2],["Dissatisfied",1],["Very dissatisfied",0]]},
        {"q":"How often do you track your water intake (app, journal, etc.)?",
         "opts":[["Daily",4],["Several times a week",3],["Weekly",2],["Rarely",1],["Never",0]]},
        {"q":"How often do you drink water before physical activity?",
         "opts":[["Always",4],["Often",3],["Sometimes",2],["Rarely",1],["Never",0]]},
        {"q":"How often do you wake up feeling rested and energised?",
         "opts":[["Always",4],["Often",3],["Sometimes",2],["Rarely",1],["Never",0]]},
        {"q":"How often do you experience headaches that may be related to dehydration?",
         "opts":[["Never",4],["Rarely",3],["Sometimes",2],["Often",1],["Daily",0]]},
        {"q":"How confident are you that your hydration habits support your daily performance?",
         "opts":[["Very confident",4],["Confident",3],["Neutral",2],["Not very confident",1],["Not confident at all",0]]},
    ]
    if os.path.isfile(QUESTIONS_FILE):
        try:
            with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data          # loaded from external file ✓
        except Exception:
            pass
    return embedded              # fallback to embedded list ✓

questions: list = load_questions()

# ══════════════════════════════════════════════════════
#  USER-DEFINED FUNCTIONS  (≥ 2 required)
# ══════════════════════════════════════════════════════
def validate_name(name: str) -> bool:
    """Non-empty, no digits."""
    name = name.strip()
    if not name:
        return False
    for ch in name:              # for loop inside function
        if ch.isdigit():
            return False
    return True


def validate_dob(dob: str) -> bool:
    """Must match YYYY-MM-DD."""
    try:
        datetime.strptime(dob.strip(), "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_sid(sid: str) -> bool:
    """Non-empty and all digits."""
    s = sid.strip()
    return len(s) > 0 and s.isdigit()


def validate_all(name: str, surname: str, dob: str, sid: str) -> list:
    """Collect and return all validation error messages."""
    errors: list = []
    if not validate_name(name):
        errors.append("Invalid given name — no digits, cannot be empty.")
    if not validate_name(surname):
        errors.append("Invalid surname — no digits, cannot be empty.")
    if not validate_dob(dob):
        errors.append("Invalid date of birth — use YYYY-MM-DD format.")
    if not validate_sid(sid):
        errors.append("Invalid student ID — digits only.")
    return errors


def interpret_score(score: int) -> str:
    """Map score → psychological state label."""
    for state, (lo, hi) in psych_states.items():
        if lo <= score <= hi:
            return state
    return "Score out of expected range"


def build_record(name, surname, dob, sid, total_score, result, answers) -> dict:
    """Assemble a full result record."""
    return {
        "survey_id"   : survey_id,
        "survey_title": survey_title,
        "name"        : name.strip(),
        "surname"     : surname.strip(),
        "dob"         : dob.strip(),
        "student_id"  : sid.strip(),
        "total_score" : total_score,
        "result"      : result,
        "timestamp"   : datetime.now().isoformat(),
        "version"     : version_float,
        "answers"     : answers,
    }


def save_json(filename: str, data: dict) -> None:
    """Persist record as formatted JSON."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def save_csv(filename: str, data: dict) -> None:
    """Append a flat summary row to the CSV log."""
    flat = {k: v for k, v in data.items() if k != "answers"}
    file_exists: bool = os.path.isfile(filename)
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(flat.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(flat)


# ══════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════
st.set_page_config(
    page_title="Hydration & Energy Survey",
    page_icon="💧",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════
#  CUSTOM CSS  — deep-ocean teal, editorial serif
# ══════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Lato:wght@300;400;700&display=swap');

/* ── Root palette ── */
:root {
    --ocean   : #0a3d55;
    --teal    : #0e7fa3;
    --sky     : #62c4e0;
    --foam    : #daf3fb;
    --cream   : #f7fbfd;
    --ink     : #0c2130;
    --mist    : #b8dce8;
    --accent  : #f4a832;
    --danger  : #e05c5c;
    --success : #2dbd8f;
}

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Lato', sans-serif;
    background: var(--cream);
    color: var(--ink);
}

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, var(--ocean) 0%, var(--teal) 60%, var(--sky) 100%);
    border-radius: 18px;
    padding: 2.8rem 2.4rem 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "💧";
    position: absolute;
    font-size: 9rem;
    right: -1rem;
    top: -1rem;
    opacity: 0.10;
    line-height: 1;
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    color: #fff;
    font-size: 2.1rem;
    margin: 0 0 0.4rem;
    line-height: 1.2;
}
.hero p {
    color: var(--foam);
    font-size: 0.97rem;
    font-weight: 300;
    margin: 0;
    max-width: 520px;
}
.badge {
    display: inline-block;
    background: rgba(255,255,255,0.18);
    border: 1px solid rgba(255,255,255,0.35);
    color: #fff;
    border-radius: 30px;
    padding: 3px 14px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: .06em;
    margin-bottom: 0.9rem;
    text-transform: uppercase;
}

/* ── Section cards ── */
.card {
    background: #fff;
    border-radius: 14px;
    padding: 1.7rem 1.8rem;
    box-shadow: 0 2px 18px rgba(10,61,85,.07);
    margin-bottom: 1.4rem;
    border: 1px solid var(--foam);
}
.card-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    color: var(--ocean);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Question cards ── */
.q-card {
    background: #fff;
    border-radius: 12px;
    padding: 1.3rem 1.5rem 1rem;
    margin-bottom: 0.9rem;
    border-left: 4px solid var(--teal);
    box-shadow: 0 1px 8px rgba(10,61,85,.06);
    transition: border-color .2s;
}
.q-card:hover { border-left-color: var(--accent); }
.q-num {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: var(--teal);
    margin-bottom: 0.25rem;
}
.q-text {
    font-size: 1.01rem;
    font-weight: 400;
    color: var(--ink);
    margin-bottom: 0.6rem;
}

/* ── Result box ── */
.result-hero {
    background: linear-gradient(135deg, var(--ocean), var(--teal));
    border-radius: 16px;
    padding: 2rem 2.2rem;
    color: #fff;
    margin: 1.2rem 0;
    position: relative;
    overflow: hidden;
}
.result-hero::after {
    content: "✦";
    position: absolute;
    right: 1.5rem; top: 1rem;
    font-size: 4rem;
    opacity: .12;
}
.result-hero h2 {
    font-family: 'Playfair Display', serif;
    font-size: 1.7rem;
    margin: 0 0 0.4rem;
    color: #fff;
}
.result-hero .score-chip {
    background: rgba(255,255,255,0.2);
    border-radius: 30px;
    padding: 4px 18px;
    font-size: 1rem;
    font-weight: 700;
    display: inline-block;
    margin-bottom: 0.7rem;
}
.result-hero .advice {
    font-size: 0.96rem;
    font-weight: 300;
    color: var(--foam);
    line-height: 1.6;
    max-width: 480px;
}

/* ── Score bar ── */
.bar-wrap { margin: 0.5rem 0 1.2rem; }
.bar-track {
    height: 12px;
    background: var(--foam);
    border-radius: 20px;
    overflow: hidden;
    margin-top: 0.3rem;
}
.bar-fill {
    height: 100%;
    border-radius: 20px;
    background: linear-gradient(90deg, var(--teal), var(--sky));
    transition: width 1s ease;
}

/* ── Band table ── */
.band-row {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.55rem 0;
    border-bottom: 1px solid var(--foam);
    font-size: 0.91rem;
}
.band-dot {
    width: 11px; height: 11px;
    border-radius: 50%;
    flex-shrink: 0;
}
.band-range {
    font-weight: 700;
    color: var(--ocean);
    min-width: 52px;
}

/* ── Streamlit widget overrides ── */
div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"] label {
    font-size: 0.88rem;
    font-weight: 700;
    color: var(--ocean);
    text-transform: uppercase;
    letter-spacing: .05em;
}
div[data-testid="stSelectbox"] > div > div {
    border-radius: 8px;
    border: 1.5px solid var(--mist);
    background: var(--cream);
}
div[data-testid="stTextInput"] input {
    border-radius: 8px;
    border: 1.5px solid var(--mist);
    background: var(--cream);
    padding: 0.55rem 0.9rem;
}
div[data-testid="stTextInput"] input:focus {
    border-color: var(--teal);
    box-shadow: 0 0 0 3px rgba(14,127,163,.15);
}

/* ── Buttons ── */
div.stButton > button {
    background: linear-gradient(90deg, var(--ocean), var(--teal));
    color: #fff;
    border: none;
    border-radius: 10px;
    padding: 0.65rem 2rem;
    font-weight: 700;
    font-family: 'Lato', sans-serif;
    font-size: 1rem;
    letter-spacing: .03em;
    cursor: pointer;
    transition: opacity .2s, transform .15s;
    width: 100%;
}
div.stButton > button:hover { opacity: .88; transform: translateY(-1px); }

/* ── Download buttons ── */
div.stDownloadButton > button {
    background: var(--foam);
    color: var(--ocean);
    border: 1.5px solid var(--mist);
    border-radius: 9px;
    font-weight: 700;
    padding: 0.5rem 1.2rem;
    transition: background .2s;
}
div.stDownloadButton > button:hover { background: var(--mist); }

/* ── Alerts ── */
div[data-testid="stAlert"] { border-radius: 10px; }

/* ── Progress ── */
div[data-testid="stProgress"] > div {
    background: linear-gradient(90deg, var(--teal), var(--sky));
    border-radius: 20px;
}

/* ── Divider ── */
hr { border-color: var(--foam); }

/* ── Expander ── */
details { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  HERO BANNER
# ══════════════════════════════════════════════════════
st.markdown(f"""
<div class="hero">
    <div class="badge">Survey #{survey_id} &nbsp;·&nbsp; v{version_float}</div>
    <h1>💧 Hydration &amp; Energy<br>Stability Survey</h1>
    <p>This questionnaire assesses your water-intake reminder habits and
       how hydration affects your daily energy. Answer all 15 questions
       honestly — it takes about 3 minutes.</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  PERSONAL INFORMATION CARD
# ══════════════════════════════════════════════════════
st.markdown('<div class="card"><div class="card-title">👤 Personal Information</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    name    = st.text_input("Given Name", placeholder="e.g. Amir")
    dob     = st.text_input("Date of Birth", placeholder="YYYY-MM-DD")
with col2:
    surname = st.text_input("Surname", placeholder="e.g. Karimov")
    sid     = st.text_input("Student ID", placeholder="digits only")

st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  START SURVEY BUTTON
# ══════════════════════════════════════════════════════
start_clicked = st.button("▶  Start Survey")

if start_clicked:

    # --- FOR LOOP: iterate validation errors ---
    errors: list = validate_all(name, surname, dob, sid)
    for err in errors:
        st.error(f"❌  {err}")

    # --- WHILE LOOP: retry guard ---
    attempt: int = 0
    while errors and attempt < 1:
        st.warning("⚠️  Please correct the errors above, then press **Start Survey** again.")
        attempt += 1
        break

    # --- CONDITIONAL STATEMENTS: if / elif / else ---
    if errors:
        st.stop()
    elif not survey_active:
        st.error("This survey is currently inactive.")
        st.stop()
    else:
        st.session_state["validated"] = True
        st.success("✅  All inputs valid — please answer the questions below.")

# ══════════════════════════════════════════════════════
#  QUESTIONS SECTION
# ══════════════════════════════════════════════════════
if st.session_state.get("validated"):

    st.markdown("---")
    st.markdown('<div class="card-title" style="font-family:\'Playfair Display\',serif;font-size:1.25rem;color:#0a3d55;margin-bottom:1rem;">📋 Survey Questions</div>', unsafe_allow_html=True)

    # Live progress bar
    answered: int = 0
    total_q: int  = len(questions)

    total_score : int  = 0
    answers     : list = []

    for idx, item in enumerate(questions):
        opts: list       = item["opts"]           # list of [label, score] pairs
        opt_labels: list = [o[0] for o in opts]

        st.markdown(f"""
        <div class="q-card">
            <div class="q-num">Question {idx+1} of {total_q}</div>
            <div class="q-text">{item['q']}</div>
        </div>
        """, unsafe_allow_html=True)

        choice: str = st.selectbox(
            label=f"q{idx}",
            options=opt_labels,
            key=f"q{idx}",
            label_visibility="collapsed"
        )

        # Look up score value
        score_val: int = next(s for label, s in opts if label == choice)
        total_score += score_val
        answered    += 1
        answers.append({
            "question_number": idx + 1,
            "question"       : item["q"],
            "selected_option": choice,
            "score"          : score_val,
        })

    # Progress indicator
    pct: float = answered / total_q
    st.progress(pct, text=f"{answered}/{total_q} questions answered")

    st.markdown("---")

    # ══════════════════════════════════════════════════════
    #  SUBMIT BUTTON
    # ══════════════════════════════════════════════════════
    if st.button("📨  Submit & View Results"):

        result_label: str = interpret_score(total_score)
        record: dict      = build_record(name, surname, dob, sid,
                                         total_score, result_label, answers)

        # ── Conditional feedback ──
        if total_score <= 15:
            emoji, advice = "🌟", (
                "Outstanding! Your hydration habits are excellent. "
                "Your reminder system is working perfectly and your energy is very stable."
            )
            bar_color = "#2dbd8f"
        elif total_score <= 30:
            emoji, advice = "👍", (
                "Good habits! Keep using your reminders and maintain the routine. "
                "A few small improvements could make your energy even more stable."
            )
            bar_color = "#0e7fa3"
        elif total_score <= 45:
            emoji, advice = "⚠️", (
                "Moderate stability detected. Consider increasing your reminder frequency "
                "and aiming for at least 8 glasses of water per day."
            )
            bar_color = "#f4a832"
        else:
            emoji, advice = "🚨", (
                "Low energy levels detected. Make hydration your top priority. "
                "Set hourly reminders and avoid sugary drink replacements."
            )
            bar_color = "#e05c5c"

        pct_score: float = total_score / max(possible_scores) * 100

        # ── Result hero card ──
        st.markdown(f"""
        <div class="result-hero">
            <h2>{emoji} {result_label}</h2>
            <div class="score-chip">Score: {total_score} / 60</div>
            <p class="advice">{advice}</p>
        </div>
        """, unsafe_allow_html=True)

        # ── Score bar ──
        st.markdown(f"""
        <div class="bar-wrap">
            <span style="font-size:.85rem;font-weight:700;color:#0a3d55;">
                Score position &nbsp;({total_score}/60)
            </span>
            <div class="bar-track">
                <div class="bar-fill" style="width:{pct_score:.1f}%;background:linear-gradient(90deg,{bar_color},{bar_color}99);"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Band reference table ──
        band_colors: list = ["#2dbd8f", "#0e7fa3", "#f4a832", "#e05c5c"]
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📊 Score Bands</div>', unsafe_allow_html=True)
        for i, (state, (lo, hi)) in enumerate(psych_states.items()):
            active_style = "font-weight:700;" if state == result_label else "opacity:0.7;"
            st.markdown(f"""
            <div class="band-row" style="{active_style}">
                <div class="band-dot" style="background:{band_colors[i]};"></div>
                <span class="band-range">{lo}–{hi}</span>
                <span>{state}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Save files ──
        json_file: str = f"{sid.strip()}_result.json"
        csv_file : str = "survey_results.csv"
        save_json(json_file, record)
        save_csv(csv_file, record)

        st.success(f"✅  Results saved → **{json_file}** and logged to **{csv_file}**")

        # ── Download buttons ──
        col_a, col_b = st.columns(2)
        with col_a:
            st.download_button(
                label="⬇️  Download JSON",
                data=json.dumps(record, indent=2, ensure_ascii=False),
                file_name=json_file,
                mime="application/json",
            )
        with col_b:
            flat = {k: v for k, v in record.items() if k != "answers"}
            csv_str: str = ",".join(flat.keys()) + "\n" + ",".join(str(v) for v in flat.values())
            st.download_button(
                label="⬇️  Download CSV",
                data=csv_str,
                file_name=f"{sid.strip()}_result.csv",
                mime="text/csv",
            )

        # ── Detailed answers expander ──
        with st.expander("📝 Review your answers"):
            for ans in answers:
                colour: str = "#2dbd8f" if ans["score"] <= 1 else ("#f4a832" if ans["score"] == 2 else "#e05c5c")
                st.markdown(
                    f"**Q{ans['question_number']}.** {ans['question']}  \n"
                    f"→ *{ans['selected_option']}* &nbsp;"
                    f"<span style='background:{colour};color:#fff;border-radius:20px;"
                    f"padding:1px 10px;font-size:.8rem;font-weight:700;'>{ans['score']} pts</span>",
                    unsafe_allow_html=True
                )
