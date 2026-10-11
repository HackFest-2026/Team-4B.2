import streamlit as st
import ai_engine

st.set_page_config(page_title="AI PM Copilot", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #0a0a0a;
        background-image: 
            radial-gradient(circle at 15% 30%, rgba(97, 247, 93, 0.04) 0%, transparent 35%),
            radial-gradient(circle at 85% 70%, rgba(255, 255, 255, 0.02) 0%, transparent 35%),
            url("data:image/svg+xml,%3Csvg xmlns='[http://www.w3.org/2000/svg](http://www.w3.org/2000/svg)' width='120' height='120' opacity='0.02'%3E%3Crect width='120' height='120' fill='none'/%3E%3Cpath d='M30 30h60v60H30z' stroke='%23ffffff' stroke-width='1.5' fill='none'/%3E%3Cpath d='M30 60h60M60 30v60' stroke='%23ffffff' stroke-width='0.5' fill='none' stroke-dasharray='4,4'/%3E%3Ccircle cx='60' cy='60' r='4' fill='%23ffffff'/%3E%3Ccircle cx='30' cy='30' r='2' fill='%23ffffff'/%3E%3Ccircle cx='90' cy='90' r='2' fill='%23ffffff'/%3E%3C/svg%3E");
        background-attachment: fixed;
    }
    [data-testid="stSidebar"] {
        background-color: rgba(10, 10, 10, 0.85);
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    [data-testid="stHeader"] {
        background-color: transparent;
    }
    h1, h2, h3, h4, h5, h6, p, label, span {
        color: #e4e4e7 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    div.stButton > button {
        background: rgba(24, 24, 27, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #ffffff !important;
        border-radius: 10px;
        padding: 0.6rem 1.4rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(8px);
        letter-spacing: 0.3px;
    }
    div.stButton > button:hover {
        background: rgba(97, 247, 93, 0.1);
        border: 1px solid #61f75d;
        color: #ffffff !important;
        box-shadow: 0 0 25px rgba(97, 247, 93, 0.15), inset 0 0 10px rgba(97, 247, 93, 0.05);
        transform: translateY(-2px);
    }
    div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea {
        background-color: rgba(18, 18, 18, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: #ffffff;
        border-radius: 10px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    div[data-testid="stTextInput"] input:focus, div[data-testid="stTextArea"] textarea:focus {
        border: 1px solid #61f75d;
        box-shadow: 0 0 15px rgba(97, 247, 93, 0.1);
        background-color: rgba(24, 24, 27, 0.8);
    }
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(24, 24, 27, 0.7), rgba(18, 18, 18, 0.9));
        border-radius: 14px;
        padding: 18px;
        border: 1px solid rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    .rice-formula {
        font-family: 'SF Mono', Consolas, Monaco, monospace;
        color: #a1a1aa;
        background: rgba(18, 18, 18, 0.5);
        padding: 14px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.03);
        text-align: center;
        backdrop-filter: blur(8px);
        font-size: 0.95rem;
        letter-spacing: 0.5px;
    }
    .rice-formula strong {
        color: #61f75d;
        font-size: 1.1rem;
    }
    hr {
        border-color: rgba(255, 255, 255, 0.05);
        margin: 2rem 0;
    }
    </style>
""", unsafe_allow_html=True)

if 'features' not in st.session_state: st.session_state.features = []
if 'selected_feature' not in st.session_state: st.session_state.selected_feature = None
if 'generated_prd' not in st.session_state: st.session_state.generated_prd = ""
if 'input_product' not in st.session_state: st.session_state.input_product = ""
if 'input_feedback' not in st.session_state: st.session_state.input_feedback = ""
if 'legacy_prd' not in st.session_state: st.session_state.legacy_prd = ""
if 'legacy_feedback_result' not in st.session_state: st.session_state.legacy_feedback_result = ""
if 'legacy_rice_analysis' not in st.session_state: st.session_state.legacy_rice_analysis = ""

col_title, col_toggle = st.columns([0.85, 0.15])
with col_title:
    st.title("AI PM Copilot")
with col_toggle:
    st.write("") 
    legacy_mode = st.toggle("Switch to Legacy UI")

if not legacy_mode:
    st.markdown("### Feedback to Feature")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.input_product = st.text_input("Product Context", placeholder="Enter your product description...", value=st.session_state.input_product)
        if st.button("Generate 20 Sample Feedbacks"):
            if not st.session_state.input_product:
                st.warning("Please enter a Product Context first to generate related reviews.")
            else:
                with st.spinner("Generating diverse reviews based on your product..."):
                    st.session_state.input_feedback = ai_engine.generate_sample_feedback(st.session_state.input_product)
                    st.rerun()

    with col2:
        st.session_state.input_feedback = st.text_area("Customer Feedback", placeholder="Feedback will appear here...", value=st.session_state.input_feedback, height=200)

    if st.button("Analyze Feedback & Prioritize Features"):
        if not st.session_state.input_product or not st.session_state.input_feedback:
            st.warning("Please provide both Product Context and Customer Feedback.")
        else:
            with st.spinner("Analyzing feedback and calculating RICE scores..."):
                result = ai_engine.process_feedback_to_features(st.session_state.input_product, st.session_state.input_feedback)
                if "error" in result:
                    st.error(f"Error: {result['error']}")
                else:
                    st.session_state.features = result
                    st.session_state.selected_feature = None
                    st.session_state.generated_prd = ""

    if st.session_state.features:
        st.divider()
        st.markdown("### AI RICE Prioritization Engine")
        
        for i, feature in enumerate(st.session_state.features):
            with st.container():
                st.subheader(f"{feature.get('feature_name', 'Feature')}")
                st.write(f"**Context:** {feature.get('description', '')}")
                st.write(f"**AI Justification:** {feature.get('justification', '')}")
                
                r = feature.get('reach', 0)
                i_val = feature.get('impact', 0)
                c = feature.get('confidence', 0)
                e = feature.get('effort', 0)
                total = feature.get('rice_score', 0)

                m1, m2, m3, m4, m5 = st.columns(5)
                m1.metric("Reach", r)
                m2.metric("Impact", i_val)
                m3.metric("Confidence", f"{c}%")
                m4.metric("Effort", e)
                m5.metric("Total RICE", total)
                
                st.markdown(f'<div class="rice-formula">Formula: (Reach: {r} × Impact: {i_val} × Confidence: {c}%) ÷ Effort: {e} = <strong>{total}</strong></div>', unsafe_allow_html=True)
                st.write("") 
                
                if st.button(f"Generate PRD for '{feature.get('feature_name')}'", key=f"btn_{i}"):
                    st.session_state.selected_feature = feature
                    with st.spinner("Drafting PRD..."):
                        prd = ai_engine.generate_prd_from_feature(st.session_state.input_product, feature)
                        st.session_state.generated_prd = prd
                st.write("---")

    if st.session_state.generated_prd:
        st.divider()
        st.markdown("### PRD Studio")
        edited_prd = st.text_area("Edit PRD:", value=st.session_state.generated_prd, height=500)
        with st.expander("Preview Markdown", expanded=True):
            st.markdown(edited_prd)

else:
    st.sidebar.markdown("### Workspace Modules")
    module_selection = st.sidebar.radio("Select Module:", ["PRD Studio", "RICE Prioritization", "Customer Feedback"])
    
    if module_selection == "PRD Studio":
        st.markdown("### PRD Studio")
        feature_idea = st.text_input("Enter Feature Brief:")
        if st.button("Generate PRD"):
            with st.spinner("Generating..."):
                st.session_state.legacy_prd = ai_engine.generate_prd_legacy(feature_idea)
        
        if st.session_state.legacy_prd:
            st.text_area("Generated PRD:", value=st.session_state.legacy_prd, height=400)
            st.markdown(st.session_state.legacy_prd)

    elif module_selection == "RICE Prioritization":
        st.markdown("### RICE Prioritization Engine")
        feature_name = st.text_input("Feature Name:")
        col1, col2, col3, col4 = st.columns(4)
        with col1: reach = st.number_input("Reach", min_value=0, value=500)
        with col2: impact = st.number_input("Impact", min_value=0.0, value=2.0)
        with col3: confidence = st.number_input("Confidence (%)", min_value=0, value=80)
        with col4: effort = st.number_input("Effort", min_value=1, value=1)
        
        if st.button("Calculate Score"):
            score = ai_engine.calculate_rice_score_legacy(reach, impact, confidence, effort)
            st.success(f"Final RICE Score: {score}")
            with st.spinner("Fetching Interpretation..."):
                st.session_state.legacy_rice_analysis = ai_engine.generate_rice_analysis_legacy(feature_name, score)
            st.info(st.session_state.legacy_rice_analysis)

    elif module_selection == "Customer Feedback":
        st.markdown("### Customer Feedback Hub")
        st.session_state.input_product = st.text_input("Product Context for Samples", placeholder="Enter product name...", value=st.session_state.input_product)
        if st.button("Generate 20 Sample Feedbacks", key="legacy_sample_btn"):
            if not st.session_state.input_product:
                st.warning("Please enter a Product Context first.")
            else:
                with st.spinner("Generating diverse reviews..."):
                    st.session_state.input_feedback = ai_engine.generate_sample_feedback(st.session_state.input_product)
                    st.rerun()
            
        feedback_input = st.text_area("Enter Customer Feedback:", value=st.session_state.input_feedback, height=200)
        
        if st.button("Analyze Sentiment"):
            with st.spinner("Analyzing..."):
                st.session_state.legacy_feedback_result = ai_engine.analyze_feedback_legacy(feedback_input)
        
        if st.session_state.legacy_feedback_result:
            st.markdown(st.session_state.legacy_feedback_result)