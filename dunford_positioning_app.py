import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

px.defaults.template = "plotly_dark"

st.set_page_config(page_title="Obviously Awesome Positioning Canvas", layout="wide")
st.title("Obviously Awesome Positioning Canvas — (Dunford)")

st.caption("Anchor in the right reference frame, surface true differentiators, and generate a crisp positioning statement.")

sample_alternatives = pd.DataFrame({
    "alternative": ["Do nothing / status quo", "In-house process", "Competitor A", "Competitor B"],
    "type": ["Status Quo", "In-house", "Competitor", "Competitor"],
    "notes": ["Spreadsheet + manual reviews", "Ops team + templates", "Well-known incumbent", "Low-cost SaaS"]
})

sample_attributes = pd.DataFrame({
    "attribute": ["Revenue playbooks", "Done-for-you onboarding", "Cohort analytics", "Guarantee / risk reversal", "Partner ecosystem"],
    "evidence": ["12 case studies", "2‑week setup SLA", "Weekly ROI reports", "30‑day guarantee", "10 certified partners"],
    "importance_icp": [9, 8, 7, 8, 6],
    "differentiation": [8, 7, 8, 6, 7]
})

sample_themes = pd.DataFrame({
    "value_theme": ["Revenue Growth", "Speed to Value", "Risk Reduction", "Operational Leverage"],
    "customer_benefit": ["Faster pipeline to cash", "Live in 14 days", "Proof + guarantees", "Do more with same headcount"],
    "supporting_attributes": ["Revenue playbooks; Cohort analytics", "Done-for-you onboarding", "Guarantee / risk reversal", "Partner ecosystem"]
})

sample_icp = pd.DataFrame({
    "segment": ["B2B SaaS"],
    "company_size": ["50–500"],
    "geo": ["ANZ / US"],
    "primary_pain": ["Stalled growth; inconsistent pipeline"],
    "use_cases": ["Outbound acceleration; RevOps maturity"],
    "must_have": ["Proof of ROI in <60 days"],
    "buyer_title": ["Head of Growth / CRO"],
    "user_title": ["SDR Lead / RevOps"]
})

sample_category = pd.DataFrame({
    "proposed_category": ["Revenue Operating System"],
    "alt_categories_considered": ["Sales consulting; RevOps tooling"],
    "why_this_category": ["Signals outcome not effort; aligns with exec buyer"],
    "tagline": ["Turn GTM chaos into a revenue OS"]
})

sample_checks = pd.DataFrame({
    "clear_reference_frame": [True],
    "specific_icp": [True],
    "provable_differentiators": [True],
    "resonates_in_calls": [False],
    "avoids_feature_battle": [True]
})

with st.sidebar:
    st.header("Data")
    mode = st.radio("Choose data mode", ["Manual editor", "Upload CSVs"], index=0)
    st.caption("Upload CSVs named (or column-matched): alternatives, attributes, themes, icp, category, checks")

def assign_or_default(uploaded_list):
    frames = {"alternatives": None, "attributes": None, "themes": None, "icp": None, "category": None, "checks": None}
    col_sigs = {
        "alternatives": {"alternative","type","notes"},
        "attributes": {"attribute","evidence","importance_icp","differentiation"},
        "themes": {"value_theme","customer_benefit","supporting_attributes"},
        "icp": {"segment","company_size","geo","primary_pain","use_cases","must_have","buyer_title","user_title"},
        "category": {"proposed_category","alt_categories_considered","why_this_category","tagline"},
        "checks": {"clear_reference_frame","specific_icp","provable_differentiators","resonates_in_calls","avoids_feature_battle"}
    }
    if uploaded_list:
        for f in uploaded_list:
            try:
                df = pd.read_csv(f)
            except Exception:
                continue
            name = (f.name or "").lower()
            matched = None
            for key, sig in col_sigs.items():
                if sig.issubset(set(df.columns)) or key in name:
                    frames[key] = df
                    matched = key
                    break
            if not matched and set(df.columns) == col_sigs["attributes"]:
                frames["attributes"] = df
    frames["alternatives"] = frames["alternatives"] or sample_alternatives.copy()
    frames["attributes"]   = frames["attributes"]   or sample_attributes.copy()
    frames["themes"]       = frames["themes"]       or sample_themes.copy()
    frames["icp"]          = frames["icp"]          or sample_icp.copy()
    frames["category"]     = frames["category"]     or sample_category.copy()
    frames["checks"]       = frames["checks"]       or sample_checks.copy()
    return frames

if mode == "Upload CSVs":
    with st.sidebar:
        uploads = st.file_uploader("Upload CSV files", type=["csv"], accept_multiple_files=True)
    frames = assign_or_default(uploads)
