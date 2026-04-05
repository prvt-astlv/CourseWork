"""
Water Intake Reminder Use and Daily Energy Stability Questionnaire
Survey ID : 68
Version   : 1.2  —  Light / Dark mode added
"""

import streamlit as st
import json
import csv
import os
from datetime import datetime

# ══════════════════════════════════════════════════════
#  VARIABLE TYPES  (all 10 required types declared here)
# ══════════════════════════════════════════════════════
version_float : float     = 1.2
survey_id     : int       = 68
survey_title  : str       = (
    "Water Intake Reminder Use and Daily Energy Stability Questionnaire"
)
score_bands   : list      = [0, 15, 30, 45, 60]
band_labels   : tuple     = (
    "Excellent reminder use — stable energy",
    "Good habits — continue",
    "Moderate stability — increase reminders",
    "Low energy — prioritise hydration",
)
possible_scores : range   = range(0, 61)
survey_active   : bool    = True
psych_states    : dict    = {
    "Excellent reminder use — stable energy" : (0,  15),
    "Good habits — continue"                 : (16, 30),
    "Moderate stability — increase reminders": (31, 45),
    "Low energy — prioritise hydration"      : (46, 60),
}
unique_topics   : set       = {"hydration", "energy", "reminder", "wellness"}
frozen_cats     : frozenset = frozenset({"daily", "weekly", "never"})

# ══════════════════════════════════════════════════════
#  LOAD QUESTIONS FROM EXTERNAL FILE
# ══════════════════════════════════════════════════════
QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), "questions.json")

def load_questions() -> list:
    """Load questions from questions.json; return embedded fallback if absent."""
    embedded: list = [
        {"q": "How often do you remind yourself to drink water?",
         "opts": [["Daily", 0], ["Often", 1], ["Sometimes", 2], ["Rarely", 3], ["Never", 4]]},
        {"q": "How stable is your energy when you are well hydrated?",
         "opts": [["Very stable", 0], ["Stable",1], ["Neutral", 2], ["Somewhat unstable", 3], ["Unstable", 4]]},
        {"q": "How many glasses of water do you typically drink per day?",
         "opts": [["8 or more", 0], ["6-7", 1], ["4-5", 2], ["2-3", 3], ["0-1", 4]]},
        {"q": "How often do you feel tired in the afternoon?",
         "opts": [["Never", 0], ["Rarely", 1], ["Sometimes", 2], ["Often", 3], ["Always", 4]]},
        {"q": "How frequently do you feel thirsty throughout the day?",
         "opts": [["Never (well hydrated)", 0], ["Rarely", 1], ["Sometimes", 3], ["Often", 1], ["Always", 4]]},
        {"q": "How would you rate your focus and concentration during the day?",
         "opts": [["Excellent", 0], ["Good", 1], ["Fair", 2], ["Poor", 3], ["Very poor", 4]]},
        {"q": "How often do you replace water with sugary drinks (sodas, juices)?",
         "opts": [["Never", 0], ["Rarely", 1], ["Sometimes", 2], ["Often", 3], ["Always", 4]]},
        {"q": "How often do you feel tired or slow in the morning?",
         "opts": [["Never", 0], ["Rarely", 1], ["Sometimes", 2], ["Often", 3], ["Always", 4]]},
        {"q": "How consistent is your hydration routine throughout the week?",
         "opts": [["Very consistent", 0], ["Mostly consistent", 1], ["Somewhat consistent", 3], ["Inconsistent", 1], ["No routine", 4]]},
        {"q": "How satisfied are you with your current energy levels throughout the day?",
         "opts": [["Very satisfied", 0], ["Satisfied", 1], ["Neutral", 2], ["Dissatisfied", 3], ["Very dissatisfied", 4]]},
        {"q": "How often do you track your water intake (app, journal, etc.)?",
         "opts": [["Daily", 0], ["Several times a week", 1], ["Weekly", 2], ["Rarely",3], ["Never", 4]]},
        {"q": "How often do you drink water before physical activity?",
         "opts": [["Always", 0], ["Often", 1], ["Sometimes", 2], ["Rarely", 3], ["Never", 4]]},
        {"q": "How often do you wake up feeling fresh and full of energy?",
         "opts": [["Always", 0], ["Often", 1], ["Sometimes", 2], ["Rarely", 3], ["Never", 4]]},
        {"q": "How often do you get headaches that might be from not drinking enough water?",
         "opts": [["Never", 0], ["Rarely", 1], ["Sometimes", 2], ["Often", 3], ["Daily", 4]]},
        {"q": "How confident are you that drinking enough water helps you do your daily tasks well?",
         "opts": [["Very confident", 0], ["Confident", 1], ["Neutral", 2], ["Not very confident", 3], ["Not confident at all", 4]]},
    ]
    if os.path.isfile(QUESTIONS_FILE):
        try:
            with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return embedded

