# 🤖 TalentScout: Intelligent Hiring Assistant

## Project Overview
TalentScout is an intelligent, locally-hosted hiring assistant chatbot designed to streamline the initial candidate screening process for technology recruitment. The chatbot serves as the first point of contact, seamlessly gathering essential candidate details (Name, Email, Experience, Location, etc.) and dynamically generating targeted technical interview questions based strictly on the candidate's declared tech stack. It features a conversational interface, robust fallback mechanisms to handle off-topic inputs, and a simulated backend that strictly adheres to GDPR data privacy standards by anonymizing PII (Personally Identifiable Information) before storage.

## Installation Instructions
Follow these steps to set up and run the application locally on your machine.

### Prerequisites
* **Python 3.9+** installed on your system.
* **Ollama** installed locally (Download from [ollama.com](https://ollama.com/)).

### Step-by-Step Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/AChanikya23/TalentScout-AI-Assistant.git
   cd TalentScout-AI-Assistant

2.  **Download the local Language Model:** Ensure Ollama is running on your machine, then open your terminal and run:
     
    Bash
     
    
        ollama run llama3
        
    
     *(Wait for the download to complete, then type*  `/bye` to exit the Ollama prompt).
     
3.  **Set up a Python Virtual Environment:**
     
    Bash
     
    
        python -m venv myenv
        
        # Activate on Windows:
        myenv\Scripts\activate
        
        # Activate on macOS/Linux:
        source myenv/bin/activate
        
    
4.  **Install required dependencies:**
     
    Bash
     
    
        pip install -r requirements.txt
        
    

## Usage Guide
 

1.  **Start the Chatbot:** With your virtual environment activated, run the following command:
     
    Bash
     
    
        streamlit run app.py
        
    
2.  **Interact:** The application will open in your default web browser. Greet the bot and follow its prompts to provide your details and tech stack.
     
3.  **Technical Screening:** Answer the 3-5 technical questions the bot dynamically generates based on your stack.
     
4.  **End Conversation:** Type "exit", "quit", or "bye" to gracefully end the chat.
     
5.  **Simulate Backend Storage:** Open the sidebar on the left side of the UI and click **"End Chat & Save Data"**. This triggers the backend pipeline to extract your data, anonymize it, and save it to the `mock_database.json` file.
     

## Technical Details
 

*   **Programming Language:** Python 3
     
*   **Libraries Used:** \* `streamlit`: For building the interactive web-based frontend UI.
     
    *   `ollama`: For seamless API connection to the local LLM.
         
    *   `json`, `hashlib`, `os`: For data handling, cryptographic hashing, and file management.
         
*   **Model Details:** Llama 3 (8B parameter model) running entirely locally via Ollama to ensure zero data leakage to cloud servers.
     
*   **Architectural Decisions:** The codebase utilizes a modular architecture to ensure high code quality, readability, and maintainability.
     
    *   `app.py`: Acts as the main controller, managing the Streamlit UI and session state.
         
    *   `chatbot.py`: Encapsulates the AI logic, System Prompts, and Ollama API calls.
         
    *   `data_handler.py`: Isolates the GDPR data sanitization and database saving logic.
         

## Prompt Design
 
The core of the chatbot's intelligence relies on a strictly structured System Prompt designed to handle sequential information gathering and dynamic question generation.
 

*   **Role Definition:** The LLM is firmly instructed to act as a professional tech recruiter, setting the tone for the interaction.
     
*   **Step-by-Step Flow Constraint:** To prevent the LLM from asking for all information at once, the prompt explicitly commands it to ask for details "ONE BY ONE." This ensures a natural conversational flow.
     
*   **Dynamic Generation Trigger:** The prompt instructs the LLM to acknowledge the candidate's tech stack immediately upon receipt, and then generate  *exactly*  3-5 technical questions tailored to those specific technologies.
     
*   **Guardrails & Fallbacks:** Fallback mechanisms are hardcoded into the prompt. If a user asks for recipes, coding help, or company secrets, the LLM is instructed to politely decline, remind the user of its purpose as a hiring assistant, and steer the conversation back to the active interview step.
     

## Challenges & Solutions
 

1.  **Challenge: Context Hallucination and Rushing**
     
    *    *Issue:*  Early iterations of the LLM would occasionally try to ask the technical questions before finishing the basic information gathering, or it would attempt to make up details about the fictional company.
         
    *    *Solution:*  Refined the prompt engineering by implementing a strict, numbered step-by-step framework (1. Greeting, 2. Information Gathering, 3. Technical Screening, 4. Closing). Added a specific negative constraint: "Do not make up answers about the company."
         
2.  **Challenge: Ensuring GDPR Data Privacy with LLMs**
     
    *    *Issue:*  Sending unmasked candidate details (PII) to a cloud-based API (like OpenAI) violates strict data privacy standards for local-only storage requirements.
         
    *    *Solution:*  Shifted the infrastructure to a completely local deployment using **Llama 3 via Ollama**. Furthermore, developed a custom `anonymize_data()` pipeline in `data_handler.py`. Before any candidate data is written to the mock JSON database, the script cryptographically hashes the candidate's name (SHA-256) and heavily masks the email address and phone number strings.
