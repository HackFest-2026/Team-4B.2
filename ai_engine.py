import os
from dotenv import load_dotenv
from google import genai

# 1. Load API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("WARNING: API Key not found. Please check your .env file.")

# 2. Initialize Gemini Client
client = genai.Client(api_key=api_key)

def generate_prd(feature_idea):
    """Takes a simple feature idea and returns a clean, structured PRD."""
    prompt = f"""
    Act as a Principal Product Manager at a top tech company.
    Write a clear, detailed, and accurate Product Requirements Document (PRD) for the following feature.
    Avoid all fluff. Do NOT stack triple asterisks (***). Use standard, clean Markdown formatting.

    Feature Brief: {feature_idea}

    Use exactly these headings:
    ## 1. Overview
    Write a concise 2-sentence executive summary.

    ## 2. Problem Statement
    Define the exact user pain point clearly.

    ## 3. Goals & Success Metrics
    List 1 business goal and 3 specific KPIs.

    ## 4. User Stories
    Provide 3 realistic agile user stories in standard format ("As a [user], I want to [action] so that [benefit]").

    ## 5. Technical & UX Requirements
    List specific technical constraints, edge cases, and UX rules using clean bullet points.
    """
    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Error connecting to AI: {e}"


def summarize_feedback(feedback_text):
    """Analyzes customer reviews and extracts key themes using Gemini."""
    prompt = f"""
    Act as an Executive Product Manager. 
    Analyze the following customer feedback and provide a clear, zero-fluff summary. Use clean Markdown formatting.
    
    Feedback: {feedback_text}
    
    Use exactly these headings:
    ## 1. Overall Sentiment
    Declare sentiment (Positive, Neutral, Negative) with 1 sentence explaining the driver.

    ## 2. Top 3 Themes
    List the top 3 patterns using bold bullet points.

    ## 3. Recommended PM Action Plan
    Provide 3 concrete engineering or product steps to take immediately.
    """
    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=prompt,
        )
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
    Explain what a score of {score} means for release planning in 2 sentences.

    ## 2. Risk & Value Trade-Off Analysis
    Explain how Effort ({effort} person-months) balances against Confidence ({confidence}%).

    ## 3. Optimization Recommendation
    Suggest 1 practical way to lower effort or increase confidence.
    """
    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Error connecting to AI: {e}"


def calculate_rice_score(reach, impact, confidence, effort):
    """Calculates RICE priority score using pure math."""
    if effort == 0:
        return 0.0
    return (float(reach) * float(impact) * (float(confidence) / 100.0)) / float(effort)