questions: list = load_questions()

# ══════════════════════════════════════════════════════
#  USER-DEFINED FUNCTIONS
# ══════════════════════════════════════════════════════
def validate_name(name: str) -> bool:
    name = name.strip()
    if not name:
        return False
    for ch in name:
        if ch.isdigit():
            return False
    return True

def validate_dob(dob: str) -> bool:
    try:
        datetime.strptime(dob.strip(), "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_sid(sid: str) -> bool:
    s = sid.strip()
    return len(s) > 0 and s.isdigit()

def validate_all(name: str, surname: str, dob: str, sid: str) -> list:
    errors: list = []
    if not validate_name(name):
        errors.append("Invalid given name - no digits, cannot be empty.")
    if not validate_name(surname):
        errors.append("Invalid surname - no digits, cannot be empty.")
    if not validate_dob(dob):
        errors.append("Invalid date of birth - use YYYY-MM-DD format.")
    if not validate_sid(sid):
        errors.append("Invalid student ID - digits only.")
    return errors

def interpret_score(score: int) -> str:
    for state, (lo, hi) in psych_states.items():
        if lo <= score <= hi:
            return state
    return "Score out of expected range"

def build_record(name, surname, dob, sid, total_score, result, answers) -> dict:
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
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def save_csv(filename: str, data: dict) -> None:
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
#  DARK / LIGHT MODE STATE
# ══════════════════════════════════════════════════════
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = True   # default: dark

# Toggle button — top right
t_col1, t_col2 = st.columns([9, 1])
with t_col2:
    toggle_icon = "☀️" if st.session_state["dark_mode"] else "🌙"
    if st.button(toggle_icon, key="theme_toggle", help="Toggle light / dark mode"):
        st.session_state["dark_mode"] = not st.session_state["dark_mode"]
        st.rerun()

is_dark: bool = st.session_state["dark_mode"]

# ══════════════════════════════════════════════════════
#  THEME TOKENS
# ══════════════════════════════════════════════════════
if is_dark:
    T = {
        "page_bg"      : "#0c1e2e",
        "card_bg"      : "#112233",
        "card_bg2"     : "#162840",
        "border"       : "#1e3a50",
        "input_bg"     : "#0f2030",
        "text"         : "#e8f4fa",
        "muted"        : "#7aabbd",
        "teal"         : "#0fa3cc",
        "sky"          : "#62d4f0",
        "ocean"        : "#0a3d55",
        "accent"       : "#f4a832",
        "danger"       : "#e05c5c",
        "success"      : "#2dbd8f",
        "hero_grad"    : "linear-gradient(135deg,#0a3d55 0%,#0e7fa3 60%,#62c4e0 100%)",
        "btn_grad"     : "linear-gradient(90deg,#0a3d55,#0fa3cc)",
        "result_grad"  : "linear-gradient(135deg,#0a3d55,#0e7fa3)",
        "progress_grad": "linear-gradient(90deg,#0fa3cc,#62d4f0)",
        "hero_text"    : "#ffffff",
        "hero_sub"     : "#a8d8ea",
        "badge_bg"     : "rgba(255,255,255,0.14)",
        "badge_border" : "rgba(255,255,255,0.28)",
        "dl_bg"        : "#162840",
        "dl_border"    : "#1e3a50",
        "dl_fg"        : "#62d4f0",
        "active_row_bg": "#162840",
        "scrollbar"    : "#1e3a50",
        "mode_label"   : "Dark mode",
        "mode_icon"    : "🌑",
    }
else:
    T = {
        "page_bg"      : "#eef7fb",
        "card_bg"      : "#ffffff",
        "card_bg2"     : "#ddf0f8",
        "border"       : "#b6d8e8",
        "input_bg"     : "#f5fbfd",
        "text"         : "#0c2130",
        "muted"        : "#3a7a96",
        "teal"         : "#0880a3",
        "sky"          : "#1aadcc",
        "ocean"        : "#063348",
        "accent"       : "#c47a0a",
        "danger"       : "#b83228",
        "success"      : "#17996a",
        "hero_grad"    : "linear-gradient(135deg,#063348 0%,#0880a3 55%,#35b2d0 100%)",
        "btn_grad"     : "linear-gradient(90deg,#063348,#0880a3)",
        "result_grad"  : "linear-gradient(135deg,#063348,#0880a3)",
        "progress_grad": "linear-gradient(90deg,#0880a3,#35b2d0)",
        "hero_text"    : "#ffffff",
        "hero_sub"     : "#cdeaf5",
        "badge_bg"     : "rgba(255,255,255,0.25)",
        "badge_border" : "rgba(255,255,255,0.55)",
        "dl_bg"        : "#ddf0f8",
        "dl_border"    : "#b6d8e8",
        "dl_fg"        : "#063348",
        "active_row_bg": "#ddf0f8",
        "scrollbar"    : "#b6d8e8",
        "mode_label"   : "Light mode",
        "mode_icon"    : "☀️",
    }

# ══════════════════════════════════════════════════════
#  INJECT CSS — all colours driven by T dict
# ══════════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Lato:wght@300;400;700&display=swap');

/* ─── Base ─── */
html, body, [class*="css"], .stApp {{
    font-family: 'Lato', sans-serif !important;
    background-color: {T["page_bg"]} !important;
    color: {T["text"]} !important;
    transition: background-color .35s, color .25s;
}}
#MainMenu, footer, header {{ visibility: hidden; }}

/* ─── Theme toggle pill ─── */
div[data-testid="stButton"]:has(button[title="Toggle light / dark mode"]) button {{
    background: {T["card_bg"]} !important;
    border: 1.5px solid {T["border"]} !important;
    color: {T["teal"]} !important;
    border-radius: 50px !important;
    font-size: 1.3rem !important;
    padding: 0.2rem 0.55rem !important;
    width: auto !important;
    min-width: unset !important;
    box-shadow: 0 2px 10px rgba(0,0,0,.15) !important;
    transition: all .2s !important;
}}
div[data-testid="stButton"]:has(button[title="Toggle light / dark mode"]) button:hover {{
    background: {T["teal"]} !important;
    color: #fff !important;
    transform: scale(1.1) !important;
}}

/* ─── Hero ─── */
.hero {{
    background: {T["hero_grad"]};
    border-radius: 20px;
    padding: 2.8rem 2.4rem 2.1rem;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0,0,0,.18);
}}
.hero::before {{
    content: "💧";
    position: absolute;
    font-size: 10rem;
    right: -1rem; top: -0.8rem;
    opacity: .08; line-height: 1;
}}
.hero h1 {{
    font-family: 'Playfair Display', serif;
    color: {T["hero_text"]};
    font-size: 2.05rem;
    margin: 0 0 .45rem;
    line-height: 1.2;
}}
.hero p {{
    color: {T["hero_sub"]};
    font-size: .97rem;
    font-weight: 300;
    margin: 0;
    max-width: 520px;
}}
.badge {{
    display: inline-block;
    background: {T["badge_bg"]};
    border: 1px solid {T["badge_border"]};
    color: #fff;
    border-radius: 30px;
    padding: 3px 14px;
    font-size: .78rem;
    font-weight: 700;
    letter-spacing: .06em;
    margin-bottom: .85rem;
    text-transform: uppercase;
}}
.theme-pill {{
    float: right;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(255,255,255,.16);
    border: 1px solid rgba(255,255,255,.30);
    border-radius: 30px;
    padding: 3px 12px 3px 9px;
    font-size: .78rem;
    color: rgba(255,255,255,.85);
    font-weight: 600;
    margin-top: -0.4rem;
}}

