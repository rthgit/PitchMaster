"""Pitch Master — Streamlit App.

Open-source fundraising copilot for founders and investors.

Usage:
    streamlit run app.py
"""

import streamlit as st
import os

from pitch_master import __version__
from pitch_master.config import LLM_PROVIDER, LLM_MODEL, OUTPUT_DIR
from pitch_master.llm_router import generate_text
from pitch_master.prompts import get_build_prompt, get_audit_prompt
from pitch_master.pef_engine import compute_pef100
from pitch_master.pdf_utils import extract_text_from_pdf, get_pdf_info
from pitch_master.export_utils import export_markdown, export_txt, export_docx, export_pdf
from pitch_master.languages import get_lang, get_lang_codes, LANGUAGES


st.set_page_config(
    page_title="Pitch Master",
    page_icon="🎯",
    layout="wide",
)

# --- Language selector ---
if "lang" not in st.session_state:
    st.session_state.lang = "EN"

with st.sidebar:
    lang_options = {f"{v['flag']} {v['lang_name']}": k for k, v in LANGUAGES.items()}
    selected = st.selectbox(
        "Language / Lingua / Idioma",
        options=list(lang_options.keys()),
        index=list(lang_options.keys()).index(f"{LANGUAGES[st.session_state.lang]['flag']} {LANGUAGES[st.session_state.lang]['lang_name']}"),
        key="lang_select",
    )
    st.session_state.lang = lang_options[selected]

L = get_lang(st.session_state.lang)

# --- Sidebar ---
with st.sidebar:
    st.title(L["sidebar_title"])
    st.caption(f"v{__version__}")
    st.divider()
    mode = st.radio(L["sidebar_mode"], [L["sidebar_build"], L["sidebar_audit"]], index=0)
    st.divider()
    st.markdown(f"**{L['sidebar_provider']}:** `{LLM_PROVIDER}`")
    st.markdown(f"**{L['sidebar_model']}:** `{LLM_MODEL}`")
    st.divider()
    st.markdown(L["sidebar_disclaimer"])

# --- Main ---
st.title(L["title_build"] if mode == L["sidebar_build"] else L["title_audit"])

if mode == L["sidebar_build"]:
    st.subheader(L["build_header"])
    st.markdown(L["build_subheader"])

    with st.form("build_form"):
        col1, col2 = st.columns(2)

        with col1:
            company_name = st.text_input(L["field_company"])
            one_liner = st.text_input(L["field_oneliner"])
            problem = st.text_area(L["field_problem"], height=100)
            solution = st.text_area(L["field_solution"], height=100)
            why_now = st.text_area(L["field_whynow"], height=80)

        with col2:
            market = st.text_area(L["field_market"], height=80)
            business_model = st.text_area(L["field_bizmodel"], height=80)
            traction = st.text_area(L["field_traction"], height=80)
            team = st.text_area(L["field_team"], height=80)
            ask = st.text_input(L["field_ask"])

        submitted = st.form_submit_button(L["btn_generate"], type="primary")

    if submitted:
        if not company_name or not one_liner or not problem or not solution:
            st.error(L["error_missing_fields"])
        else:
            prompt = f"""Build a compelling investor pitch for this startup:

Company: {company_name}
One-liner: {one_liner}
Problem: {problem}
Solution: {solution}
Why Now: {why_now or 'Not specified'}
Market: {market or 'Not specified'}
Business Model: {business_model or 'Not specified'}
Traction: {traction or 'Not specified'}
Team: {team or 'Not specified'}
Ask: {ask or 'Not specified'}

Provide:
1. Executive Summary (3-4 sentences)
2. Pitch Deck Outline (slide by slide with content for each slide)
3. Investor Narrative (300-400 words, natural flow)
4. Email Intro (50-80 words, ready to copy)
5. PEF Self-Audit (self-assessment on Attention/Understanding/Belief/Trust/FOMO)
"""
            with st.spinner(L["spinner_generating"]):
                try:
                    result = generate_text(prompt, get_build_prompt(st.session_state.lang))
                    st.divider()
                    st.subheader(L["generated_header"])
                    st.markdown(result)

                    # Export buttons
                    st.divider()
                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        if st.button(L["export_md"]):
                            path = export_markdown(result, f"pitch_{company_name}")
                            st.success(L["saved"].format(path=os.path.basename(path)))
                    with c2:
                        if st.button(L["export_txt"]):
                            path = export_txt(result, f"pitch_{company_name}")
                            st.success(L["saved"].format(path=os.path.basename(path)))
                    with c3:
                        if st.button(L["export_docx"]):
                            path = export_docx(result, f"pitch_{company_name}")
                            st.success(L["saved"].format(path=os.path.basename(path)))
                    with c4:
                        if st.button(L["export_pdf"]):
                            path = export_pdf(result, f"pitch_{company_name}")
                            st.success(L["saved"].format(path=os.path.basename(path)))

                except Exception as e:
                    st.error(L["error_generic"].format(error=e))

