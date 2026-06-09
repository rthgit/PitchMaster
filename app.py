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
from pitch_master.languages import get_lang, LANGUAGES
from pitch_master.history import save_pitch, load_pitch, list_pitches, delete_pitch, get_stats
from pitch_master.templates import list_templates, get_template_fields


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

    # Status indicator
    if "app_started" not in st.session_state:
        st.session_state.app_started = False

    if not st.session_state.app_started:
        if st.button("🚀 Start Pitch Master", type="primary", use_container_width=True):
            st.session_state.app_started = True
            st.rerun()
        st.warning("App not started. Click the button above.")
    else:
        st.success("✅ App running")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⏹ Stop", use_container_width=True):
                st.session_state.app_started = False
                st.rerun()
        with col2:
            if st.button("🔄 Restart", use_container_width=True):
                st.session_state.app_started = False
                st.rerun()

    st.divider()

    # Main navigation (only if started)
    if st.session_state.app_started:
        page = st.radio(
            L["sidebar_mode"],
            [L["sidebar_build"], L["sidebar_audit"], "📊 Compare", "📁 History", "📈 Analytics"],
            index=0,
        )
    else:
        page = None

    st.divider()
    st.markdown(f"**{L['sidebar_provider']}:** `{LLM_PROVIDER}`")
    st.markdown(f"**{L['sidebar_model']}:** `{LLM_MODEL}`")
    st.divider()
    st.markdown(L["sidebar_disclaimer"])


# --- WELCOME SCREEN ---
if not st.session_state.app_started:
    st.title("🎯 Pitch Master")
    st.markdown("---")
    st.subheader("Welcome to Pitch Master")
    st.markdown("""
    Open-source fundraising copilot for founders and investors.

    **Features:**
    - 🏗️ **Build Mode** — Generate pitch decks from questionnaires
    - 🔍 **Audit Mode** — Analyze PDF pitch decks with PEF-100
    - 📊 **Compare** — Side-by-side deck comparison
    - 📁 **History** — Save and manage past pitches
    - 📈 **Analytics** — PEF-100 trends and insights

    **Getting Started:**
    1. Click **🚀 Start Pitch Master** in the sidebar
    2. Select your mode (Build / Audit)
    3. Start creating!

    **Quick Start:**
    ```bash
    # Windows
    start.bat

    # Or manually
    pip install -r requirements.txt
    streamlit run app.py
    ```
    """)
    st.markdown("---")
    st.caption("v" + __version__ + " | MIT License | Open Source")


# --- BUILD MODE ---
elif page == L["sidebar_build"]:
    st.title(L["title_build"])
    st.subheader(L["build_header"])

    # Template selector
    templates = list_templates()
    template_names = ["-- Custom --"] + [t["name"] for t in templates]
    selected_template = st.selectbox("Template (optional)", template_names, key="template_select")

    # Load template fields if selected
    template_fields = {}
    if selected_template != "-- Custom --":
        template_id = next(t["id"] for t in templates if t["name"] == selected_template)
        template_fields = get_template_fields(template_id)
        st.info(f"Loaded template: **{selected_template}** — {templates[template_id-1]['description'] if False else ''}")
        # Show description
        for t in templates:
            if t["id"] == template_id:
                st.info(f"Loaded template: **{selected_template}** — {t['description']}")
                break

    st.markdown(L["build_subheader"])

    with st.form("build_form"):
        col1, col2 = st.columns(2)

        with col1:
            company_name = st.text_input(L["field_company"], value=template_fields.get("company_name", ""))
            one_liner = st.text_input(L["field_oneliner"], value=template_fields.get("one_liner", ""))
            problem = st.text_area(L["field_problem"], value=template_fields.get("problem", ""), height=100)
            solution = st.text_area(L["field_solution"], value=template_fields.get("solution", ""), height=100)
            why_now = st.text_area(L["field_whynow"], value=template_fields.get("why_now", ""), height=80)

        with col2:
            market = st.text_area(L["field_market"], value=template_fields.get("market", ""), height=80)
            business_model = st.text_area(L["field_bizmodel"], value=template_fields.get("business_model", ""), height=80)
            traction = st.text_area(L["field_traction"], value=template_fields.get("traction", ""), height=80)
            team = st.text_area(L["field_team"], value=template_fields.get("team", ""), height=80)
            ask = st.text_input(L["field_ask"], value=template_fields.get("ask", ""))

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

                    # Save to history
                    save_pitch(company_name, "build", result, lang=st.session_state.lang)

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