else:
    if "pc_frames" not in st.session_state:
        st.session_state.pc_frames = {
            "alternatives": sample_alternatives.copy(),
            "attributes": sample_attributes.copy(),
            "themes": sample_themes.copy(),
            "icp": sample_icp.copy(),
            "category": sample_category.copy(),
            "checks": sample_checks.copy(),
        }
    with st.sidebar:
        c1, c2 = st.columns(2)
        if c1.button("Reset to sample"):
            st.session_state.pc_frames = {
                "alternatives": sample_alternatives.copy(),
                "attributes": sample_attributes.copy(),
                "themes": sample_themes.copy(),
                "icp": sample_icp.copy(),
                "category": sample_category.copy(),
                "checks": sample_checks.copy(),
            }

    st.subheader("Competitive Alternatives")
    st.session_state.pc_frames["alternatives"] = st.data_editor(
        st.session_state.pc_frames["alternatives"], num_rows="dynamic", use_container_width=True
    )

    st.subheader("Unique Attributes (score these 1–10)")
    st.session_state.pc_frames["attributes"] = st.data_editor(
        st.session_state.pc_frames["attributes"], num_rows="dynamic", use_container_width=True,
        column_config={
            "importance_icp": st.column_config.NumberColumn("importance_icp", min_value=0, max_value=10, step=1),
            "differentiation": st.column_config.NumberColumn("differentiation", min_value=0, max_value=10, step=1),
        }
    )

    st.subheader("Value Themes")
    st.session_state.pc_frames["themes"] = st.data_editor(
        st.session_state.pc_frames["themes"], num_rows="dynamic", use_container_width=True
    )

    st.subheader("ICP (best-fit customers)")
    st.session_state.pc_frames["icp"] = st.data_editor(
        st.session_state.pc_frames["icp"], num_rows="dynamic", use_container_width=True
    )

    st.subheader("Market Category")
    st.session_state.pc_frames["category"] = st.data_editor(
        st.session_state.pc_frames["category"], num_rows="dynamic", use_container_width=True
    )

    st.subheader("Customer Narrative Check")
    st.session_state.pc_frames["checks"] = st.data_editor(
        st.session_state.pc_frames["checks"], num_rows="dynamic", use_container_width=True
    )

    frames = st.session_state.pc_frames

st.markdown("---")
st.subheader("Differentiator Scorecard")

with st.sidebar:
    st.header("Weights")
    w_imp = st.slider("Importance to ICP (weight)", 0.1, 3.0, 1.2, 0.1)
    w_diff = st.slider("Differentiation (weight)", 0.1, 3.0, 1.0, 0.1)

attrs = frames["attributes"].copy()
for c in ["importance_icp","differentiation"]:
    attrs[c] = pd.to_numeric(attrs[c], errors="coerce").fillna(0).clip(0,10)

attrs["score"] = (attrs["importance_icp"]**w_imp) * (attrs["differentiation"]**w_diff)

score_cols = ["attribute","importance_icp","differentiation","score","evidence"]
st.dataframe(attrs[score_cols].sort_values("score", ascending=False).round(3), use_container_width=True)

fig_bar = px.bar(attrs.sort_values("score", ascending=False), x="attribute", y="score",
                 hover_data=["importance_icp","differentiation","evidence"],
                 title="Attribute Differentiation Score")
st.plotly_chart(fig_bar, use_container_width=True)
try:
    png_bytes = fig_bar.to_image(format="png", scale=2)
    st.download_button("🖼️ Download scorecard as PNG", data=png_bytes, file_name="differentiator_scorecard.png", mime="image/png")
except Exception as e:
    st.info("PNG export needs `kaleido` (in requirements). If it fails locally, reinstall/upgrade `kaleido`.")

fig_scatter = px.scatter(attrs, x="importance_icp", y="differentiation", text="attribute",
                         size="score", size_max=30, title="Importance vs Differentiation (bubble=size score)")
fig_scatter.update_traces(textposition="top center")
st.plotly_chart(fig_scatter, use_container_width=True)
try:
    scatter_png = fig_scatter.to_image(format="png", scale=2)
    st.download_button("🖼️ Download scatter as PNG", data=scatter_png, file_name="importance_vs_diff.png", mime="image/png")
except Exception:
    pass

st.markdown("---")
st.subheader("Positioning Statement")

top_attr = attrs.sort_values("score", ascending=False).head(1)["attribute"].tolist()
competitors = frames["alternatives"][frames["alternatives"]["type"].str.contains("Competitor", case=False, na=False)]["alternative"].tolist()
icp_row = frames["icp"].iloc[0] if not frames["icp"].empty else None
cat_row = frames["category"].iloc[0] if not frames["category"].empty else None

