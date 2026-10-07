import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

def generate_prd(feature_idea):
    """Takes a simple feature idea and returns a structured PRD."""
    prompt = f"""
    Act as an Expert Product Manager.
    Write a clear, professional, and structured Product Requirements Document (PRD) for the following feature:

    Feature: {feature_idea}

    You MUST output the PRD in Markdown format with these exact headings:
    ## 1. Overview
    ## 2. Problem Statement
    ## 3. Goals & Success Metrics
    ## 4. User Stories
    ## 5. Technical Requirements
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error connecting to AI: {e}"

def summarize_feedback(feedback_text):
    """Analyzes customer reviews and extracts key themes using Gemini."""
    prompt = f"""
    Act as an Expert Product Manager. 
    Analyze the following customer feedback and provide a structured summary.
    
    Feedback: {feedback_text}
    
    Format the output in Markdown with these exact headings:
    ## 1. Overall Sentiment (Positive, Neutral, Negative)
    ## 2. Top 3 Themes or Requests
    ## 3. Recommended PM Action
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error connecting to AI: {e}"

def explain_rice_score(feature_name, reach, impact, confidence, effort, score):
    """Provides a PM consulting breakdown of what the computed RICE score means."""
    prompt = f"""
    Act as a Principal Product Strategist. 
    Analyze the following RICE prioritization results for a feature:
    - Feature Name: {feature_name}
    - Reach: {reach} users/month
    - Impact Multiple: {impact}x
    - Confidence Rating: {confidence}%
    - Development Effort: {effort} person-months
    - Computed RICE Score: {score}

    Provide a concise strategic breakdown with these headings:
    ## 1. Executive Verdict
    (Explain what a score of {score} means for release planning in 2 sentences)

    ## 2. Risk & Value Trade-Off Analysis
    (Explain how the Effort of {effort} person-months balances against the {confidence}% Confidence level)

    ## 3. Optimization Recommendation
    (Suggest 1 practical way to lower effort or increase confidence)
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error connecting to AI: {e}"

def calculate_rice_score(reach, impact, confidence, effort):
    """Calculates RICE priority score using pure math."""
    if effort == 0:
        return 0.0
    return (float(reach) * float(impact) * (float(confidence) / 100.0)) / float(effort)
