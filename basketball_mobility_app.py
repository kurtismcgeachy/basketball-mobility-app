# basketball_mobility_app.py
# Streamlit app to generate daily basketball mobility routines with embedded videos.
# Includes Bigs/Guards one-click presets.
# Author: Built for Kurtis McGeachy

import streamlit as st
import pandas as pd
import random
import datetime as dt

# ------------- Exercise Library -------------
EXERCISES = [
    # ======= Warm-up (dynamic) =======
    {
        "name": "Monkey Walks",
        "category": "Warm-up",
        "focus": ["Hips", "Ankles", "Posterior Chain"],
        "roles": ["Guards", "Wings", "Bigs"],
        "duration": 45,
        "video_url": "https://www.youtube.com/watch?v=mK2XsIEtiko&t=49s",
        "source": "Nathanael Morton – 7‑Minute Mobility"
    },
    {
        "name": "Squat Walks",
        "category": "Warm-up",
        "focus": ["Hips", "Ankles"],
        "roles": ["Guards", "Wings", "Bigs"],
        "duration": 45,
        "video_url": "https://www.youtube.com/watch?v=mK2XsIEtiko&t=77s",
        "source": "Nathanael Morton"
    },
    {
        "name": "Front–Back Leg Kicks",
        "category": "Warm-up",
        "focus": ["Hips", "Hamstrings"],
        "roles": ["Guards", "Wings", "Bigs"],
        "duration": 40,
        "video_url": "https://www.youtube.com/watch?v=mK2XsIEtiko&t=345s",
        "source": "Nathanael Morton"
    },
    {
        "name": "Side‑to‑Side Leg Kicks",
        "category": "Warm-up",
        "focus": ["Hips"],
        "roles": ["Guards", "Wings", "Bigs"],
        "duration": 40,
        "video_url": "https://www.youtube.com/watch?v=mK2XsIEtiko&t=382s",
        "source": "Nathanael Morton"
    },

    # ======= Mobility (main block) =======
    {
        "name": "Archer Squats (Cossack pattern)",
        "category": "Mobility",
        "focus": ["Hips", "Adductors", "Ankles"],
        "roles": ["Wings", "Bigs"],
        "duration": 60,
        "video_url": "https://www.youtube.com/watch?v=mK2XsIEtiko&t=113s",
        "source": "Nathanael Morton"
    },
    {
        "name": "Lunge + Reach (Thoracic Rotation)",
        "category": "Mobility",
        "focus": ["Hips", "T‑Spine/Rotation"],
        "roles": ["Guards", "Wings", "Bigs"],
        "duration": 60,
        "video_url": "https://www.youtube.com/watch?v=mK2XsIEtiko&t=147s",
        "source": "Nathanael Morton"
    },
    {
        "name": "Ostrich Walks",
        "category": "Mobility",
        "focus": ["Hamstrings", "Posterior Chain"],
        "roles": ["Guards", "Wings", "Bigs"],
        "duration": 45,
        "video_url": "https://www.youtube.com/watch?v=mK2XsIEtiko&t=223s",
        "source": "Nathanael Morton"
    },
    {
        "name": "Caterpillars (Inchworm: Cobra → Down Dog)",
        "category": "Mobility",
        "focus": ["Hamstrings", "Posterior Chain", "Shoulders"],
        "roles": ["Guards", "Wings", "Bigs"],
        "duration": 45,
        "video_url": "https://www.youtube.com/watch?v=mK2XsIEtiko&t=272s",
        "source": "Nathanael Morton"
    },
    {
        "name": "6‑Minute Daily Drill (Full‑body Mobility)",
        "category": "Mobility",
        "focus": ["Hips", "Ankles", "T‑Spine/Rotation"],
        "roles": ["Guards", "Wings", "Bigs"],
        "duration": 360,
        "video_url": "https://www.youtube.com/watch?v=uBOEH01bBkM",
        "source": "Good Drill"
    },
    {
        "name": "5‑Minute Hooper Flow (Beginner)",
        "category": "Mobility",
        "focus": ["Hips", "Ankles", "Hamstrings", "T‑Spine/Rotation"],
        "roles": ["Guards", "Wings", "Bigs"],
        "duration": 300,
        "video_url": "https://www.youtube.com/watch?v=A66HdK3CZDA",
        "source": "Quick Beginner Routine"
    },

    # ======= Activation (pre‑practice neuromuscular priming) =======
    {
        "name": "Deep Squat Pry + Ankle Rock",
        "category": "Activation",
        "focus": ["Hips", "Ankles"],
        "roles": ["Wings", "Bigs"],
        "duration": 40,
        "video_url": "https://www.youtube.com/watch?v=mK2XsIEtiko&t=77s",
        "source": "Mapped from Squat Walk pattern"
    },
    {
        "name": "Split‑Stance Lunge Reach (fast reps)",
        "category": "Activation",
        "focus": ["Hips", "T‑Spine/Rotation"],
        "roles": ["Guards", "Wings"],
        "duration": 40,
        "video_url": "https://www.youtube.com/watch?v=mK2XsIEtiko&t=147s",
        "source": "Nathanael Morton"
    },

    # ======= Cool‑down (static / post‑practice) =======
    {
        "name": "Hamstring Static Stretch (30–40s/side)",
        "category": "Cool-down",
        "focus": ["Hamstrings", "Posterior Chain"],
        "roles": ["Guards", "Wings", "Bigs"],
        "duration": 80,
        "video_url": "https://www.youtube.com/watch?v=mK2XsIEtiko&t=223s",
        "source": "Post‑session static"
    },
    {
        "name": "Hip Flexor Static Stretch (Kneeling)",
        "category": "Cool-down",
        "focus": ["Hips"],
        "roles": ["Guards", "Wings", "Bigs"],
        "duration": 80,
        "video_url": "https://www.youtube.com/watch?v=mK2XsIEtiko&t=147s",
        "source": "Post‑session static"
    },
]