else:
    # --- AUDIT MODE ---
    st.subheader(L["audit_header"])
    st.markdown(L["audit_subheader"])

    uploaded_file = st.file_uploader(L["upload_pdf"], type=["pdf"])

    if uploaded_file:
        file_bytes = uploaded_file.read()

        # Extract text
        with st.spinner(L["spinner_extracting"]):
            try:
                text = extract_text_from_pdf(file_bytes)
                pdf_info = get_pdf_info(file_bytes)
            except ValueError as e:
                st.error(L["pdf_error"].format(error=e))
                text = None

        if text:
            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown(f"**{L['pdf_pages']}:** {pdf_info['page_count']}")
                st.markdown(f"**{L['pdf_words']}:** {len(text.split())}")

            # PEF-100 score
            pef = compute_pef100(text)

            with col2:
                st.metric(L["pef_score"], f"{pef['pef100']:.0f}/100")

            st.divider()

            # Layer breakdown
            st.subheader(L["layer_breakdown"])
            layer_cols = st.columns(5)
            layer_names = ["attention", "understanding", "belief", "trust", "fomo"]
            layer_labels = [L["layer_attention"], L["layer_understanding"], L["layer_belief"], L["layer_trust"], L["layer_fomo"]]
            for i, (name, label) in enumerate(zip(layer_names, layer_labels)):
                with layer_cols[i]:
                    st.metric(label, f"{pef['layers'][name]:.1f}/25")

            # Penalties
            st.subheader(L["penalties_header"])
            pen_cols = st.columns(2)
            with pen_cols[0]:
                st.metric(L["penalty_friction"], f"{pef['penalties']['cognitive_friction']:.1f}/10")
            with pen_cols[1]:
                st.metric(L["penalty_risk"], f"{pef['penalties']['perceived_risk']:.1f}/10")

            # Red flags
            if pef["red_flags"]:
                st.warning(f"**{L['red_flags']}:** {', '.join(pef['red_flags'])}")

            # Text preview
            with st.expander(L["text_preview"]):
                st.text(text[:2000])

            # LLM Audit
            st.divider()
            st.subheader(L["llm_audit_header"])

            if st.button(L["btn_deep_audit"], type="primary"):
                audit_prompt = f"""Audit this pitch deck text. Be direct, practical, and helpful.

--- TEXT START ---
{text[:6000]}
--- TEXT END ---

For each PEF-100 layer (Attention, Understanding, Belief, Trust, FOMO, Cognitive Friction, Perceived Risk):
1. Score 0-5 with explanation
2. Identify specific problems
3. Give concrete improvement suggestions

Also provide:
- Overall assessment (3-4 sentences)
- Top 3 fixes that would have the most impact
- What the deck does well (positive feedback)
"""
                with st.spinner(L["spinner_auditing"]):
                    try:
                        audit = generate_text(audit_prompt, get_audit_prompt(st.session_state.lang))
                        st.markdown(audit)

                        # Export audit
                        st.divider()
                        c1, c2, c3, c4 = st.columns(4)
                        with c1:
                            if st.button(L["export_audit_md"]):
                                path = export_markdown(audit, f"audit_{uploaded_file.name}")
                                st.success(L["saved"].format(path=os.path.basename(path)))
                        with c2:
                            if st.button(L["export_audit_txt"]):
                                path = export_txt(audit, f"audit_{uploaded_file.name}")
                                st.success(L["saved"].format(path=os.path.basename(path)))
                        with c3:
                            if st.button(L["export_audit_docx"]):
                                path = export_docx(audit, f"audit_{uploaded_file.name}")
                                st.success(L["saved"].format(path=os.path.basename(path)))
                        with c4:
                            if st.button(L["export_audit_pdf"]):
                                path = export_pdf(audit, f"audit_{uploaded_file.name}")
                                st.success(L["saved"].format(path=os.path.basename(path)))

                    except Exception as e:
                        st.error(L["error_generic"].format(error=e))

            # Footer
            st.divider()
            st.caption(L["footer_disclaimer"])
