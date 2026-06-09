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
from pitch_master.prompts import BUILD_SYSTEM_PROMPT, AUDIT_SYSTEM_PROMPT
from pitch_master.pef_engine import compute_pef100
from pitch_master.pdf_utils import extract_text_from_pdf, get_pdf_info
from pitch_master.export_utils import export_markdown, export_txt, export_docx, export_pdf


st.set_page_config(
    page_title="Pitch Master",
    page_icon="🎯",
    layout="wide",
)

# --- Sidebar ---
with st.sidebar:
    st.title("🎯 Pitch Master")
    st.caption(f"v{__version__}")
    st.divider()
    mode = st.radio("Mode", ["Build Mode", "Audit Mode"], index=0)
    st.divider()
    st.markdown(f"**Provider:** `{LLM_PROVIDER}`")
    st.markdown(f"**Model:** `{LLM_MODEL}`")
    st.divider()
    st.markdown(
        "**Disclaimer:** This is a heuristic v0.1 score, not investment advice. "
        "Pitch Master does not decide whether a company is investable."
    )

# --- Main ---
st.title("🎯 Pitch Master" if mode == "Build Mode" else "🎯 Pitch Master — Audit")

if mode == "Build Mode":
    st.subheader("Build your pitch")
    st.markdown("Answer the questions below. The more detail you give, the better the output.")

    with st.form("build_form"):
        col1, col2 = st.columns(2)

        with col1:
            company_name = st.text_input("Company name *")
            one_liner = st.text_input("One-liner (what you do) *")
            problem = st.text_area("Problem you solve *", height=100)
            solution = st.text_area("Your solution *", height=100)
            why_now = st.text_area("Why now? (timing, trends, regulation)", height=80)

        with col2:
            market = st.text_area("Market (TAM/SAM, growth rate)", height=80)
            business_model = st.text_area("Business model (pricing, unit economics)", height=80)
            traction = st.text_area("Traction (revenue, users, pilots, growth)", height=80)
            team = st.text_area("Team (founders, backgrounds, unfair advantage)", height=80)
            ask = st.text_input("Ask (how much, what for)")

        submitted = st.form_submit_button("Generate Pitch", type="primary")

    if submitted:
        if not company_name or not one_liner or not problem or not solution:
            st.error("Please fill in at least: Company name, One-liner, Problem, Solution.")
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
            with st.spinner("Generating pitch..."):
                try:
                    result = generate_text(prompt, BUILD_SYSTEM_PROMPT)
                    st.divider()
                    st.subheader("Generated Pitch")
                    st.markdown(result)

                    # Export buttons
                    st.divider()
                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        if st.button("Export MD"):
                            path = export_markdown(result, f"pitch_{company_name}")
                            st.success(f"Saved: {os.path.basename(path)}")
                    with c2:
                        if st.button("Export TXT"):
                            path = export_txt(result, f"pitch_{company_name}")
                            st.success(f"Saved: {os.path.basename(path)}")
                    with c3:
                        if st.button("Export DOCX"):
                            path = export_docx(result, f"pitch_{company_name}")
                            st.success(f"Saved: {os.path.basename(path)}")
                    with c4:
                        if st.button("Export PDF"):
                            path = export_pdf(result, f"pitch_{company_name}")
                            st.success(f"Saved: {os.path.basename(path)}")

                except Exception as e:
                    st.error(f"Error: {e}")

else:
    # --- AUDIT MODE ---
    st.subheader("Audit a pitch deck")
    st.markdown("Upload a PDF pitch deck to get a PEF-100 score and improvement suggestions.")

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file:
        file_bytes = uploaded_file.read()

        # Extract text
        with st.spinner("Extracting text from PDF..."):
            try:
                text = extract_text_from_pdf(file_bytes)
                pdf_info = get_pdf_info(file_bytes)
            except ValueError as e:
                st.error(f"PDF Error: {e}")
                text = None

        if text:
            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown(f"**Pages:** {pdf_info['page_count']}")
                st.markdown(f"**Words:** {len(text.split())}")

            # PEF-100 score
            pef = compute_pef100(text)

            with col2:
                st.metric("PEF-100 Score", f"{pef['pef100']:.0f}/100")

            st.divider()

            # Layer breakdown
            st.subheader("Layer Breakdown")
            layer_cols = st.columns(5)
            layer_names = ["attention", "understanding", "belief", "trust", "fomo"]
            layer_labels = ["Attention", "Understanding", "Belief", "Trust", "FOMO"]
            for i, (name, label) in enumerate(zip(layer_names, layer_labels)):
                with layer_cols[i]:
                    st.metric(label, f"{pef['layers'][name]:.1f}/25")

            # Penalties
            st.subheader("Penalties")
            pen_cols = st.columns(2)
            with pen_cols[0]:
                st.metric("Cognitive Friction", f"{pef['penalties']['cognitive_friction']:.1f}/10")
            with pen_cols[1]:
                st.metric("Perceived Risk", f"{pef['penalties']['perceived_risk']:.1f}/10")

            # Red flags
            if pef["red_flags"]:
                st.warning(f"**Red Flags Found:** {', '.join(pef['red_flags'])}")

            # Text preview
            with st.expander("Text Preview (first 2000 chars)"):
                st.text(text[:2000])

            # LLM Audit
            st.divider()
            st.subheader("LLM-Powered Audit")

            if st.button("Run Deep Audit", type="primary"):
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
                with st.spinner("Running deep audit..."):
                    try:
                        audit = generate_text(audit_prompt, AUDIT_SYSTEM_PROMPT)
                        st.markdown(audit)

                        # Export audit
                        st.divider()
                        c1, c2, c3, c4 = st.columns(4)
                        with c1:
                            if st.button("Export Audit MD"):
                                path = export_markdown(audit, f"audit_{uploaded_file.name}")
                                st.success(f"Saved: {os.path.basename(path)}")
                        with c2:
                            if st.button("Export Audit TXT"):
                                path = export_txt(audit, f"audit_{uploaded_file.name}")
                                st.success(f"Saved: {os.path.basename(path)}")
                        with c3:
                            if st.button("Export Audit DOCX"):
                                path = export_docx(audit, f"audit_{uploaded_file.name}")
                                st.success(f"Saved: {os.path.basename(path)}")
                        with c4:
                            if st.button("Export Audit PDF"):
                                path = export_pdf(audit, f"audit_{uploaded_file.name}")
                                st.success(f"Saved: {os.path.basename(path)}")

                    except Exception as e:
                        st.error(f"Error: {e}")

            # Footer
            st.divider()
            st.caption(
                "PEF-100 is a heuristic v0.1 score. The real PEF-100 is a 23-variable measurement system "
                "validated through inter-rater reliability and factor analysis."
            )
