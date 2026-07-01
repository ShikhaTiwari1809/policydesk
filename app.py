import json
import os
import streamlit as st

st.set_page_config(
    page_title="PolicyDesk",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={},
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --navy:       #1A2F5A;
    --navy-mid:   #243A6E;
    --teal:       #0B7EA3;
    --teal-bg:    #E8F4F8;
    --gold:       #F5A623;
    --gold-bg:    #FEF3DC;
    --bg:         #F4F6FA;
    --surface:    #FFFFFF;
    --border:     #DDE3EE;
    --text:       #1A2744;
    --text-mid:   #4A5568;
    --text-muted: #718096;
    --green:      #1E7E34;
    --green-bg:   #D4EDDA;
    --amber:      #856404;
    --amber-bg:   #FFF3CD;
    --red:        #C0392B;
    --red-bg:     #FDECEA;
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.stApp { background-color: var(--bg) !important; }

#MainMenu, footer { visibility: hidden; }
[data-testid="collapsedControl"], button[kind="header"] { display: none !important; }

[data-testid="stHeader"] {
    background: var(--bg) !important;
    height: 0 !important;
    min-height: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
}

.block-container {
    padding: 1.5rem 2rem 3rem 2rem !important;
    max-width: 1200px;
}

[data-testid="stSidebar"] {
    background: var(--navy) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * { color: #E2E8F0 !important; }
[data-testid="stSidebar"] .stRadio label {
    color: #CBD5E0 !important;
    font-size: 0.9rem !important;
    padding: 0.25rem 0 !important;
}
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] { background: transparent !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.15) !important; }

.pg-title {
    border-left: 4px solid var(--teal);
    padding: 0.4rem 0 0.6rem 1rem;
    margin: 0 0 1.75rem 0;
}
.pg-title h1 {
    color: var(--navy) !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    margin: 0 0 0.2rem 0 !important;
}
.pg-title p {
    color: var(--text-muted) !important;
    font-size: 0.87rem !important;
    margin: 0 !important;
}

.divider {
    height: 2px;
    background: linear-gradient(to right, var(--teal), transparent);
    margin: 1.5rem 0;
    border: none;
}

.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.3rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.card h3 {
    color: var(--navy) !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    margin: 0 0 0.7rem 0 !important;
}
.card p, .card li {
    color: var(--text-mid) !important;
    font-size: 0.87rem !important;
    line-height: 1.6 !important;
    margin: 0.2rem 0 !important;
}
.card ul { padding-left: 1rem; margin: 0; }

.stat-tile {
    background: var(--surface);
    border: 1px solid var(--border);
    border-top: 3px solid var(--teal);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.stat-tile .num {
    font-size: 1.9rem;
    font-weight: 700;
    color: var(--navy);
    line-height: 1;
}
.stat-tile .lbl {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-top: 0.3rem;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}

.verdict-pass { background: var(--green-bg); border-left: 5px solid var(--green); border-radius: 8px; padding: 1rem 1.4rem; margin-bottom: 1.25rem; }
.verdict-flag { background: var(--amber-bg); border-left: 5px solid var(--gold);  border-radius: 8px; padding: 1rem 1.4rem; margin-bottom: 1.25rem; }
.verdict-deny { background: var(--red-bg);   border-left: 5px solid var(--red);   border-radius: 8px; padding: 1rem 1.4rem; margin-bottom: 1.25rem; }
.verdict-pass .vt { color: var(--green) !important; font-size: 1.05rem; font-weight: 700; margin: 0 0 0.25rem; }
.verdict-flag .vt { color: var(--amber) !important; font-size: 1.05rem; font-weight: 700; margin: 0 0 0.25rem; }
.verdict-deny .vt { color: var(--red)   !important; font-size: 1.05rem; font-weight: 700; margin: 0 0 0.25rem; }
.verdict-pass .vb, .verdict-flag .vb, .verdict-deny .vb { color: var(--text) !important; font-size: 0.88rem; margin: 0; }

.badge-high     { background: var(--red-bg);   color: var(--red);   font-size: 0.71rem; font-weight: 600; padding: 0.13rem 0.5rem; border-radius: 12px; }
.badge-medium   { background: var(--amber-bg); color: var(--amber); font-size: 0.71rem; font-weight: 600; padding: 0.13rem 0.5rem; border-radius: 12px; }
.badge-low      { background: var(--green-bg); color: var(--green); font-size: 0.71rem; font-weight: 600; padding: 0.13rem 0.5rem; border-radius: 12px; }
.badge-added    { background: #D1FAE5; color: #065F46; font-size: 0.71rem; font-weight: 600; padding: 0.13rem 0.5rem; border-radius: 12px; }
.badge-removed  { background: #FEE2E2; color: #991B1B; font-size: 0.71rem; font-weight: 600; padding: 0.13rem 0.5rem; border-radius: 12px; }
.badge-modified { background: #EDE9FE; color: #5B21B6; font-size: 0.71rem; font-weight: 600; padding: 0.13rem 0.5rem; border-radius: 12px; }
.badge-approve  { background: #D1FAE5; color: #065F46; font-size: 0.71rem; font-weight: 600; padding: 0.13rem 0.5rem; border-radius: 12px; }
.badge-deny     { background: #FEE2E2; color: #991B1B; font-size: 0.71rem; font-weight: 600; padding: 0.13rem 0.5rem; border-radius: 12px; }
.badge-flag     { background: var(--gold-bg);  color: #92400E; font-size: 0.71rem; font-weight: 600; padding: 0.13rem 0.5rem; border-radius: 12px; }

.info-box {
    background: var(--teal-bg);
    border: 1px solid #B2D8E8;
    border-radius: 8px;
    padding: 0.85rem 1.1rem;
    font-size: 0.86rem;
    color: #1A4A5C !important;
    margin-bottom: 1rem;
}
.info-box strong { color: var(--teal) !important; }

.cite {
    background: var(--teal-bg);
    border-left: 3px solid var(--teal);
    border-radius: 0 6px 6px 0;
    padding: 0.65rem 1rem;
    font-size: 0.83rem;
    font-style: italic;
    color: var(--text-mid) !important;
    margin-bottom: 0.5rem;
}

.section-label {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.9px;
    color: var(--teal) !important;
    margin: 1.4rem 0 0.7rem 0;
}

.cpt-chip {
    display: inline-flex;
    align-items: center;
    background: var(--navy);
    color: #fff !important;
    font-size: 0.76rem;
    font-weight: 600;
    padding: 0.22rem 0.65rem;
    border-radius: 6px;
    margin: 0.15rem;
}
.cpt-chip span { color: var(--gold) !important; margin-right: 0.35rem; }

[data-testid="stFileUploader"] {
    border: 2px dashed var(--border) !important;
    border-radius: 8px !important;
    background: var(--surface) !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--navy), var(--teal)) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 7px !important;
    padding: 0.5rem 1.7rem !important;
    font-size: 0.9rem !important;
}
.stButton > button[kind="primary"]:hover { opacity: 0.88 !important; }

[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    background: var(--surface) !important;
    margin-bottom: 0.5rem !important;
}
[data-testid="stExpander"] summary {
    font-weight: 500 !important;
    font-size: 0.87rem !important;
    color: var(--text) !important;
    padding: 0.65rem 1rem !important;
}

.sb-logo { text-align: center; padding: 1.5rem 1rem 0.5rem; }
.sb-logo .icon { font-size: 2rem; line-height: 1; }
.sb-logo h2 { color: #fff !important; font-size: 1.15rem !important; font-weight: 700 !important; margin: 0.5rem 0 0.1rem !important; letter-spacing: 1px; }
.sb-logo .sub { color: rgba(255,255,255,0.5) !important; font-size: 0.68rem !important; text-transform: uppercase; letter-spacing: 1.5px; }
.gold-bar { height: 2px; background: var(--gold); margin: 1rem 0; border-radius: 2px; }
.sb-nav-lbl { color: rgba(255,255,255,0.4) !important; font-size: 0.67rem !important; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 0.4rem; }
.sb-foot { font-size: 0.7rem; color: rgba(255,255,255,0.3) !important; text-align: center; padding: 1.5rem 1rem 1rem; line-height: 1.7; }
</style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown("""
    <div class="sb-logo">
        <div class="icon">🏥</div>
        <h2>POLICYDESK</h2>
        <div class="sub">Cotiviti · Policy Intelligence</div>
    </div>
    <div class="gold-bar"></div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-nav-lbl">Tools</div>', unsafe_allow_html=True)

    MODE = st.radio(
        "",
        options=[
            "📋  Policy Summarizer",
            "🔍  Policy Diff",
            "⚙️  Policy-to-Rules",
            "🩺  Claim Review Copilot",
        ],
        index=0,
        label_visibility="collapsed",
    )

    st.markdown('<div class="gold-bar"></div>', unsafe_allow_html=True)

    

SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "sample_docs")


def load_sample(filename: str) -> str:
    path = os.path.join(SAMPLE_DIR, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def upload_or_sample(label: str, sample_file: str, key: str, hint: str = "") -> str:
    col_u, col_s = st.columns([3, 2])
    with col_u:
        uploaded = st.file_uploader(label, type=["pdf", "txt"], key=f"up_{key}", help=hint)
    with col_s:
        st.markdown("<br>", unsafe_allow_html=True)
        use_sample = st.checkbox(f"Use sample: `{sample_file}`", key=f"smp_{key}")

    if uploaded:
        from utils.pdf_parser import extract_text_from_upload
        try:
            text = extract_text_from_upload(uploaded)
            st.markdown(
                f'<div class="info-box">✅ <strong>{uploaded.name}</strong> — {len(text):,} chars</div>',
                unsafe_allow_html=True,
            )
            return text
        except Exception as e:
            st.error(str(e))
            return ""
    elif use_sample:
        text = load_sample(sample_file)
        if text:
            st.markdown(
                f'<div class="info-box">📄 Loaded <strong>{sample_file}</strong></div>',
                unsafe_allow_html=True,
            )
        else:
            st.warning(f"File not found: {sample_file}")
        return text
    return ""


def page_header(icon: str, title: str, subtitle: str):
    st.markdown(f"""
    <div class="pg-title">
        <h1>{icon} {title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def section(label: str):
    st.markdown(f'<div class="section-label">{label}</div>', unsafe_allow_html=True)


def card(title: str, items: list, icon: str = ""):
    if not items:
        return
    bullets = "".join(f"<li>{i}</li>" for i in items)
    st.markdown(f"""
    <div class="card">
        <h3>{icon} {title}</h3>
        <ul>{bullets}</ul>
    </div>
    """, unsafe_allow_html=True)


def stats_row(items: list[tuple]):
    cols = st.columns(len(items))
    for col, (val, lbl, color) in zip(cols, items):
        with col:
            st.markdown(f"""
            <div class="stat-tile" style="border-top-color:{color}">
                <div class="num" style="color:{color}">{val}</div>
                <div class="lbl">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)


if MODE == "📋  Policy Summarizer":
    page_header("📋", "Policy Summarizer",
        "Upload a CMS or payer policy and get a structured breakdown — "
        "criteria, CPT codes, documentation requirements, and exclusions.")

    policy_text = upload_or_sample(
        "Upload policy document",
        "lcd_epidural_steroid.txt",
        "summarizer",
        hint="CMS LCDs, NCD articles, payer policy PDFs, or plain text",
    )

    if policy_text:
        with st.expander("Preview document"):
            st.text_area("", policy_text[:3000] + ("…" if len(policy_text) > 3000 else ""),
                         height=150, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("Run Summary", type="primary", disabled=not policy_text)

    if run_btn and policy_text:
        with st.spinner("Analyzing…"):
            from modes.summarizer import run as summarize
            try:
                result = summarize(policy_text)
            except Exception as e:
                st.error(str(e))
                st.stop()

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"""
            <div class="card">
                <h3>📌 {result.get('policy_name', 'Policy')}</h3>
                <p><strong>ID:</strong> {result.get('policy_id') or '—'}</p>
                <p><strong>Effective:</strong> {result.get('effective_date') or '—'}</p>
                <p style="margin-top:0.5rem">{result.get('purpose', '')}</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            covered = result.get("covered_services", [])
            st.markdown(f"""
            <div class="card">
                <h3>🏷️ Covered Services</h3>
                {''.join(f'<p>• {s}</p>' for s in covered) if covered else '<p>None listed</p>'}
            </div>
            """, unsafe_allow_html=True)

        with col3:
            cpts = result.get("cpt_codes", [])
            chips = "".join(
                f'<div class="cpt-chip"><span>{c.get("code","")}</span>{c.get("description","")}</div>'
                for c in cpts
            ) if cpts else "<p>None listed</p>"
            st.markdown(f"""
            <div class="card">
                <h3>🔢 CPT Codes</h3>
                <div style="display:flex;flex-wrap:wrap;gap:4px">{chips}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        col_l, col_r = st.columns(2)
        with col_l:
            card("Coverage Criteria", result.get("coverage_criteria", []), "✅")
            card("Key Notes", result.get("key_notes", []), "⚠️")
        with col_r:
            card("Documentation Required", result.get("documentation_requirements", []), "📁")
            card("Exclusions", result.get("exclusions", []), "🚫")

        with st.expander("View raw output"):
            st.json(result)


elif MODE == "🔍  Policy Diff":
    page_header("🔍", "Policy Diff",
        "Compare two versions of a policy and see exactly what changed, "
        "ranked by clinical and billing impact.")

    col_a, col_b = st.columns(2)
    with col_a:
        section("Version A — Older")
        text_a = upload_or_sample("Upload Version A", "em_guidelines_2023.txt", "diff_a")
    with col_b:
        section("Version B — Newer")
        text_b = upload_or_sample("Upload Version B", "em_guidelines_2024.txt", "diff_b")

    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("Compare", type="primary", disabled=not (text_a and text_b))

    if run_btn and text_a and text_b:
        with st.spinner("Comparing…"):
            from modes.diff import run as diff_policies
            try:
                result = diff_policies(text_a, text_b)
            except Exception as e:
                st.error(str(e))
                st.stop()

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        total = result.get("total_changes", len(result.get("changes", [])))
        high  = result.get("high_impact_count", 0)
        med   = result.get("medium_impact_count", 0)
        low   = result.get("low_impact_count", 0)

        stats_row([
            (total, "Total Changes", "#1A2F5A"),
            (high,  "High Impact",   "#C0392B"),
            (med,   "Medium Impact", "#856404"),
            (low,   "Low Impact",    "#1E7E34"),
        ])

        st.markdown(f'<div class="info-box" style="margin-top:1rem">{result.get("summary","")}</div>',
                    unsafe_allow_html=True)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        order = {"High": 0, "Medium": 1, "Low": 2}
        changes = sorted(result.get("changes", []), key=lambda c: order.get(c.get("impact", "Low"), 3))

        IMPACT_ICON = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
        TYPE_ICON   = {"Added": "➕", "Removed": "➖", "Modified": "✏️"}

        for ch in changes:
            impact = ch.get("impact", "Low")
            ctype  = ch.get("change_type", "Modified")
            imp_badge  = f'<span class="badge-{impact.lower()}">{impact}</span>'
            type_badge = f'<span class="badge-{ctype.lower()}">{ctype}</span>'

            with st.expander(
                f"{IMPACT_ICON.get(impact,'⚪')} {TYPE_ICON.get(ctype,'•')}  {ch.get('section','')}"
            ):
                st.markdown(f"{imp_badge} &nbsp; {type_badge}", unsafe_allow_html=True)
                st.markdown(f"**{ch.get('description','')}**")

                if ch.get("version_a_text") or ch.get("version_b_text"):
                    ca, cb = st.columns(2)
                    with ca:
                        if ch.get("version_a_text"):
                            st.markdown("**Before**")
                            st.markdown(f'<div class="cite">{ch["version_a_text"]}</div>',
                                        unsafe_allow_html=True)
                    with cb:
                        if ch.get("version_b_text"):
                            st.markdown("**After**")
                            st.markdown(f'<div class="cite">{ch["version_b_text"]}</div>',
                                        unsafe_allow_html=True)

        with st.expander("View raw output"):
            st.json(result)


elif MODE == "⚙️  Policy-to-Rules":
    page_header("⚙️", "Policy-to-Rules",
        "Convert policy language into structured rules ready for a "
        "claims adjudication or rules engine.")

    policy_text = upload_or_sample(
        "Upload policy document", "lcd_epidural_steroid.txt", "rules"
    )

    fmt = st.radio("Output format", [
        "JSON  (structured rules list)",
        "Python  (if/then adjudication function)",
    ], label_visibility="collapsed", horizontal=True)
    as_json = fmt.startswith("JSON")

    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("Extract Rules", type="primary", disabled=not policy_text)

    if run_btn and policy_text:
        with st.spinner("Extracting…"):
            from modes.rules_converter import run_json, run_python
            try:
                result = run_json(policy_text) if as_json else run_python(policy_text)
            except Exception as e:
                st.error(str(e))
                st.stop()

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        if as_json and isinstance(result, list):
            approve = sum(1 for r in result if r.get("action") == "APPROVE")
            deny    = sum(1 for r in result if r.get("action") == "DENY")
            flag    = sum(1 for r in result if r.get("action") == "FLAG_FOR_REVIEW")

            stats_row([
                (len(result), "Total Rules",     "#1A2F5A"),
                (approve,     "Approve",          "#065F46"),
                (deny,        "Deny",             "#991B1B"),
                (flag,        "Flag for Review",  "#92400E"),
            ])

            st.markdown('<hr class="divider">', unsafe_allow_html=True)

            ACTION_BADGE = {"APPROVE": "badge-approve", "DENY": "badge-deny", "FLAG_FOR_REVIEW": "badge-flag"}
            ACTION_ICON  = {"APPROVE": "✅", "DENY": "❌", "FLAG_FOR_REVIEW": "⚠️"}

            for rule in result:
                action = rule.get("action", "FLAG_FOR_REVIEW")
                with st.expander(
                    f"{ACTION_ICON.get(action,'•')}  {rule.get('rule_id','')} — {rule.get('description','')}"
                ):
                    st.markdown(
                        f'<span class="{ACTION_BADGE.get(action,"badge-flag")}">{action}</span>'
                        f'<span style="color:var(--text-muted);font-size:0.78rem;margin-left:8px">'
                        f'Priority {rule.get("priority","")}</span>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(f"**Condition:** {rule.get('condition','')}")
                    st.markdown(f"**Rationale:** {rule.get('rationale','')}")

            with st.expander("Raw JSON"):
                st.json(result)
        else:
            st.code(result if isinstance(result, str) else str(result), language="python")


elif MODE == "🩺  Claim Review Copilot":
    page_header("🩺", "Claim Review Copilot",
        "Run a claim against a policy and get a rule-by-rule breakdown "
        "with cited policy text to support the reviewer's decision.")

    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown("**Policy document**")
        policy_text = upload_or_sample(
            "Upload policy", "lcd_epidural_steroid.txt", "cop_policy"
        )

    with col_r:
        st.markdown("**Claim**")
        src = st.radio("", ["Use sample claims", "Paste JSON"],
                       label_visibility="collapsed", horizontal=True, key="clm_src")
        claim_data = None

        if src == "Use sample claims":
            raw = load_sample("synthetic_claims.json")
            if raw:
                all_claims = json.loads(raw)
                opts = [
                    f"{c.get('claim_id','')} · {c.get('procedure_description','')}"
                    for c in all_claims
                ]
                sel = st.selectbox("Select a claim", opts)
                claim_data = all_claims[opts.index(sel)]
                with st.expander("Claim details"):
                    st.json(claim_data)
            else:
                st.warning("Sample claims file not found.")
        else:
            raw_in = st.text_area("Paste claim JSON", height=220)
            if raw_in:
                try:
                    claim_data = json.loads(raw_in)
                except json.JSONDecodeError:
                    st.error("Invalid JSON.")

    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("Review Claim", type="primary",
                        disabled=not (policy_text and claim_data))

    if run_btn and policy_text and claim_data:
        with st.spinner("Reviewing…"):
            from modes.claim_copilot import run as adjudicate
            try:
                result = adjudicate(policy_text, claim_data)
            except Exception as e:
                st.error(str(e))
                st.stop()

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        decision   = result.get("decision", "FLAG")
        confidence = result.get("confidence", "Low")
        summary    = result.get("summary", "")

        VERDICTS = {
            "PASS": ("verdict-pass", "✅ Pass"),
            "FLAG": ("verdict-flag", "⚠️ Flag for Review"),
            "DENY": ("verdict-deny", "❌ Deny"),
        }
        css, label = VERDICTS.get(decision, ("verdict-flag", "⚠️ Flag"))

        st.markdown(f"""
        <div class="{css}">
            <p class="vt">{label}
                <span style="font-weight:400;font-size:0.83rem;opacity:0.75;margin-left:6px">
                    Confidence: {confidence}
                </span>
            </p>
            <p class="vb">{summary}</p>
        </div>
        """, unsafe_allow_html=True)

        col_rules, col_cites = st.columns([3, 2])

        with col_rules:
            section("Rule evaluation")
            for r in result.get("reasons", []):
                met  = r.get("met", False)
                with st.expander(f"{'✅' if met else '❌'}  {r.get('rule', '')}"):
                    st.markdown(r.get("explanation", ""))

        with col_cites:
            section("Policy citations")
            for cite in result.get("policy_citations", []):
                st.markdown(f'<div class="cite">"{cite}"</div>', unsafe_allow_html=True)

            missing = result.get("missing_documentation", [])
            if missing:
                section("Missing documentation")
                for doc in missing:
                    st.markdown(f"• {doc}")

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="card">
            <h3>👤 For the reviewer</h3>
            <p>{result.get('recommendation', '')}</p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("View raw output"):
            st.json(result)
