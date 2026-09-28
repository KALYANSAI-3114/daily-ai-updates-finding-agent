import html
from datetime import datetime
from urllib.parse import urlparse

import streamlit as st
from agent import get_ai_updates


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Daily Updates",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# STYLES
# ============================================================

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Instrument+Sans:wght@400;500;600&display=swap');

:root {
    --ink: #14213d;
    --ink-soft: #4a5568;
    --ink-faint: #7b8494;
    --paper: #eef1f6;
    --card: #ffffff;
    --line: #dde2ec;
    --accent: #2f4bff;
    --accent-soft: #e8ecff;
}

/* ---------- Page ---------- */
.stApp { background: var(--paper); }
#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }
.block-container { max-width: 1120px; padding-top: 2rem; padding-bottom: 3rem; }
html, body, .stApp, .stMarkdown, button, input, label {
    font-family: 'Instrument Sans', system-ui, sans-serif;
}

/* ---------- Hero ---------- */
.hero { padding: 8px 0 22px 0; }
.hero-date { font-size: 14px; color: var(--ink-faint); margin-bottom: 10px; }
.hero-title {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: clamp(34px, 6vw, 58px);
    font-weight: 800;
    line-height: 1.02;
    letter-spacing: -0.03em;
    color: var(--ink);
    margin: 0 0 12px 0;
}
.hero-sub { font-size: 17px; color: var(--ink-soft); max-width: 560px; line-height: 1.5; }

/* ---------- Button ---------- */
div[data-testid="stButton"] > button[kind="primary"] {
    background: var(--accent);
    border: none;
    color: #fff;
    font-weight: 600;
    font-size: 16px;
    padding: 0.75rem 1.4rem;
    border-radius: 12px;
    box-shadow: 0 6px 18px rgba(47, 75, 255, 0.28);
    transition: transform .15s ease, box-shadow .15s ease;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 24px rgba(47, 75, 255, 0.34);
}
div[data-testid="stButton"] > button[kind="primary"]:focus-visible {
    outline: 3px solid #9fb0ff;
    outline-offset: 2px;
}

/* ---------- Stats ---------- */
.stats { display: flex; flex-wrap: wrap; gap: 12px; margin: 26px 0 8px 0; }
.stat {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 12px 18px;
    min-width: 130px;
}
.stat-num {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 28px;
    font-weight: 700;
    color: var(--ink);
    line-height: 1.1;
}
.stat-label { font-size: 13px; color: var(--ink-faint); margin-top: 2px; }