default_icp = icp_row["segment"] if icp_row is not None and "segment" in icp_row else "your ICP"
default_pain = icp_row["primary_pain"] if icp_row is not None and "primary_pain" in icp_row else "their primary pain"
default_cat  = cat_row["proposed_category"] if cat_row is not None and "proposed_category" in cat_row else "your category"
default_val  = frames["themes"]["customer_benefit"].iloc[0] if not frames["themes"].empty else "key value"
default_comp = competitors[0] if competitors else "the usual alternative"
default_diff = top_attr[0] if top_attr else "your differentiator"

col1, col2 = st.columns(2)
with col1:
    icp_in   = st.text_input("ICP", value=str(default_icp))
    pain_in  = st.text_input("Primary pain/problem", value=str(default_pain))
    cat_in   = st.text_input("Market category", value=str(default_cat))
with col2:
    value_in = st.text_input("Core value/outcome", value=str(default_val))
    comp_in  = st.text_input("Main comparator", value=str(default_comp))
    diff_in  = st.text_input("Differentiator (anchor)", value=str(default_diff))

stmt = f"For {icp_in}, who struggle with {pain_in}, we are a {cat_in} that delivers {value_in}. Unlike {comp_in}, we {diff_in}."
st.text_area("Generated statement", value=stmt, height=90)
st.download_button("⬇️ Download statement (Markdown)", data=f"**Positioning Statement**\n\n{stmt}\n", file_name="positioning_statement.md", mime="text/markdown")

st.markdown("---")
st.subheader("Customer Narrative Check")
checks = frames["checks"].copy()
for c in checks.columns:
    if checks[c].dtype != bool:
        checks[c] = checks[c].astype(str).str.lower().isin(["true","1","yes","y"])
st.dataframe(checks, use_container_width=True)
score = int(checks.iloc[0].sum()) if not checks.empty else 0
st.write(f"✅ Narrative health score: **{score}/{checks.shape[1]}**")

with st.sidebar.expander("Google Sheets (optional)", expanded=False):
    st.caption("Set secrets in Streamlit Cloud: 'gcp_service_account' (JSON) and 'gsheets.url'.")
    load_btn = st.button("Load all tables")
    save_btn = st.button("Save all tables")

def _get_ws(url, title="data"):
    import gspread
    from google.oauth2.service_account import Credentials
    sa = st.secrets.get("gcp_service_account")
    if not sa or not st.secrets.get("gsheets", {}).get("url"):
        raise RuntimeError("Missing secrets: 'gcp_service_account' and/or 'gsheets.url'.")
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(sa, scopes=scopes)
    gc = gspread.authorize(creds)
    sh = gc.open_by_url(st.secrets["gsheets"]["url"])
    try:
        ws = sh.worksheet(title)
    except gspread.exceptions.WorksheetNotFound:
        ws = sh.add_worksheet(title=title, rows="1000", cols="26")
    return ws

def _df_to_ws(ws, df_in):
    values = [list(df_in.columns)] + df_in.astype(object).where(pd.notnull(df_in), "").values.tolist()
    ws.clear()
    ws.update(values)

def _ws_to_df(ws):
    rows = ws.get_all_values()
    if not rows:
        return pd.DataFrame()
    hdr, data = rows[0], rows[1:]
    return pd.DataFrame(data, columns=hdr)

sheet_tabs = {"alternatives":"alternatives", "attributes":"attributes", "themes":"themes", "icp":"icp", "category":"category", "checks":"checks"}

if 'load_btn' in locals() and load_btn:
    try:
        loaded = {}
        for key, tab in sheet_tabs.items():
            ws = _get_ws(st.secrets["gsheets"]["url"], tab)
            loaded[key] = _ws_to_df(ws)
        for c in ["importance_icp","differentiation"]:
            if c in loaded["attributes"].columns:
                loaded["attributes"][c] = pd.to_numeric(loaded["attributes"][c], errors="coerce")
        if mode == "Manual editor":
            for k,v in loaded.items():
                if not v.empty:
                    frames[k] = v
            st.success("Loaded tables from Google Sheets.")
            st.session_state.pc_frames = frames
            st.rerun()
        else:
            st.warning("Switch to Manual editor to see the loaded tables.")
    except Exception as e:
        st.error(f"Load failed: {e}")

if 'save_btn' in locals() and save_btn:
    try:
        for key, tab in sheet_tabs.items():
            ws = _get_ws(st.secrets["gsheets"]["url"], tab)
            _df_to_ws(ws, frames[key])
        st.success("Saved all tables to Google Sheets.")
    except Exception as e:
        st.error(f"Save failed: {e}")
