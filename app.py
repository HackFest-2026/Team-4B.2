import streamlit as st
import time
import ai_engine

# 1. Page Configuration
st.set_page_config(
    page_title="AI PM Copilot | Enterprise Dashboard", 
    page_icon="🚀", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- HIGH-DENSITY SAAS STYLING INJECTION ---
st.markdown("""
<style>
    .stApp {
        background-color: #09090b;
        color: #f4f4f5;
    }
    .top-header {
        background: linear-gradient(90deg, rgba(99, 102, 241, 0.15) 0%, rgba(168, 85, 247, 0.15) 100%);
        border: 1px solid rgba(168, 85, 247, 0.3);
        padding: 16px 24px;
        border-radius: 12px;
        margin-bottom: 24px;
    }
    .stat-card {
        background-color: #18181b;
        border: 1px solid #27272a;
        padding: 16px;
        border-radius: 10px;
        text-align: center;
    }
    .stat-number {
        font-size: 22px;
        font-weight: 700;
        color: #a855f7;
    }
    .stat-label {
        font-size: 11px;
        color: #a1a1aa;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .stButton > button {
        border-radius: 8px;
        background-color: #18181b;
        color: #f4f4f5;
        transition: all 0.2s ease-in-out;
        border: 1px solid rgba(255, 255, 255, 0.1);
        font-weight: 500;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        border-color: #6366f1;
        background-color: #27272a;
        color: #ffffff;
    }
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def stream_text_with_cursor(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)

# --- HERO HEADER & SYSTEM METRICS BANNER ---
st.markdown("""
<div class="top-header">
    <h2 style="margin:0; font-size: 24px; font-weight: 700;">🚀 AI PM Copilot <span style="font-size: 14px; background: #6366f1; padding: 2px 8px; border-radius: 12px; vertical-align: middle;">v2.4 Enterprise</span></h2>
    <p style="margin: 4px 0 0 0; color: #a1a1aa; font-size: 14px;">Automated Product Requirements, Feature Prioritization, and Sentiment Analysis Engine.</p>
</div>
""", unsafe_allow_html=True)

# 4-Column Top KPI Telemetry
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown('<div class="stat-card"><div class="stat-number">-60%</div><div class="stat-label">Requirement Cycle Time</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="stat-card"><div class="stat-number">92%</div><div class="stat-label">Prioritization Accuracy</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="stat-card"><div class="stat-number">-40%</div><div class="stat-label">Spec Rework Rate</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown('<div class="stat-card"><div class="stat-number">Gemini 3.5 Lite</div><div class="stat-label">Active Neural Model</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- NAVIGATION SIDEBAR ---
st.sidebar.title("🛠️ PM Tool Suite")
menu_selection = st.sidebar.radio(
    "Select Workspace Module:", 
    ["📝 PRD Studio", "📊 RICE Prioritization Engine", "💬 Customer Feedback Hub"]
)

if "PRD Studio" in menu_selection:
    app_mode = "PRD"
elif "RICE Prioritization Engine" in menu_selection:
    app_mode = "RICE"
elif "Customer Feedback Hub" in menu_selection:
    app_mode = "FEEDBACK"

# --- WORKSPACE MODULES ---

# MODULE 1: PRD STUDIO
if app_mode == "PRD":
    st.subheader("📝 PRD Generator Studio")
    st.caption("Transform feature briefs into standard Product Requirement Documents in seconds.")
    
    col_input, col_output = st.columns([1, 1.2])
    
    with col_input:
        st.markdown("### 1. Configuration & Brief")
        st.markdown("**Quick Preset Briefs:**")
        preset_cols = st.columns(2)
        
        if "prd_brief_text" not in st.session_state:
            st.session_state.prd_brief_text = ""
            
        if preset_cols[0].button("⚡ Google SSO"):
            st.session_state.prd_brief_text = "One-click OAuth Google Sign-In button for mobile e-commerce checkout"
        if preset_cols[1].button("🌙 Dark Mode"):
            st.session_state.prd_brief_text = "System-wide dark mode theme toggle with schedule options"
            
        feature_idea = st.text_area(
            "Feature Description Brief:", 
            value=st.session_state.prd_brief_text,
            height=160,
            placeholder="e.g., An automated email digest sent every Monday summarizing team task progress..."
        )
        st.session_state.prd_brief_text = feature_idea
        
        generate_btn = st.button("🚀 Generate PRD Specification")

    with col_output:
        st.markdown("### 2. Generated Specification")
        
        if generate_btn:
            cleaned_input = feature_idea.strip()
            if len(cleaned_input) >= 3:
                with st.spinner("✨ Gemini AI analyzing requirements and drafting PRD..."):
                    st.session_state.raw_prd = ai_engine.generate_prd(cleaned_input)
                    st.session_state.show_prd_approval = True
            else:
                st.toast("Please enter a feature description briefly first.", icon="⚠️")
                
        if st.session_state.get("show_prd_approval"):
            st.info("💡 **AI Proposes, People Decide:** Review the rendered PRD below or expand the edit box to customize it.")
            
            # Formatted clean Markdown render
            st.markdown(st.session_state.raw_prd)
            
            # Collapsible edit box for human review
            with st.expander("✏️ Edit PRD Draft (Human Review & Override)", expanded=False):
                edited_prd = st.text_area("Modify PRD Content:", value=st.session_state.raw_prd, height=300)
                if st.button("💾 Save Edits"):
                    st.session_state.raw_prd = edited_prd
                    st.success("Edits saved!")
                    st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("✅ Approve & Add to Backlog"):
                st.success("PRD Approved! Synced to backlog with evidence attached.")
                st.balloons()
                st.session_state.show_prd_approval = False

# MODULE 2: RICE CALCULATOR
elif app_mode == "RICE":
    st.subheader("📊 RICE Prioritization & Risk Assessment Engine")
    st.caption("Quantify feature ROI, evaluate strategic trade-offs, and receive AI-backed execution guidance.")
    
    col_inputs, col_dashboard = st.columns([1, 1.3])
    
    with col_inputs:
        st.markdown("### 1. Matrix Inputs")
        feature_name = st.text_input("Feature Title", "AI Automated Invoice Scanner")
        reach = st.number_input("Reach (Users impacted / quarter)", min_value=0, value=5000, step=500)
        impact = st.select_slider(
            "Impact Scale Factor", 
            options=[0.25, 0.5, 1.0, 2.0, 3.0], value=2.0, 
            format_func=lambda x: {0.25: "0.25 (Minimal)", 0.5: "0.5 (Low)", 1.0: "1.0 (Medium)", 2.0: "2.0 (High)", 3.0: "3.0 (Massive)"}[x]
        )
        confidence = st.slider("Confidence Rating (%)", min_value=10, max_value=100, value=80, step=10)
        effort = st.number_input("Effort (Person-Months)", min_value=0.5, value=1.5, step=0.5)
        
        compute_btn = st.button("📊 Calculate Score & Run AI Diagnostics")

    with col_dashboard:
        st.markdown("### 2. Strategic Diagnostics & Score")
        
        if compute_btn:
            raw_score = ai_engine.calculate_rice_score(reach, impact, confidence, effort)
            
            kpi_col1, kpi_col2 = st.columns(2)
            with kpi_col1:
                st.metric(label="RICE Score", value=f"{raw_score:,.1f}")
            with kpi_col2:
                if raw_score >= 2000:
                    st.markdown("### Status: 🔥 **P0 Priority**")
                elif raw_score >= 800:
                    st.markdown("### Status: ⚡ **P1 Priority**")
                else:
                    st.markdown("### Status: 🧊 **P2 Priority**")

            st.markdown("---")
            st.markdown("#### 📐 Mathematical Breakdown")
            st.latex(r"\text{RICE Score} = \frac{\text{Reach} \times \text{Impact} \times \text{Confidence}}{\text{Effort}}")
            st.code(f"({reach:,} Reach  ×  {impact}x Impact  ×  {confidence}% Confidence)  /  {effort} Person-Months  =  {raw_score:,.1f}", language="text")

            st.markdown("#### ⚡ Value vs. Cost Balance")
            total_value = reach * impact * (confidence / 100)
            st.progress(min(int((total_value / 10000) * 100), 100))
            st.progress(min(int((effort / 10) * 100), 100))

            st.markdown("---")
            st.markdown("#### 🤖 AI Strategic Interpretation")
            with st.spinner("✨ Gemini AI evaluating feature tradeoffs..."):
                explanation = ai_engine.explain_rice_score(feature_name, reach, impact, confidence, effort, raw_score)
            st.write_stream(stream_text_with_cursor(explanation))
            
            st.markdown("---")
            st.markdown("#### 👤 PM Decision Record")
            pm_notes = st.text_input("Add your justification or override notes here:")
            if st.button("🔒 Lock Score & Approve"):
                st.success(f"Score of {raw_score:,.1f} locked by Product Manager. Added to Roadmap.")
        else:
            st.info("👈 Set your metrics on the left and click **'Calculate Score & Run AI Diagnostics'**")

# MODULE 3: CUSTOMER FEEDBACK HUB
elif app_mode == "FEEDBACK":
    st.subheader("💬 Customer Feedback Intelligence Engine")
    st.caption("Extract actionable feature requests and sentiment trends from raw customer reviews.")
    
    col_f_in, col_f_out = st.columns([1, 1.2])
    
    with col_f_in:
        st.markdown("### 1. Raw Feedback Stream")
        
        if "feedback_input_text" not in st.session_state:
            st.session_state.feedback_input_text = ""
            
        if st.button("📋 Load Sample Customer Reviews Dataset"):
            st.session_state.feedback_input_text = "\n".join([
                "1. App crashes on PDF export.",
                "2. Need dark mode ASAP.",
                "3. Too expensive for small teams.",
                "4. PDF export broken on iOS devices.",
                "5. Love the UI! Super clean design.",
                "6. Can't reset password from login screen.",
                "7. Add Google SSO please.",
                "8. Exporting reports freezes my phone.",
                "9. Great customer support team.",
                "10. Dark mode would save my eyes at night.",
                "11. Billing page is confusing.",
                "12. Cannot download PDF summaries.",
                "13. Fast and responsive web app.",
                "14. Add Apple sign-in option.",
                "15. PDF generation fails with error 500.",
                "16. Dashboard is too bright at night.",
                "17. The new layout is amazing.",
                "18. I keep getting logged out randomly.",
                "19. Why does PDF export take 5 minutes?",
                "20. Need SSO integration for enterprise.",
                "21. Invoice scanner works perfectly.",
                "22. Please implement a dark theme.",
                "23. App hangs on the reports page.",
                "24. PDF export button does nothing.",
                "25. Very clean and intuitive interface.",
                "26. Wish there was a black background option.",
                "27. Microsoft login integration needed.",
                "28. Reports export is completely broken.",
                "29. Fast loading times across pages.",
                "30. Dark mode is standard now, please add it!"
            ])
            
        feedback_input = st.text_area(
            "Paste Raw Reviews / Survey Text:", 
            value=st.session_state.feedback_input_text,
            height=200, 
            placeholder="Paste 5 to 50 raw customer reviews..."
        )
        st.session_state.feedback_input_text = feedback_input
        
        sum_btn = st.button("🔍 Extract Sentiment & Action Items")

    with col_f_out:
        st.markdown("### 2. Executive Insights Summary")
        if sum_btn:
            cleaned_text = feedback_input.strip()
            if cleaned_text:
                with st.spinner("✨ Gemini AI scanning reviews and synthesizing feedback..."):
                    summary_result = ai_engine.summarize_feedback(cleaned_text)
                st.write_stream(stream_text_with_cursor(summary_result))
            else:
                st.toast("Please paste some raw reviews or click 'Load Sample Reviews' first.", icon="⚠️")
        else:
            st.info("👈 Paste customer comments or load the sample dataset on the left to run sentiment analysis.")