CATEGORIES = ["Warm-up", "Mobility", "Activation", "Cool-down"]
FOCI = sorted({f for ex in EXERCISES for f in ex["focus"]})
ROLES = ["Guards", "Wings", "Bigs"]

# ------------- Page Setup -------------
st.set_page_config(page_title="Basketball Mobility Builder", page_icon="🏀", layout="wide")
st.title("🏀 Daily Basketball Mobility Builder")

# Seed by date so the plan changes daily by default
with st.sidebar:
    st.header("Controls")
    today = st.date_input("Routine Date", value=dt.date.today())
    seed = int(today.strftime("%Y%m%d"))
    if "seed" not in st.session_state:
        st.session_state.seed = seed

    # Preserve state for filters and counts
    def _ensure_state(key, default):
        if key not in st.session_state:
            st.session_state[key] = default

    _ensure_state("focus_filter", [])
    _ensure_state("role_filter", [])
    _ensure_state("cnt_wu", 2)
    _ensure_state("cnt_mob", 3)
    _ensure_state("cnt_act", 1)
    _ensure_state("cnt_cd", 2)

    # --- Presets ---
    st.subheader("Presets")
    colp1, colp2, colp3 = st.columns(3)
    with colp1:
        if st.button("Bigs"):
            st.session_state.role_filter = ["Bigs"]
            st.session_state.focus_filter = ["Hips", "Ankles", "Adductors"]
            st.session_state.cnt_wu, st.session_state.cnt_mob = 2, 3
            st.session_state.cnt_act, st.session_state.cnt_cd = 1, 2
    with colp2:
        if st.button("Guards"):
            st.session_state.role_filter = ["Guards"]
            st.session_state.focus_filter = ["Hips", "Ankles", "T‑Spine/Rotation"]
            st.session_state.cnt_wu, st.session_state.cnt_mob = 2, 3
            st.session_state.cnt_act, st.session_state.cnt_cd = 1, 2
    with colp3:
        if st.button("Reset"):
            st.session_state.role_filter = []
            st.session_state.focus_filter = []
            st.session_state.cnt_wu, st.session_state.cnt_mob = 2, 3
            st.session_state.cnt_act, st.session_state.cnt_cd = 1, 2

    # --- Randomization ---
    if st.button("🔀 Shuffle (ignore date)"):
        st.session_state.seed = random.randint(1, 10**9)

    random.seed(st.session_state.seed)

    # --- Filters ---
    st.subheader("Filters (optional)")
    st.session_state.focus_filter = st.multiselect(
        "Focus areas", options=FOCI, default=st.session_state.focus_filter
    )
    st.session_state.role_filter = st.multiselect(
        "Position focus", options=ROLES, default=st.session_state.role_filter
    )

    # --- Block counts ---
    st.subheader("Block configuration")
    st.session_state.cnt_wu = st.number_input("Warm‑up items", 0, 6, st.session_state.cnt_wu)
    st.session_state.cnt_mob = st.number_input("Mobility items", 0, 10, st.session_state.cnt_mob)
    st.session_state.cnt_act = st.number_input("Activation items", 0, 6, st.session_state.cnt_act)
    st.session_state.cnt_cd = st.number_input("Cool‑down items", 0, 6, st.session_state.cnt_cd)

