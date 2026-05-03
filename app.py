"""
app.py – AI-Powered Past Paper Analyzer & Smart Study Planner
Run: streamlit run app.py
"""

import os
import json
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# ── Project modules ──────────────────────────────────────────────────────────
from utils.extractor import load_all_papers
from utils.analyzer  import load_syllabus, run_analysis
from utils.planner   import generate_study_plan

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PaperLens – AI Study Analyzer",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root palette ── */
:root {
    --bg:        #0d0f14;
    --surface:   #161a24;
    --border:    #232840;
    --accent:    #6c63ff;
    --accent2:   #ff6584;
    --accent3:   #43d9ad;
    --text:      #e8eaf6;
    --muted:     #7c83a0;
    --card-bg:   #1c2030;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}
.main .block-container { padding: 1.5rem 2rem 4rem; max-width: 1300px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── Headings ── */
h1, h2, h3, h4 { font-family: 'Syne', sans-serif !important; }

/* ── Cards ── */
.card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}
.card-accent { border-left: 4px solid var(--accent); }
.card-green  { border-left: 4px solid var(--accent3); }
.card-red    { border-left: 4px solid var(--accent2); }

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #1c2030 0%, #0d1220 100%);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 2.2rem 2.4rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(108,99,255,0.18) 0%, transparent 70%);
    top: -60px; right: -60px;
    border-radius: 50%;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(90deg, #6c63ff, #a78bfa, #43d9ad);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.15;
    margin-bottom: .35rem;
}
.hero-sub { color: var(--muted); font-size: 1rem; }

/* ── Status badges ── */
.badge {
    display: inline-block;
    padding: .25rem .75rem;
    border-radius: 999px;
    font-size: .78rem;
    font-weight: 600;
    margin: .2rem .1rem;
}
.badge-green  { background: rgba(67,217,173,.15); color: #43d9ad; border: 1px solid rgba(67,217,173,.3); }
.badge-purple { background: rgba(108,99,255,.15); color: #a78bfa; border: 1px solid rgba(108,99,255,.3); }
.badge-red    { background: rgba(255,101,132,.15); color: #ff6584; border: 1px solid rgba(255,101,132,.3); }
.badge-yellow { background: rgba(251,191,36,.15);  color: #fbbf24; border: 1px solid rgba(251,191,36,.3); }

/* ── Insight rows ── */
.insight-row {
    display: flex;
    align-items: center;
    gap: .8rem;
    padding: .6rem 0;
    border-bottom: 1px solid var(--border);
}
.insight-row:last-child { border-bottom: none; }
.insight-icon { font-size: 1.3rem; min-width: 2rem; }
.insight-label { font-size: .82rem; color: var(--muted); }
.insight-val   { font-family: 'Syne', sans-serif; font-size: 1rem; font-weight: 700; }

/* ── Plan day cards ── */
.plan-row {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: .8rem 0;
    border-bottom: 1px solid var(--border);
}
.plan-row:last-child { border-bottom: none; }
.plan-day {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.1rem;
    min-width: 60px;
    color: var(--accent);
}
.plan-topics { flex: 1; }
.plan-topic-chip {
    display: inline-block;
    background: rgba(108,99,255,.12);
    border: 1px solid rgba(108,99,255,.25);
    border-radius: 6px;
    padding: .15rem .55rem;
    font-size: .82rem;
    margin: .15rem .1rem;
    color: #c4b5fd;
}
.plan-meta { font-size: .75rem; color: var(--muted); margin-top: .25rem; }

/* ── Streamlit overrides ── */
.stSlider > div > div { color: var(--text) !important; }
.stButton > button {
    background: linear-gradient(135deg, #6c63ff, #a78bfa);
    color: white; border: none; border-radius: 10px;
    padding: .6rem 1.6rem; font-family: 'Syne', sans-serif;
    font-weight: 700; font-size: 1rem;
    transition: opacity .2s;
    width: 100%;
}
.stButton > button:hover { opacity: .85; }
div[data-testid="stMetric"] {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem;
}
div[data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: .8rem; }
div[data-testid="stMetricValue"] { font-family: 'Syne', sans-serif !important; font-size: 1.8rem !important; color: var(--text) !important; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PATHS
# ═══════════════════════════════════════════════════════════════════════════════
BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
DATASET_FOLDER  = os.path.join(BASE_DIR, "papers_dataset")
SYLLABUS_PATH   = os.path.join(BASE_DIR, "syllabus.json")


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 📘 PaperLens")
    st.markdown("<p style='color:#7c83a0;font-size:.85rem;'>AI Past Paper Analyzer</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### ⏳ Exam Details")
    days_left      = st.slider("Days left for exam",  min_value=1, max_value=60, value=14, step=1)
    hours_per_day  = st.slider("Study hours per day", min_value=1, max_value=12, value=4,  step=1)

    st.markdown("---")
    st.markdown("### 📂 Dataset")

    # Count papers
    pdf_count = 0
    if os.path.exists(DATASET_FOLDER):
        pdf_count = len([f for f in os.listdir(DATASET_FOLDER) if f.lower().endswith(".pdf")])

    if pdf_count > 0:
        st.markdown(f'<span class="badge badge-green">✔ {pdf_count} Papers Loaded</span>', unsafe_allow_html=True)
        st.markdown('<span class="badge badge-green">✔ Ready for Analysis</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge badge-red">✗ No Papers Found</span>', unsafe_allow_html=True)
        st.caption(f"Place PDF files in: `papers_dataset/`")

    st.markdown("---")
    run_btn = st.button("🚀 Run Analysis")

    st.markdown("---")
    st.markdown("<p style='color:#7c83a0;font-size:.75rem;'>Built with Streamlit · pdfplumber · plotly</p>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# HERO SECTION
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
    <div class="hero-title">📘 AI Past Paper Analyzer</div>
    <div class="hero-sub">Upload past exam papers → Discover high-impact topics → Get a personalized study plan.</div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
if not run_btn:
    # Landing state
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="card card-accent">
            <div style="font-size:2rem">📄</div>
            <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:1.05rem;margin:.4rem 0">PDF Extraction</div>
            <div style="color:#7c83a0;font-size:.85rem">Automatically reads all past papers and extracts question text for analysis.</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="card card-green">
            <div style="font-size:2rem">🔍</div>
            <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:1.05rem;margin:.4rem 0">Topic Analysis</div>
            <div style="color:#7c83a0;font-size:.85rem">Matches syllabus topics using smart keyword detection and ranks by frequency.</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="card card-red">
            <div style="font-size:2rem">📅</div>
            <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:1.05rem;margin:.4rem 0">Study Planner</div>
            <div style="color:#7c83a0;font-size:.85rem">Generates a personalized day-by-day study plan optimized for your exam timeline.</div>
        </div>""", unsafe_allow_html=True)

    st.info("👈 Configure your exam details in the sidebar, then click **Run Analysis** to get started.", icon="💡")
    st.stop()


# ── Run pipeline ─────────────────────────────────────────────────────────────
with st.spinner("🔍 Extracting text from PDFs..."):
    paper_data = load_all_papers(DATASET_FOLDER)

if "error" in paper_data and paper_data["count"] == 0:
    st.error(f"❌ {paper_data['error']}")
    st.stop()

with st.spinner("🧠 Analyzing topics..."):
    syllabus = load_syllabus(SYLLABUS_PATH)
    if not syllabus:
        st.error("❌ Could not load syllabus.json. Please check the file.")
        st.stop()
    results = run_analysis(paper_data["combined_text"], syllabus)

with st.spinner("📅 Generating study plan..."):
    plan = generate_study_plan(results["ranked"], days_left, hours_per_day)

st.success(f"✅ Analysis complete! Processed **{paper_data['count']} papers** and **{len(results['frequency'])} topics**.")

# ═══════════════════════════════════════════════════════════════════════════════
# METRICS ROW
# ═══════════════════════════════════════════════════════════════════════════════
m1, m2, m3, m4 = st.columns(4)
m1.metric("📄 Papers Analyzed",   paper_data["count"])
m2.metric("📚 Topics Tracked",    len(results["frequency"]))
m3.metric("⏳ Days to Exam",      days_left)
m4.metric("⏱ Daily Study Hours", hours_per_day)

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# CHARTS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("## 📊 Topic Frequency Analysis")
chart_col1, chart_col2 = st.columns([3, 2])

ranked = results["ranked"]
topics_list  = [t for t, _ in ranked]
counts_list  = [c for _, c in ranked]
colors       = ["#6c63ff" if c > 2 else "#43d9ad" if c >= 1 else "#ff6584" for c in counts_list]

# ── Bar Chart ──────────────────────────────────────────────────────────────
with chart_col1:
    fig_bar = go.Figure(go.Bar(
        x=topics_list,
        y=counts_list,
        marker=dict(color=colors, line=dict(width=0)),
        text=counts_list,
        textposition="outside",
        textfont=dict(color="#e8eaf6", size=11),
        hovertemplate="<b>%{x}</b><br>Frequency: %{y}<extra></extra>",
    ))
    fig_bar.update_layout(
        title=dict(text="Topic Frequency (All Papers)", font=dict(size=15, color="#e8eaf6", family="Syne")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#7c83a0", family="DM Sans"),
        xaxis=dict(tickangle=-35, gridcolor="rgba(255,255,255,0.04)", color="#7c83a0"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)", color="#7c83a0"),
        margin=dict(l=0, r=0, t=45, b=10),
        height=380,
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

# ── Pie Chart ──────────────────────────────────────────────────────────────
with chart_col2:
    pie_topics = [t for t, c in ranked if c > 0]
    pie_counts = [c for _, c in ranked if c > 0]
    pie_colors = px.colors.qualitative.Pastel + px.colors.qualitative.Bold

    fig_pie = go.Figure(go.Pie(
        labels=pie_topics,
        values=pie_counts,
        hole=0.52,
        marker=dict(colors=pie_colors[:len(pie_topics)], line=dict(color="#0d0f14", width=2)),
        textinfo="label+percent",
        textfont=dict(size=10, color="#e8eaf6"),
        hovertemplate="<b>%{label}</b><br>%{value} mentions (%{percent})<extra></extra>",
    ))
    fig_pie.update_layout(
        title=dict(text="Topic Distribution", font=dict(size=15, color="#e8eaf6", family="Syne")),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#7c83a0", family="DM Sans"),
        showlegend=False,
        margin=dict(l=0, r=0, t=45, b=10),
        height=380,
        annotations=[dict(
            text=f"<b>{sum(pie_counts)}</b><br>Total",
            x=.5, y=.5, font=dict(size=14, color="#e8eaf6", family="Syne"),
            showarrow=False,
        )]
    )
    st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

# ── Unit-level bar ─────────────────────────────────────────────────────────
st.markdown("#### 📦 Analysis by Unit")
unit_names  = list(results["unit_summary"].keys())
unit_counts = list(results["unit_summary"].values())
unit_colors = ["#6c63ff","#43d9ad","#ff6584","#fbbf24","#f472b6"]

fig_unit = go.Figure(go.Bar(
    y=unit_names,
    x=unit_counts,
    orientation="h",
    marker=dict(color=unit_colors[:len(unit_names)], line=dict(width=0)),
    text=unit_counts,
    textposition="outside",
    textfont=dict(color="#e8eaf6"),
    hovertemplate="<b>%{y}</b>: %{x} mentions<extra></extra>",
))
fig_unit.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#7c83a0", family="DM Sans"),
    xaxis=dict(gridcolor="rgba(255,255,255,0.06)", color="#7c83a0"),
    yaxis=dict(color="#e8eaf6", tickfont=dict(size=11)),
    margin=dict(l=0, r=60, t=10, b=10),
    height=220,
)
st.plotly_chart(fig_unit, use_container_width=True, config={"displayModeBar": False})


# ═══════════════════════════════════════════════════════════════════════════════
# INSIGHTS SECTION
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("## 🔥 Key Insights")
ins1, ins2, ins3 = st.columns(3)

# High priority
with ins1:
    top_html = ""
    for topic, count in results["top_topics"]:
        top_html += f'<div class="insight-row"><span class="insight-icon">🔥</span><div><div class="insight-val">{topic}</div><div class="insight-label">{count} occurrences – High Priority</div></div></div>'
    st.markdown(f'<div class="card card-accent"><h4 style="margin-top:0;font-family:Syne,sans-serif">🔥 High Priority Topics</h4>{top_html}</div>', unsafe_allow_html=True)

# Low priority
with ins2:
    low_html = ""
    for topic, count in results["low_topics"]:
        low_html += f'<div class="insight-row"><span class="insight-icon">⚠️</span><div><div class="insight-val">{topic}</div><div class="insight-label">{count} occurrences – Lower Priority</div></div></div>'
    st.markdown(f'<div class="card card-red"><h4 style="margin-top:0;font-family:Syne,sans-serif">⚠️ Low Priority Topics</h4>{low_html}</div>', unsafe_allow_html=True)

# Predicted
with ins3:
    pred_html = ""
    for topic, count in results["predicted"]:
        reason = "Not asked in past papers" if count == 0 else f"Only {count} occurrence(s)"
        pred_html += f'<div class="insight-row"><span class="insight-icon">🔮</span><div><div class="insight-val">{topic}</div><div class="insight-label">{reason} – Likely to appear</div></div></div>'
    if not pred_html:
        pred_html = '<div class="insight-row"><span class="insight-icon">✅</span><div class="insight-val">All topics well-covered!</div></div>'
    st.markdown(f'<div class="card card-green"><h4 style="margin-top:0;font-family:Syne,sans-serif">🔮 Predicted Topics</h4>{pred_html}</div>', unsafe_allow_html=True)


# ── Full topic table ────────────────────────────────────────────────────────
with st.expander("📋 View Full Topic Frequency Table"):
    import pandas as pd
    df = pd.DataFrame(results["ranked"], columns=["Topic", "Frequency"])
    df["Priority"] = df["Frequency"].apply(
        lambda x: "🔥 High" if x > 2 else ("⚡ Medium" if x >= 1 else "🔮 Predicted")
    )
    st.dataframe(df, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════════════════════
# STUDY PLAN SECTION
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("## 📅 Your Personalized Study Plan")
st.caption(f"Based on **{days_left} days** × **{hours_per_day} hours/day** — optimized by topic importance")

if not plan:
    st.warning("Could not generate a study plan. Please adjust your inputs.")
else:
    plan_html = ""
    for entry in plan:
        if entry.get("is_revision"):
            chips = '<span class="plan-topic-chip" style="background:rgba(67,217,173,.1);border-color:rgba(67,217,173,.3);color:#43d9ad;">📝 Revision & Practice</span>'
        else:
            chips = "".join(f'<span class="plan-topic-chip">{t}</span>' for t in entry["topics"])

        meta = f'{entry["priority_label"]} &nbsp;·&nbsp; {entry["total_hours"]}h total'
        if not entry.get("is_revision"):
            meta += f' &nbsp;·&nbsp; ~{entry["hours_each"]}h per topic'

        plan_html += f"""
        <div class="plan-row">
            <div class="plan-day">Day {entry["day"]}</div>
            <div class="plan-topics">{chips}<div class="plan-meta">{meta}</div></div>
        </div>"""

    st.markdown(f'<div class="card">{plan_html}</div>', unsafe_allow_html=True)

    # Summary timeline chart
    st.markdown("#### 📈 Study Plan Timeline")
    timeline_days   = [e["day"] for e in plan]
    timeline_topics = [", ".join(e["topics"])[:40] for e in plan]
    timeline_hours  = [e.get("total_hours", hours_per_day) for e in plan]
    timeline_colors = ["#43d9ad" if e.get("is_revision") else
                       "#6c63ff" if "High" in e.get("priority_label","") else
                       "#fbbf24" if "Medium" in e.get("priority_label","") else
                       "#ff6584" for e in plan]

    fig_timeline = go.Figure(go.Bar(
        x=[f"Day {d}" for d in timeline_days],
        y=timeline_hours,
        marker=dict(color=timeline_colors, line=dict(width=0)),
        text=timeline_topics,
        textposition="inside",
        textfont=dict(size=9, color="white"),
        hovertemplate="<b>Day %{x}</b><br>%{text}<br>%{y}h study<extra></extra>",
    ))
    fig_timeline.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#7c83a0", family="DM Sans"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)", color="#7c83a0", tickangle=-45),
        yaxis=dict(title="Hours", gridcolor="rgba(255,255,255,0.06)", color="#7c83a0"),
        margin=dict(l=0, r=0, t=10, b=10),
        height=280,
    )
    st.plotly_chart(fig_timeline, use_container_width=True, config={"displayModeBar": False})


# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#7c83a0;font-size:.82rem;padding:1rem 0">
    📘 <strong style="color:#a78bfa">PaperLens</strong> &nbsp;·&nbsp;
    Built with Streamlit, pdfplumber & Plotly &nbsp;·&nbsp;
    <em>"Focus on what matters. Ace the exam."</em>
</div>
""", unsafe_allow_html=True)