/* ---------- Grid + cards ---------- */
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 440px), 1fr));
    gap: 18px;
    margin-top: 18px;
}
.card {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 24px 26px;
    display: flex;
    flex-direction: column;
    gap: 14px;
    box-shadow: 0 1px 2px rgba(20, 33, 61, 0.04);
}
.card.featured {
    grid-column: 1 / -1;
    padding: 32px 34px;
    border-color: #c9d2ff;
    background: linear-gradient(180deg, #ffffff 0%, #f6f8ff 100%);
}
.card-top { display: flex; align-items: center; justify-content: space-between; gap: 10px; flex-wrap: wrap; }
.chip {
    font-size: 13px;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 999px;
}
.flag { font-size: 13px; font-weight: 600; color: var(--accent); }
.card-title {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 22px;
    font-weight: 700;
    line-height: 1.25;
    letter-spacing: -0.01em;
    color: var(--ink);
    margin: 0;
}
.featured .card-title { font-size: 32px; letter-spacing: -0.02em; }
.company { font-size: 14px; color: var(--ink-faint); font-weight: 500; }
.summary { font-size: 15.5px; line-height: 1.65; color: var(--ink-soft); max-width: 70ch; }
.why {
    background: var(--accent-soft);
    border-left: 4px solid var(--accent);
    border-radius: 10px;
    padding: 12px 16px;
}
.why-label { font-size: 13px; font-weight: 700; color: #1f33c7; margin-bottom: 3px; }
.why-text { font-size: 14.5px; line-height: 1.55; color: #2b3563; }
.card-foot { margin-top: auto; padding-top: 4px; }
.source {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 14px;
    font-weight: 600;
    color: var(--accent) !important;
    text-decoration: none !important;
    border-bottom: 1.5px solid transparent;
}
.source:hover { border-bottom-color: var(--accent); }
.source:focus-visible { outline: 3px solid #9fb0ff; outline-offset: 3px; border-radius: 4px; }

/* ---------- Empty ---------- */
.empty {
    text-align: center;
    background: var(--card);
    border: 1px dashed #c3cadb;
    border-radius: 18px;
    padding: 56px 24px;
    margin-top: 26px;
}
.empty-icon { font-size: 44px; }
.empty-title {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: var(--ink);
    margin-top: 10px;
}
.empty-text { font-size: 15px; color: var(--ink-soft); margin-top: 6px; }

/* ---------- Footer ---------- */
.foot {
    text-align: center;
    color: var(--ink-faint);
    font-size: 13px;
    margin-top: 44px;
    padding-top: 18px;
    border-top: 1px solid var(--line);
}

@media (max-width: 640px) {
    .card, .card.featured { padding: 20px; }
    .featured .card-title { font-size: 25px; }
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


# ============================================================
# HELPERS
# ============================================================

# Category colors carry meaning: same kind of news, same color.
CATEGORY_STYLES = [
    (("model", "research", "benchmark", "paper"), ("#e3ebff", "#1f3fbf")),
    (("product", "launch", "release", "app", "feature"), ("#dcf5e7", "#146c3c")),
    (("fund", "invest", "business", "acqui", "market", "revenue"), ("#fff0d1", "#8a5a00")),
    (("policy", "regulat", "safety", "law", "ethic", "legal"), ("#ffe1e6", "#a3193a")),
    (("open", "tool", "developer", "framework", "api", "agent"), ("#ecdfff", "#6224b8")),
    (("hardware", "chip", "gpu", "infra", "cloud"), ("#dff3f7", "#116174")),
]
DEFAULT_STYLE = ("#e9ecf2", "#3d4759")


def category_style(category: str):
    key = (category or "").lower()
    for keywords, style in CATEGORY_STYLES:
        if any(k in key for k in keywords):
            return style
    return DEFAULT_STYLE


def esc(value) -> str:
    """Escape text so titles/summaries containing < > & can't break the layout."""
    return html.escape(str(value or ""), quote=True)


def domain_of(url: str) -> str:
    try:
        host = urlparse(url).netloc.lower()
        return host[4:] if host.startswith("www.") else host
    except Exception:
        return ""


def flat(markup: str) -> str:
    """
    Remove indentation and blank lines from HTML.
    Streamlit's markdown treats lines indented 4+ spaces as a code block,
    which is what makes indented HTML show up as raw text.
    """
    return "".join(line.strip() for line in markup.splitlines() if line.strip())


def card_html(update: dict, featured: bool = False) -> str:
    title = esc(update.get("title", "Untitled AI update"))
    company = esc(update.get("company", ""))
    category = esc(update.get("category", "AI"))
    summary = esc(update.get("summary", "No summary available."))
    why = esc(update.get("why_it_matters", ""))
    url = update.get("source_url", "") or ""

    bg, fg = category_style(update.get("category", ""))

    flag = '<span class="flag">Top story</span>' if featured else ""
    company_html = f'<div class="company">{company}</div>' if company else ""

    why_html = ""
    if why:
        why_html = f"""
        <div class="why">
            <div class="why-label">Why it matters</div>
            <div class="why-text">{why}</div>
        </div>
        """

    source_html = ""
    if url and url != "#" and url.startswith(("http://", "https://")):
        source_html = f"""
        <div class="card-foot">
            <a class="source" href="{esc(url)}" target="_blank" rel="noopener noreferrer">
                Read on {esc(domain_of(url)) or "source"} ↗
            </a>
        </div>
        """

    return flat(
        f"""
        <article class="card{' featured' if featured else ''}">
            <div class="card-top">
                <span class="chip" style="background:{bg};color:{fg};">{category}</span>
                {flag}
            </div>
            <h3 class="card-title">{title}</h3>
            {company_html}
            <div class="summary">{summary}</div>
            {why_html}
            {source_html}
        </article>
        """
    )


def stats_html(updates: list) -> str:
    companies = {u.get("company") for u in updates if u.get("company")}
    categories = {u.get("category") for u in updates if u.get("category")}
    items = [
        (len(updates), "updates"),
        (len(companies), "companies"),
        (len(categories), "categories"),
    ]
    boxes = "".join(
        f'<div class="stat"><div class="stat-num">{n}</div>'
        f'<div class="stat-label">{label}</div></div>'
        for n, label in items
    )
    return f'<div class="stats">{boxes}</div>'


# ============================================================
# HERO
# ============================================================

today = datetime.now().strftime("%A, %d %B %Y")

st.markdown(
    flat(
        f"""
        <div class="hero">
            <div class="hero-date">{today}</div>
            <h1 class="hero-title">AI Daily Updates</h1>
            <div class="hero-sub">
                The most important AI developments from the past 24 hours,
                with a plain-language note on why each one matters.
            </div>
        </div>
        """
    ),
    unsafe_allow_html=True,
)

btn_col, _ = st.columns([1, 2])
with btn_col:
    run_updates = st.button("Get AI updates", type="primary", use_container_width=True)


# ============================================================
# FETCH (results are kept in session_state so filters don't refetch)
# ============================================================

if run_updates:
    with st.spinner("Searching the latest AI news and analyzing updates…"):
        try:
            st.session_state["updates"] = get_ai_updates() or []
            st.session_state["fetched_at"] = datetime.now().strftime("%I:%M %p")
            st.session_state["error"] = None
        except Exception as error:
            st.session_state["updates"] = None
            st.session_state["error"] = str(error)


# ============================================================
# DISPLAY
# ============================================================

updates = st.session_state.get("updates")
error = st.session_state.get("error")

if error:
    st.error(f"Couldn't fetch AI updates: {error}. Check your API keys and try again.")

elif updates is None:
    st.markdown(
        flat(
            """
            <div class="empty">
                <div class="empty-icon">📰</div>
                <div class="empty-title">Ready for today's AI news?</div>
                <div class="empty-text">Select <b>Get AI updates</b> to search the web for what's new.</div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

elif not updates:
    st.warning("No significant AI updates were found in the past 24 hours. Try again later.")

else:
    st.markdown(stats_html(updates), unsafe_allow_html=True)
    st.caption(f"Last updated at {st.session_state.get('fetched_at', '')}")

    # ----- Category filter -----
    all_categories = sorted({u.get("category", "AI") for u in updates})
    if len(all_categories) > 1:
        if hasattr(st, "pills"):
            selected = st.pills(
                "Filter by category",
                all_categories,
                selection_mode="multi",
                label_visibility="collapsed",
            )
        else:
            selected = st.multiselect("Filter by category", all_categories)
    else:
        selected = []

    visible = [u for u in updates if not selected or u.get("category", "AI") in selected]

    if not visible:
        st.info("No updates match the selected categories.")
    else:
        cards = "".join(card_html(u, featured=(idx == 0)) for idx, u in enumerate(visible))
        st.markdown(f'<div class="grid">{cards}</div>', unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="foot">Web search by Tavily · Analysis by Groq GPT-OSS-120B</div>',
    unsafe_allow_html=True,
)