# ------------- Helper functions -------------
def _filter_exercises(category):
    pool = [e for e in EXERCISES if e["category"] == category]
    f_focus = st.session_state.focus_filter
    f_roles = st.session_state.role_filter
    if f_focus:
        pool = [e for e in pool if any(f in e["focus"] for f in f_focus)]
    if f_roles:
        pool = [e for e in pool if any(r in e["roles"] for r in f_roles)]
    return pool

def _pick(pool, k):
    if k <= 0 or not pool:
        return []
    if k >= len(pool):
        return random.sample(pool, len(pool))
    return random.sample(pool, k)

def _render_block(title, items):
    st.markdown(f"### {title}")
    total = 0
    for i, ex in enumerate(items, 1):
        with st.expander(f"{i}. {ex['name']}  •  {ex['duration']}s  •  Focus: {', '.join(ex['focus'])}"):
            st.write(f"Source: {ex['source']}")
            st.video(ex["video_url"])
        total += ex["duration"]
    st.markdown(f"**Block time:** ~{int(total/60)}:{total%60:02d} min")

# ------------- Build & render routine -------------
wu = _pick(_filter_exercises("Warm-up"), st.session_state.cnt_wu)
mob = _pick(_filter_exercises("Mobility"), st.session_state.cnt_mob)
act = _pick(_filter_exercises("Activation"), st.session_state.cnt_act)
cd = _pick(_filter_exercises("Cool-down"), st.session_state.cnt_cd)

st.success(f"Routine for {today.strftime('%b %d, %Y')}")
_render_block("Warm‑up (dynamic)", wu)
_render_block("Mobility Circuit", mob)
_render_block("Activation (court‑ready)", act)
_render_block("Cool‑down (post‑session static)", cd)

# ------------- Export -------------
def _export(rows):
    if not rows:
        st.info("Build a routine to enable exports.")
        return
    df = pd.DataFrame(rows)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download CSV", data=csv, file_name="mobility_routine.csv", mime="text/csv")

    lines = ["# Basketball Mobility Routine", ""]
    for r in rows:
        lines += [
            f"### {r['category']}: {r['name']}",
            f"- Duration: {r['duration']}s",
            f"- Focus: {', '.join(r['focus'])}",
            f"- Video: {r['video_url']}",
            ""
        ]
    md = "\n".join(lines).encode("utf-8")
    st.download_button("⬇️ Download Markdown", data=md, file_name="mobility_routine.md", mime="text/markdown")

st.divider()
st.subheader("Export / Share")
_export(wu + mob + act + cd)

st.caption("Tip: Use dynamic work before practice; reserve static stretches for after to protect power and build range over time.")
