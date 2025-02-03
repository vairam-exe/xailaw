import streamlit as st
import yaml
import requests

# --- Load Gemini API configuration from a YAML file ---
def load_config(config_path="config.yaml"):
    """
    Loads configuration data (such as Gemini API key) from a YAML file.
    """
    try:
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        st.error(f"Error loading configuration: {e}")
        return {}

config = load_config()
gemini_api_key = config.get("gemini_api_key")
if not gemini_api_key:
    st.error("Gemini API key not found in configuration file.")
    st.stop()

# --- Function to call the Gemini API ---
def call_gemini_api(query_text):
    """
    Calls the Gemini API with the provided query_text.
    Replace the URL and parameters below with those appropriate for your Gemini API.
    """
    url = "https://api.gemini.example/analyze"  # Replace with actual Gemini API endpoint
    headers = {
        "Authorization": f"Bearer {gemini_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": query_text,
        "max_tokens": 1024  # Adjust parameters as needed
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        # Assume the API returns a JSON with a field 'result' containing the analysis text.
        result = response.json().get("result", "")
        return result
    except requests.exceptions.RequestException as e:
        st.error(f"Error calling Gemini API: {e}")
        return ""

# --- Streamlit Interface ---
st.title("NyayaBot Legal Analysis")
st.write("Enter the legal scenario query below. The bot will analyze the query and output a structured legal analysis based on Indian law.")

# Input area for the legal scenario query
user_query = st.text_area("Enter your legal query scenario:", height=200)

if st.button("Analyze"):
    if not user_query.strip():
        st.warning("Please enter a legal query scenario.")
    else:
        # Construct the prompt for the Gemini API including instructions for output formatting.
        # This prompt includes the detailed format structure required.
        full_prompt = f"""
Role: You are "NyayaBot," an AI legal assistant specializing in Indian law compliance. Your task is to analyze user scenarios, explain legal implications with references, and suggest ethical alternatives. Prioritize accuracy, clarity, and explainability in your responses.

Please produce the output exactly in the following structure:

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

User Query: "{user_query}"
"""
        # Call the Gemini API with the full prompt.
        api_response = call_gemini_api(full_prompt)
        
        if api_response:
            # Display the output in a text area.
            st.markdown("### **NyayaBot Response**")
            st.text_area("Response", value=api_response, height=600)
        else:
            st.error("No response received from the Gemini API. Please try again later.")