/* ─── Cards ─── */
.card {{
    background: {T["card_bg"]};
    border-radius: 14px;
    padding: 1.6rem 1.8rem;
    box-shadow: 0 2px 18px rgba(0,0,0,.07);
    margin-bottom: 1.4rem;
    border: 1px solid {T["border"]};
    transition: background .3s, border-color .3s;
}}
.card-title {{
    font-family: 'Playfair Display', serif;
    font-size: 1.12rem;
    color: {T["teal"]};
    margin-bottom: .9rem;
    display: flex;
    align-items: center;
    gap: .5rem;
}}
.section-heading {{
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem;
    color: {T["ocean"]};
    margin-bottom: 1rem;
    padding-bottom: .4rem;
    border-bottom: 2px solid {T["teal"]};
}}

/* ─── Question cards ─── */
.q-card {{
    background: {T["card_bg"]};
    border-radius: 12px;
    padding: 1.1rem 1.4rem .85rem;
    margin-bottom: .8rem;
    border-left: 4px solid {T["teal"]};
    box-shadow: 0 1px 8px rgba(0,0,0,.07);
    transition: border-color .2s, background .3s;
}}
.q-card:hover {{ border-left-color: {T["accent"]}; }}
.q-num {{
    font-size: .72rem;
    font-weight: 700;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: {T["teal"]};
    margin-bottom: .2rem;
}}
.q-text {{
    font-size: 1rem;
    color: {T["text"]};
    margin-bottom: .45rem;
    line-height: 1.45;
}}

