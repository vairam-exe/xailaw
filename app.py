# app.py
import streamlit as st
import yaml
import google.generativeai as genai
import time
import re

def load_config():
    """Load configuration from config.yaml."""
    try:
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        raise Exception("config.yaml file not found. Create one with your Gemini API key.")

def initialize_gemini(config):
    """Initialize the Gemini model with the provided API key."""
    genai.configure(api_key=config['gemini']['api_key'])
    return genai.GenerativeModel(config['gemini']['model_name'])

# Load configuration
config = load_config()

# Initialize Gemini model
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
    """Parse structured response from Gemini output for NyayaBot legal analysis."""
    parsed = {
        'Verdict': '',
        'Relevant Laws': '',
        'Explanation': '',
        'Legal Advice': '',
        'Warning': '',
        'XAI-Driven Reasoning': ''
    }
    
    # Split the response into sections using the delimiter
    sections = re.split(r'-----------------------------------------', response)
    if len(sections) >= 3:
        content = sections[1].strip()
        
        # Extract sections by matching the markdown headers
        parsed['Verdict'] = extract_section(content, r'🔍 \*\*Verdict:\*\*\s*(.*)')
        parsed['Relevant Laws'] = extract_section(content, r'📜 \*\*Relevant Laws:\*\*\s*(.*?)\n\n', re.DOTALL)
        parsed['Explanation'] = extract_section(content, r'📖 \*\*Explanation:\*\*\s*(.*?)\n\n', re.DOTALL)
        parsed['Legal Advice'] = extract_section(content, r'🛡️ \*\*Legal Advice \(Actionable Alternatives\):\*\*\s*(.*?)\n\n', re.DOTALL)
        parsed['Warning'] = extract_section(content, r'🚨 \*\*Warning:\*\*\s*(.*?)\n\n', re.DOTALL)
        parsed['XAI-Driven Reasoning'] = extract_section(content, r'### \*\*XAI-Driven Reasoning \(Chain-of-Thought Explanation\):\*\*\s*(.*?)$', re.DOTALL)
    else:
        # Fallback: if parsing fails, return the entire response as Explanation.
        parsed['Explanation'] = response
    return parsed

def extract_section(content, pattern, flags=0):
    """Helper function to extract a section from content using regex."""
    match = re.search(pattern, content, flags)
    return match.group(1).strip() if match else ""

def generate_response(user_input):
    """Generate and parse Gemini response for legal analysis."""
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
