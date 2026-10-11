from google import genai
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

MODEL_NAME = 'gemini-3.5-flash-lite' 

def clean_json_response(raw_text):
    raw_text = raw_text.strip()
    if raw_text.startswith("```json"):
        raw_text = raw_text[7:]
    if raw_text.startswith("```"):
        raw_text = raw_text[3:]
    if raw_text.endswith("```"):
        raw_text = raw_text[:-3]
    return raw_text.strip()

def process_feedback_to_features(product_context, customer_feedback):
    prompt = f"""
    You are an Expert Product Manager. 
    Product Context: {product_context}
    Raw Customer Feedback: {customer_feedback}
    
    Task: Analyze the feedback and extract the top 1 to 3 actionable feature requests.
    For each feature, output the estimated RICE variables based on the feedback context:
    - Reach (1-1000 users affected)
    - Impact (3=Massive, 2=High, 1=Medium, 0.25=Low)
    - Confidence (0-100 based on how clear the feedback is)
    - Effort (1-5 person-months)
    
    Output STRICTLY in this JSON array format, nothing else:
    [
        {{
            "feature_name": "Name of feature",
            "description": "Brief description based on feedback",
            "reach": 500,
            "impact": 2,
            "confidence": 80,
            "effort": 1,
            "justification": "Why this RICE score was given based on the feedback"
        }}
    ]
    """
    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        cleaned_json = clean_json_response(response.text)
        features = json.loads(cleaned_json)
        
        for feature in features:
            reach = float(feature.get('reach', 0))
            impact = float(feature.get('impact', 0))
            confidence = float(feature.get('confidence', 0))
            effort = float(feature.get('effort', 1))
            if effort == 0:
                effort = 0.1 
            feature['rice_score'] = round((reach * impact * (confidence / 100.0)) / effort, 2)
            
        return features
    except Exception as e:
        return {"error": str(e)}

def generate_prd_from_feature(product_context, feature_data):
    prompt = f"""
    Act as an Expert Product Manager. Write a structured Product Requirement Document (PRD) 
    for the following feature, which belongs to the product: {product_context}.
    
    Feature Name: {feature_data.get('feature_name', '')}
    Description: {feature_data.get('description', '')}
    Business Justification: {feature_data.get('justification', '')}
    
    Format the output in strict Markdown with these sections:
    1. Overview & Problem Statement
    2. Target Audience
    3. Proposed Solution & User Story
    4. Scope (In-Scope & Out-of-Scope)
    5. Success Metrics (KPIs)
    """
    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        return response.text
    except Exception as e:
        return f"Error connecting to AI: {str(e)}"

def generate_sample_feedback(product_context):
    prompt = f"""
    Generate exactly 20 diverse, realistic customer reviews for the following product: {product_context}.
    Include a mix of positive feedback, negative complaints, bug reports, and feature requests.
    Output ONLY the reviews as a numbered list from 1 to 20, with no introductory or concluding text.
    """
    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        return response.text
    except Exception as e:
        return f"Error connecting to AI: {str(e)}"

def generate_prd_legacy(feature_idea):
    prompt = f"Act as an Expert Product Manager. Write a structured PRD for: {feature_idea}"
    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        return response.text
    except Exception as e:
        return f"Error connecting to AI: {str(e)}"

def calculate_rice_score_legacy(reach, impact, confidence, effort):
    if effort == 0:
        return 0
    return round((reach * impact * (confidence / 100.0)) / effort, 2)

def analyze_feedback_legacy(feedback):
    prompt = f"Analyze this customer feedback. Extract the overall sentiment and top 3 key themes: {feedback}"
    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        return response.text
    except Exception as e:
        return f"Error connecting to AI: {str(e)}"

def generate_rice_analysis_legacy(feature_name, score):
    prompt = f"Provide a brief 2-sentence strategic interpretation for feature '{feature_name}' with a RICE score of {score}."
    for attempt in range(3):
        try:
            response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
            return response.text
        except Exception as e:
            if attempt == 2:
                return f"Unable to reach AI service. (Details: {e})"
            time.sleep(1)