/* ─── Result hero ─── */
.result-hero {{
    background: {T["result_grad"]};
    border-radius: 16px;
    padding: 2rem 2.2rem;
    color: #fff;
    margin: 1.2rem 0;
    position: relative;
    overflow: hidden;
    box-shadow: 0 6px 28px rgba(0,0,0,.20);
}}
.result-hero::after {{
    content: "✦";
    position: absolute;
    right: 1.5rem; top: .8rem;
    font-size: 4.5rem;
    opacity: .09;
}}
.result-hero h2 {{
    font-family: 'Playfair Display', serif;
    font-size: 1.65rem;
    margin: 0 0 .5rem;
    color: #fff;
}}
.result-hero .score-chip {{
    background: rgba(255,255,255,.20);
    border-radius: 30px;
    padding: 4px 18px;
    font-size: 1rem;
    font-weight: 700;
    display: inline-block;
    margin-bottom: .7rem;
}}
.result-hero .advice {{
    font-size: .96rem;
    font-weight: 300;
    color: rgba(255,255,255,.88);
    line-height: 1.65;
    max-width: 490px;
}}

/* ─── Score bar ─── */
.bar-wrap {{ margin: .5rem 0 1.2rem; }}
.bar-label {{
    font-size: .84rem;
    font-weight: 700;
    color: {T["muted"]};
    margin-bottom: .3rem;
}}
.bar-track {{
    height: 13px;
    background: {T["card_bg2"]};
    border-radius: 20px;
    overflow: hidden;
    border: 1px solid {T["border"]};
}}
.bar-fill {{ height: 100%; border-radius: 20px; transition: width 1.2s ease; }}

/* ─── Band rows ─── */
.band-row {{
    display: flex;
    align-items: center;
    gap: .8rem;
    padding: .52rem .6rem;
    border-bottom: 1px solid {T["border"]};
    border-radius: 6px;
    font-size: .91rem;
    transition: background .15s;
}}
.band-row:hover {{ background: {T["card_bg2"]}; }}
.band-dot {{ width: 11px; height: 11px; border-radius: 50%; flex-shrink: 0; }}
.band-range {{ font-weight: 700; color: {T["teal"]}; min-width: 52px; font-size: .87rem; }}
.band-label {{ color: {T["text"]}; }}
.my-result-tag {{
    margin-left: auto;
    font-size: .75rem;
    font-weight: 700;
    border-radius: 20px;
    padding: 2px 10px;
    white-space: nowrap;
}}

/* ─── Inputs ─── */
div[data-testid="stTextInput"] label,
div[data-testid="stSelectbox"] label {{
    font-size: .84rem !important;
    font-weight: 700 !important;
    color: {T["muted"]} !important;
    text-transform: uppercase !important;
    letter-spacing: .05em !important;
}}
div[data-testid="stTextInput"] input {{
    background: {T["input_bg"]} !important;
    color: {T["text"]} !important;
    border: 1.5px solid {T["border"]} !important;
    border-radius: 8px !important;
    padding: .55rem .9rem !important;
    transition: border-color .2s, box-shadow .2s !important;
}}
div[data-testid="stTextInput"] input:focus {{
    border-color: {T["teal"]} !important;
    box-shadow: 0 0 0 3px rgba(15,163,204,.18) !important;
}}
div[data-testid="stSelectbox"] > div > div {{
    background: {T["input_bg"]} !important;
    color: {T["text"]} !important;
    border: 1.5px solid {T["border"]} !important;
    border-radius: 8px !important;
}}

/* ─── Main buttons ─── */
div.stButton > button {{
    background: {T["btn_grad"]} !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: .65rem 2rem !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: .03em !important;
    width: 100% !important;
    transition: opacity .2s, transform .15s !important;
    box-shadow: 0 3px 12px rgba(0,0,0,.18) !important;
}}
div.stButton > button:hover {{
    opacity: .87 !important;
    transform: translateY(-1px) !important;
}}

