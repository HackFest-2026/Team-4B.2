import streamlit as st
import time
import ai_engine

# 1. Page Configuration (Configured to keep sidebar expanded and menu controls visible)
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
    
    /* Top Banner Bar */
    .top-header {
        background: linear-gradient(90deg, rgba(99, 102, 241, 0.15) 0%, rgba(168, 85, 247, 0.15) 100%);
        border: 1px solid rgba(168, 85, 247, 0.3);
        padding: 16px 24px;
        border-radius: 12px;
        margin-bottom: 24px;
    }
    
    /* Stat Cards */
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

    /* Buttons */
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
    
    /* Clean up footer while preserving header menu controls */
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Helper: Simulated Typing Generator
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
    st.markdown('<div class="stat-card"><div class="stat-number">1,240+</div><div class="stat-label">PRDs Generated</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="stat-card"><div class="stat-number">98.4%</div><div class="stat-label">Time Saved / Doc</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="stat-card"><div class="stat-number">4.2k</div><div class="stat-label">Reviews Scanned</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown('<div class="stat-card"><div class="stat-number">Gemini 3.5 Lite</div><div class="stat-label">Active Neural Model</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- NAVIGATION SIDEBAR ---
st.sidebar.title("🛠️ PM Tool Suite")
menu_selection = st.sidebar.radio(
    "Select Workspace Module:", 
    ["📝 PRD Studio", "📊 RICE Prioritization Engine", "💬 Customer Feedback Hub"]
)

# Workspace State Routing
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
        preset_prompt = ""
        if preset_cols[0].button("⚡ Google SSO"):
            preset_prompt = "One-click OAuth Google Sign-In button for mobile e-commerce checkout"
        if preset_cols[1].button("🌙 Dark Mode"):
            preset_prompt = "System-wide dark mode theme toggle with schedule options"
            
        feature_idea = st.text_area(
            "Feature Description Brief:", 
            value=preset_prompt if preset_prompt else "",
            height=160,
            placeholder="e.g., An automated email digest sent every Monday summarizing team task progress..."
        )
        
        generate_btn = st.button("🚀 Generate PRD Specification")

    with col_output:
        st.markdown("### 2. Generated Specification")
        if generate_btn:
            cleaned_input = feature_idea.strip()
            if len(cleaned_input) >= 3:
                with st.spinner("✨ Gemini AI analyzing requirements and drafting PRD..."):
                    raw_prd = ai_engine.generate_prd(cleaned_input)
                st.write_stream(stream_text_with_cursor(raw_prd))
            else:
                st.toast("Please enter a feature description briefly first.", icon="⚠️")
        else:
            st.info("👈 Enter a feature brief on the left or select a quick preset to generate the document.")

# MODULE 2: RICE CALCULATOR (ENTERPRISE DASHBOARD)
elif app_mode == "RICE":
    st.subheader("📊 RICE Prioritization & Risk Assessment Engine")
    st.caption("Quantify feature ROI, evaluate strategic trade-offs, and receive AI-backed execution guidance.")
    
    col_inputs, col_dashboard = st.columns([1, 1.3])
    
    with col_inputs:
        st.markdown("### 1. Matrix Inputs")
        feature_name = st.text_input("Feature Title", "AI Automated Invoice Scanner")
        
        reach = st.number_input(
            "Reach (Users impacted / quarter)", 
            min_value=0, value=5000, step=500,
            help="Total unique users expected to use this feature."
        )
        
        impact = st.select_slider(
            "Impact Scale Factor", 
            options=[0.25, 0.5, 1.0, 2.0, 3.0], value=2.0, 
            format_func=lambda x: {
                0.25: "0.25 (Minimal)", 
                0.5: "0.5 (Low)", 
                1.0: "1.0 (Medium)", 
                2.0: "2.0 (High)", 
                3.0: "3.0 (Massive)"
            }[x],
            help="How much this feature will improve conversion or retention for each user."
        )
        
        confidence = st.slider(
            "Confidence Rating (%)", 
            min_value=10, max_value=100, value=80, step=10,
            help="High = backed by user research; Low = pure intuition."
        )
        
        effort = st.number_input(
            "Effort (Person-Months)", 
            min_value=0.5, value=1.5, step=0.5,
            help="Total engineer/designer months required to ship."
        )
        
        compute_btn = st.button("📊 Calculate Score & Run AI Diagnostics")

    with col_dashboard:
        st.markdown("### 2. Strategic Diagnostics & Score")
        
        if compute_btn:
            # 1. Compute Numerical Score
            raw_score = ai_engine.calculate_rice_score(reach, impact, confidence, effort)
            
            # 2. Display KPI Cards Side-by-Side
            kpi_col1, kpi_col2 = st.columns(2)
            with kpi_col1:
                st.metric(label="RICE Score", value=f"{raw_score:,.1f}")
            with kpi_col2:
                if raw_score >= 2000:
                    st.markdown("### Status: 🔥 **P0 Priority**")
                    st.caption("Immediate Roadmap Candidate")
                elif raw_score >= 800:
                    st.markdown("### Status: ⚡ **P1 Priority**")
                    st.caption("Secondary Release Cycle")
                else:
                    st.markdown("### Status: 🧊 **P2 Priority**")
                    st.caption("Low Return / High Cost")

            # 3. Mathematical Formula Visual Breakdown
            st.markdown("---")
            st.markdown("#### 📐 Mathematical Breakdown")
            st.latex(r"\text{RICE Score} = \frac{\text{Reach} \times \text{Impact} \times \text{Confidence}}{\text{Effort}}")
            st.code(
                f"({reach:,} Reach  ×  {impact}x Impact  ×  {confidence}% Confidence)  /  {effort} Person-Months  =  {raw_score:,.1f}", 
                language="text"
            )

            # 4. Value vs. Cost Bar Telemetry
            st.markdown("#### ⚡ Value vs. Cost Balance")
            total_value = reach * impact * (confidence / 100)
            st.write(f"**Value Multiplier:** {total_value:,.0f} points")
            st.progress(min(int((total_value / 10000) * 100), 100))
            
            st.write(f"**Resource Cost (Effort):** {effort} months")
            st.progress(min(int((effort / 10) * 100), 100))

            # 5. AI Strategic Interpretation
            st.markdown("---")
            st.markdown("#### 🤖 AI Strategic Interpretation")
            with st.spinner("✨ Gemini AI evaluating feature tradeoffs..."):
                explanation = ai_engine.explain_rice_score(feature_name, reach, impact, confidence, effort, raw_score)
            st.write_stream(stream_text_with_cursor(explanation))
            
        else:
            st.info("👈 Set your metrics on the left and click **'Calculate Score & Run AI Diagnostics'** to view the full prioritization matrix.")

# MODULE 3: CUSTOMER FEEDBACK HUB
elif app_mode == "FEEDBACK":
    st.subheader("💬 Customer Feedback Intelligence Engine")
    st.caption("Extract actionable feature requests and sentiment trends from raw customer reviews.")
    
    col_f_in, col_f_out = st.columns([1, 1.2])
    
    with col_f_in:
        st.markdown("### 1. Raw Feedback Stream")
        
        if st.button("📋 Load Sample Customer Reviews Dataset"):
            sample_data = "1. App crashes whenever I try to export reports to PDF.\n2. We desperately need dark mode, my eyes hurt at night.\n3. The pricing is too high for small teams.\n4. Love the new dashboard layout! Super clean.\n5. PDF export is broken on iOS devices."
        else:
            sample_data = ""
            
        feedback_input = st.text_area(
            "Paste Raw Reviews / Survey Text:", 
            value=sample_data if sample_data else "",
            height=200, 
            placeholder="Paste 5 to 50 raw customer reviews..."
        )
        
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