# --- AUDIT MODE ---
elif page == L["sidebar_audit"]:
    st.title(L["title_audit"])
    st.subheader(L["audit_header"])
    st.markdown(L["audit_subheader"])

    uploaded_file = st.file_uploader(L["upload_pdf"], type=["pdf"])

    if uploaded_file:
        file_bytes = uploaded_file.read()

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

                        # Save to history
                        company_from_name = uploaded_file.name.replace(".pdf", "").replace("_", " ")
                        save_pitch(company_from_name, "audit", audit, pef_score=pef["pef100"], pef_data=pef, lang=st.session_state.lang)

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

            st.divider()
            st.caption(L["footer_disclaimer"])


# --- COMPARE MODE ---
elif page == "📊 Compare":
    st.title("📊 PEF-100 Comparison")
    st.markdown("Compare PEF-100 scores across multiple decks side by side.")

    # Get all audits from history
    audits = list_pitches(mode="audit")

    if not audits:
        st.info("No audits saved yet. Run some audits first to compare them.")
    else:
        # Select decks to compare
        deck_options = {f"{a['company_name']} ({a.get('pef_score', 'N/A')})": a["id"] for a in audits}
        selected_decks = st.multiselect(
            "Select decks to compare (up to 5)",
            options=list(deck_options.keys()),
            max_selections=5,
            key="compare_select",
        )

        if selected_decks:
            st.divider()

            # Comparison table
            cols = st.columns(len(selected_decks))
            for i, deck_label in enumerate(selected_decks):
                entry_id = deck_options[deck_label]
                entry = load_pitch(entry_id)
                if not entry:
                    continue

                with cols[i]:
                    st.subheader(entry["company_name"])

                    if entry.get("pef_score") is not None:
                        st.metric("PEF-100", f"{entry['pef_score']:.0f}/100")
                    else:
                        st.metric("PEF-100", "N/A")

                    if entry.get("pef_data"):
                        pef = entry["pef_data"]
                        st.markdown("**Layers:**")
                        for layer in ["attention", "understanding", "belief", "trust", "fomo"]:
                            st.markdown(f"- {layer.title()}: {pef['layers'].get(layer, 0):.1f}/25")

            # Bar chart comparison
            st.divider()
            st.subheader("Score Comparison")

            import pandas as pd
            chart_data = []
            for deck_label in selected_decks:
                entry_id = deck_options[deck_label]
                entry = load_pitch(entry_id)
                if entry and entry.get("pef_data"):
                    pef = entry["pef_data"]
                    chart_data.append({
                        "Deck": entry["company_name"],
                        "Attention": pef["layers"].get("attention", 0),
                        "Understanding": pef["layers"].get("understanding", 0),
                        "Belief": pef["layers"].get("belief", 0),
                        "Trust": pef["layers"].get("trust", 0),
                        "FOMO": pef["layers"].get("fomo", 0),
                    })

            if chart_data:
                df = pd.DataFrame(chart_data)
                df = df.set_index("Deck")
                st.bar_chart(df)


