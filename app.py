import streamlit as st
import json

# Import functions from our newly created modular files
from chatbot import SYSTEM_PROMPT, get_chat_response, extract_candidate_data
from data_handler import anonymize_data, save_to_mock_db

# --- INITIALIZATION & CONFIGURATION ---
st.set_page_config(page_title="TalentScout AI Assistant", page_icon="🤖")

# --- SESSION STATE MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # Get initial greeting from chatbot.py
    initial_greeting = get_chat_response(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": initial_greeting})

# --- UI RENDERING ---
st.title("🤖 TalentScout Hiring Assistant")
st.markdown("Welcome! I am here to help you kickstart your application process.")
st.divider()

# --- SIDEBAR FOR GDPR BACKEND SIMULATION ---
with st.sidebar:
    st.header("Admin / Backend Panel")
    st.write("This simulates the backend process securely extracting and saving candidate data.")
    
    if st.button("End Chat & Save Data"):
        with st.spinner("Extracting and Anonymizing Data..."):
            # Get the raw JSON string from chatbot.py
            raw_json_string = extract_candidate_data(st.session_state.messages)
            
            try:
                # Clean up the output in case the LLM added formatting
                raw_json_string = raw_json_string.replace('```json', '').replace('```', '').strip()
                extracted_data = json.loads(raw_json_string)
                
                # Anonymize and save using data_handler.py
                secure_data = anonymize_data(extracted_data)
                save_to_mock_db(secure_data)
                
                st.success("✅ Data securely anonymized and saved to mock_database.json!")
                st.json(secure_data) # Show the admin what was saved
            except Exception as e:
                st.error(f"Failed to parse data: {e}. Please ensure the interview is complete.")

# Display chat messages from history
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- CHAT INPUT & LOGIC ---
if prompt := st.chat_input("Type your message here..."):
    # 1. Show user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Check for exit keywords
    exit_keywords = ["quit", "exit", "bye", "stop"]
    if any(keyword in prompt.lower() for keyword in exit_keywords):
        with st.chat_message("assistant"):
            st.markdown("Thank you for your time. Your session has ended. You may close this window.")
        st.stop()

    # 3. Get AI response from chatbot.py
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = get_chat_response(st.session_state.messages)
        message_placeholder.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    

