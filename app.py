# app.py
import streamlit as st
import yaml
import google.generativeai as genai
import time
import re

def load_config():
    """Load configuration from config.yaml"""
    try:
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        raise Exception("config.yaml file not found. Create one with your Gemini API key.")

def initialize_gemini(config):
    """Initialize Gemini model with API key"""
    genai.configure(api_key=config['gemini']['api_key'])
    return genai.GenerativeModel(config['gemini']['model_name'])

# Load configuration
config = load_config()

# Initialize Gemini
model = initialize_gemini(config)

# System prompt template for NyayaBot (Legal Analysis)
SYSTEM_PROMPT = """
Role: You are "NyayaBot," an AI legal assistant specializing in Indian law compliance. Your task is to analyze user scenarios, explain legal implications with references, and suggest ethical alternatives. Prioritize accuracy, clarity, and explainability in your responses.

Response Format:
-----------------------------------------
**NyayaBot Response**

🔍 **Verdict:**  
[Insert Verdict: ✅ Legal / ❌ Illegal / ⚠️ Conditional]

📜 **Relevant Laws:**  
- [List the relevant legal provisions as bullet points.]

📖 **Explanation:**  
1. **[Point 1 Title]:**  
   - **Action:** [Explanation of the action.]  
   - **Relevant Law:** [Reference to the law and section.]  
   - **Case Reference:** [Case law reference if applicable.]

2. **[Point 2 Title]:**  
   - **Action:** [Explanation of the action.]  
   - **Relevant Law:** [Reference to the law and section.]  
   - **Outcome:** [Legal outcome of the action.]

🛡️ **Legal Advice (Actionable Alternatives):**  
- ✅ **Alternative 1:** [Description of the alternative.]  
- ✅ **Alternative 2:** [Description of the alternative.]  
- ✅ **Alternative 3:** [Description of the alternative.]

🚨 **Warning:**  
**[If illegal, include a bold red-flag message describing the legal risks.]**

### **XAI-Driven Reasoning (Chain-of-Thought Explanation):**

"I arrived at this conclusion by analyzing the key legal provisions that regulate the privacy of electronic communications in India. First, I identified that recording a call without consent directly conflicts with the provisions of the Indian Telegraph Act (Section 5), which restricts unauthorized interception. Then, I mapped this to the IT Act 66E, which explicitly penalizes privacy violations in digital communications. I also considered the possibility of defamation under IPC Section 500 if the uploaded content harms someone’s reputation. The absence of a standalone data privacy law in India means these laws collectively govern privacy-related offenses. This layered analysis ensures that the legal implications are thoroughly considered, leading to the final verdict that uploading such a recording without consent is illegal."
-----------------------------------------
"""

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def parse_gemini_response(response):
    """Parse structured response from Gemini output using regex for NyayaBot legal analysis"""
    parsed = {
        'Verdict': '',
        'Relevant Laws': '',
        'Explanation': '',
        'Legal Advice': '',
        'Warning': '',
        'XAI-Driven Reasoning': ''
    }
    # Attempt to split the response into sections using the delimiter
    sections = re.split(r'-----------------------------------------', response)
    if len(sections) >= 3:
        content = sections[1].strip()
        # Extract sections by matching the markdown headers
        verdict_match = re.search(r'🔍 \*\*Verdict:\*\*\s*(.*)', content)
        parsed['Verdict'] = verdict_match.group(1).strip() if verdict_match else ""

        relevant_laws_match = re.search(r'📜 \*\*Relevant Laws:\*\*\s*(.*?)\n\n', content, re.DOTALL)
        parsed['Relevant Laws'] = relevant_laws_match.group(1).strip() if relevant_laws_match else ""

        explanation_match = re.search(r'📖 \*\*Explanation:\*\*\s*(.*?)\n\n', content, re.DOTALL)
        parsed['Explanation'] = explanation_match.group(1).strip() if explanation_match else ""

        legal_advice_match = re.search(r'🛡️ \*\*Legal Advice \(Actionable Alternatives\):\*\*\s*(.*?)\n\n', content, re.DOTALL)
        parsed['Legal Advice'] = legal_advice_match.group(1).strip() if legal_advice_match else ""

        warning_match = re.search(r'🚨 \*\*Warning:\*\*\s*(.*?)\n\n', content, re.DOTALL)
        parsed['Warning'] = warning_match.group(1).strip() if warning_match else ""

        xai_match = re.search(r'### \*\*XAI-Driven Reasoning \(Chain-of-Thought Explanation\):\*\*\s*(.*?)$', content, re.DOTALL)
        parsed['XAI-Driven Reasoning'] = xai_match.group(1).strip() if xai_match else ""
    else:
        # Fallback: if parsing fails, return the entire response as Explanation.
        parsed['Explanation'] = response
    return parsed

def generate_response(user_input):
    """Generate and parse Gemini response for legal analysis"""
    full_prompt = f"{SYSTEM_PROMPT}\nUser Query: {user_input}"
    try:
        response = model.generate_content(full_prompt)
        parsed = parse_gemini_response(response.text)
        return parsed, response.text
    except Exception as e:
        return {"error": f"API Error: {str(e)}"}, ""

# Streamlit UI
st.title("NyayaBot: Indian Law Compliance Assistant")
st.caption("Analyze legal scenarios and receive detailed legal analysis based on Indian law.")

user_input = st.chat_input("Enter your legal scenario (e.g., recording a call without consent and uploading it):")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process new input
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.spinner("Analyzing legal implications..."):
        ai_response, full_response = generate_response(user_input)
        time.sleep(0.5)
    if 'error' in ai_response:
        with st.chat_message("assistant"):
            st.error(ai_response['error'])
    else:
        with st.chat_message("assistant"):
            st.markdown(full_response)
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": full_response
    })