/* ─── Download buttons ─── */
div.stDownloadButton > button {{
    background: {T["dl_bg"]} !important;
    color: {T["dl_fg"]} !important;
    border: 1.5px solid {T["dl_border"]} !important;
    border-radius: 9px !important;
    font-weight: 700 !important;
    padding: .5rem 1.2rem !important;
    width: 100% !important;
    transition: background .2s, color .2s !important;
}}
div.stDownloadButton > button:hover {{
    background: {T["teal"]} !important;
    color: #fff !important;
    border-color: {T["teal"]} !important;
}}

/* ─── Alerts ─── */
div[data-testid="stAlert"] {{
    border-radius: 10px !important;
    background: {T["card_bg"]} !important;
    border-color: {T["border"]} !important;
}}

/* ─── Progress ─── */
div[data-testid="stProgress"] > div {{
    background: {T["progress_grad"]} !important;
    border-radius: 20px !important;
}}
div[data-testid="stProgress"] {{
    background: {T["card_bg2"]} !important;
    border-radius: 20px !important;
}}

/* ─── Expander ─── */
details {{
    background: {T["card_bg"]} !important;
    border: 1px solid {T["border"]} !important;
    border-radius: 10px !important;
}}
summary {{ color: {T["teal"]} !important; font-weight: 700 !important; }}

/* ─── HR ─── */
hr {{ border-color: {T["border"]} !important; }}