# --- BATCH AUDIT MODE ---
elif page == "📁 History":
    st.title("📁 Pitch History")

    stats = get_stats()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Saved", stats["total"])
    with col2:
        st.metric("Build Pitches", stats["build"])
    with col3:
        st.metric("Audits", stats["audit"])
    with col4:
        st.metric("Avg PEF-100", f"{stats['avg_pef']:.0f}" if stats['avg_pef'] else "N/A")

    st.divider()

    # Filter
    filter_mode = st.selectbox("Filter by mode", ["All", "Build", "Audit"], key="history_filter")
    mode_filter = None if filter_mode == "All" else filter_mode.lower()

    entries = list_pitches(mode=mode_filter)

    if not entries:
        st.info("No pitches saved yet.")
    else:
        for entry in entries:
            with st.expander(f"**{entry['company_name']}** — {entry['mode'].title()} — {entry.get('created_at', '')[:10]}"):
                col1, col2 = st.columns([1, 1])

                with col1:
                    st.markdown(f"**Mode:** {entry['mode'].title()}")
                    st.markdown(f"**Language:** {entry.get('lang', 'EN')}")
                    if entry.get("pef_score") is not None:
                        st.markdown(f"**PEF-100:** {entry['pef_score']:.0f}/100")

                with col2:
                    if st.button("Delete", key=f"del_{entry['id']}"):
                        delete_pitch(entry["id"])
                        st.rerun()

                # Show content preview
                content = entry.get("content", "")
                if len(content) > 500:
                    st.text(content[:500] + "...")
                else:
                    st.text(content)

                # Export buttons
                st.divider()
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    if st.button("MD", key=f"md_{entry['id']}"):
                        path = export_markdown(content, f"pitch_{entry['company_name']}")
                        st.success(f"Saved: {os.path.basename(path)}")
                with c2:
                    if st.button("TXT", key=f"txt_{entry['id']}"):
                        path = export_txt(content, f"pitch_{entry['company_name']}")
                        st.success(f"Saved: {os.path.basename(path)}")
                with c3:
                    if st.button("DOCX", key=f"docx_{entry['id']}"):
                        path = export_docx(content, f"pitch_{entry['company_name']}")
                        st.success(f"Saved: {os.path.basename(path)}")
                with c4:
                    if st.button("PDF", key=f"pdf_{entry['id']}"):
                        path = export_pdf(content, f"pitch_{entry['company_name']}")
                        st.success(f"Saved: {os.path.basename(path)}")


# --- ANALYTICS DASHBOARD ---
elif page == "📈 Analytics":
    st.title("📈 Analytics Dashboard")

    stats = get_stats()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Pitches", stats["total"])
    with col2:
        st.metric("Avg PEF-100", f"{stats['avg_pef']:.1f}" if stats['avg_pef'] else "N/A")
    with col3:
        st.metric("Audits", stats["audit"])

    st.divider()

    if stats["total"] == 0:
        st.info("No data yet. Run some audits to see analytics.")
    else:
        import pandas as pd

        # PEF Score distribution
        audits = list_pitches(mode="audit")
        if audits:
            st.subheader("PEF-100 Score Distribution")

            scores = [a.get("pef_score", 0) for a in audits if a.get("pef_score") is not None]
            if scores:
                df_scores = pd.DataFrame({"PEF-100 Score": scores})
                st.bar_chart(df_scores["PEF-100 Score"].value_counts().sort_index())

                # Layer averages
                st.subheader("Average Layer Scores")
                layer_avgs = {"attention": 0, "understanding": 0, "belief": 0, "trust": 0, "fomo": 0}
                count = 0
                for a in audits:
                    if a.get("pef_data") and a["pef_data"].get("layers"):
                        for layer in layer_avgs:
                            layer_avgs[layer] += a["pef_data"]["layers"].get(layer, 0)
                        count += 1

                if count > 0:
                    for layer in layer_avgs:
                        layer_avgs[layer] = round(layer_avgs[layer] / count, 1)

                    df_layers = pd.DataFrame([
                        {"Layer": k.title(), "Avg Score": v, "Max": 25}
                        for k, v in layer_avgs.items()
                    ])
                    st.bar_chart(df_layers.set_index("Layer")[["Avg Score", "Max"]])

        # Timeline
        st.subheader("Pitch Activity")
        all_entries = list_pitches()
        if all_entries:
            timeline_data = []
            for e in all_entries:
                timeline_data.append({
                    "Date": e.get("created_at", "")[:10],
                    "Mode": e["mode"].title(),
                    "Company": e["company_name"],
                })
            df_timeline = pd.DataFrame(timeline_data)
            st.dataframe(df_timeline, use_container_width=True, hide_index=True)