/* ─── Scrollbar ─── */
::-webkit-scrollbar {{ width: 6px; }}
::-webkit-scrollbar-track {{ background: {T["page_bg"]}; }}
::-webkit-scrollbar-thumb {{ background: {T["scrollbar"]}; border-radius: 10px; }}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  HERO BANNER
# ══════════════════════════════════════════════════════
st.markdown(f"""
<div class="hero">
    <div class="badge">Survey #{survey_id} &nbsp;·&nbsp; v{version_float}</div>
    <span class="theme-pill">{T["mode_icon"]} {T["mode_label"]}</span>
    <h1>💧 Hydration &amp; Energy<br>Stability Survey</h1>
    <p>This questionnaire assesses your water-intake reminder habits and
       how hydration affects your daily energy. Answer all 15 questions
       honestly — it takes about 3 minutes.</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  PERSONAL INFORMATION
# ══════════════════════════════════════════════════════
st.markdown(f'<div class="card"><div class="card-title">👤 Personal Information</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    name    = st.text_input("Given Name",    placeholder="e.g. Amir")
    dob     = st.text_input("Date of Birth", placeholder="YYYY-MM-DD")
with col2:
    surname = st.text_input("Surname",       placeholder="e.g. Karimov")
    sid     = st.text_input("Student ID",    placeholder="digits only")

st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  START SURVEY
# ══════════════════════════════════════════════════════
if st.button("▶  Start Survey", key="start_btn"):

    errors: list = validate_all(name, surname, dob, sid)
    for err in errors:
        st.error(f"❌  {err}")

    attempt: int = 0
    while errors and attempt < 1:
        st.warning("⚠️  Please correct the errors above, then press Start Survey again.")
        attempt += 1
        break

    if errors:
        st.stop()
    elif not survey_active:
        st.error("This survey is currently inactive.")
        st.stop()
    else:
        st.session_state["validated"] = True
        st.success("✅  All inputs valid — please answer the questions below.")

# ══════════════════════════════════════════════════════
#  QUESTIONS
# ══════════════════════════════════════════════════════
if st.session_state.get("validated"):

    st.markdown("---")
    st.markdown('<div class="section-heading">📋 Survey Questions</div>', unsafe_allow_html=True)

    answered   : int  = 0
    total_q    : int  = len(questions)
    total_score: int  = 0
    answers    : list = []

    for idx, item in enumerate(questions):
        opts      : list = item["opts"]
        opt_labels: list = [o[0] for o in opts]

        st.markdown(f"""
        <div class="q-card">
            <div class="q-num">Question {idx+1} of {total_q}</div>
            <div class="q-text">{item['q']}</div>
        </div>
        """, unsafe_allow_html=True)

        choice: str = st.selectbox(
            label=f"q{idx}", options=opt_labels,
            key=f"q{idx}", label_visibility="collapsed"
        )
        score_val: int = next(s for label, s in opts if label == choice)
        total_score   += score_val
        answered      += 1
        answers.append({
            "question_number": idx + 1,
            "question"       : item["q"],
            "selected_option": choice,
            "score"          : score_val,
        })

    pct: float = answered / total_q
    st.progress(pct, text=f"{answered}/{total_q} questions answered")
    st.markdown("---")

    # ══════════════════════════════════════════════════════
    #  SUBMIT
    # ══════════════════════════════════════════════════════
    if st.button("📨  Submit & View Results", key="submit_btn"):

        result_label: str = interpret_score(total_score)
        record: dict      = build_record(name, surname, dob, sid,
                                         total_score, result_label, answers)

        if total_score >= 46:
            emoji, advice, bar_color = "🌟", (
                "Outstanding! Your hydration habits are excellent. "
                "Your reminder system is working perfectly and your energy is very stable."
            ), T["success"]
        elif total_score >= 31:
            emoji, advice, bar_color = "👍", (
                "Good habits! Keep using your reminders and maintain the routine. "
                "A few small improvements could make your energy even more stable."
            ), T["teal"]
        elif total_score >= 16:
            emoji, advice, bar_color = "⚠️", (
                "Moderate stability detected. Consider increasing your reminder frequency "
                "and aiming for at least 8 glasses of water per day."
            ), T["accent"]
        else:
            emoji, advice, bar_color = "🚨", (
                "Low energy levels detected. Make hydration your top priority. "
                "Set hourly reminders and avoid sugary drink replacements."
            ), T["danger"]

        pct_score: float = total_score / max(possible_scores) * 100

        # Result card
        st.markdown(f"""
        <div class="result-hero">
            <h2>{emoji} {result_label}</h2>
            <div class="score-chip">Score: {total_score} / 60</div>
            <p class="advice">{advice}</p>
        </div>
        """, unsafe_allow_html=True)

        # Score bar
        st.markdown(f"""
        <div class="bar-wrap">
            <div class="bar-label">Score position &nbsp;({total_score} / 60)</div>
            <div class="bar-track">
                <div class="bar-fill"
                     style="width:{pct_score:.1f}%;
                            background:linear-gradient(90deg,{bar_color},{bar_color}99);">
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Band table
        band_colors: list = [T["success"], T["teal"], T["accent"], T["danger"]]
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📊 Score Bands</div>', unsafe_allow_html=True)
        for i, (state, (lo, hi)) in enumerate(psych_states.items()):
            is_active  = state == result_label
            row_style  = f"font-weight:700;" if is_active else "opacity:0.5;"
            active_bg  = f"background:{T['active_row_bg']};" if is_active else ""
            active_tag = (
                f'<span class="my-result-tag" '
                f'style="background:{band_colors[i]};color:#fff;">'
                f'Your result</span>'
            ) if is_active else ""
            st.markdown(f"""
            <div class="band-row" style="{row_style}{active_bg}">
                <div class="band-dot"
                     style="background:{band_colors[i]};
                            box-shadow:0 0 6px {band_colors[i]}88;">
                </div>
                <span class="band-range">{lo}–{hi}</span>
                <span class="band-label">{state}</span>
                {active_tag}
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Save
        json_file: str = f"{sid.strip()}_result.json"
        csv_file : str = "survey_results.csv"
        save_json(json_file, record)
        save_csv(csv_file, record)
        st.success(f"✅  Results saved to **{json_file}** and logged in **{csv_file}**")

        # Download buttons
        col_a, col_b = st.columns(2)
        with col_a:
            st.download_button(
                label="⬇️  Download JSON",
                data=json.dumps(record, indent=2, ensure_ascii=False),
                file_name=json_file,
                mime="application/json",
            )
        with col_b:
            flat    = {k: v for k, v in record.items() if k != "answers"}
            csv_str = ",".join(flat.keys()) + "\n" + ",".join(str(v) for v in flat.values())
            st.download_button(
                label="⬇️  Download CSV",
                data=csv_str,
                file_name=f"{sid.strip()}_result.csv",
                mime="text/csv",
            )

        # Detailed answers
        with st.expander("📝 Review your answers"):
            for ans in answers:
                s = ans["score"]
                colour = T["success"] if s >= 3 else (T["accent"] if s == 2 else T["danger"])
                st.markdown(
                    f"**Q{ans['question_number']}.** {ans['question']}  \n"
                    f"→ *{ans['selected_option']}* &nbsp;"
                    f"<span style='background:{colour};color:#fff;border-radius:20px;"
                    f"padding:1px 10px;font-size:.8rem;font-weight:700;'>{s} pts</span>",
                    unsafe_allow_html=True
                )
