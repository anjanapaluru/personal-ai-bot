import streamlit as st
from google import genai
from google.genai import types

# 1. App Configuration and Title
st.set_page_config(page_title="My Personal Voice Bot", page_icon="🤖")
st.title("🤖 Personal AI Persona Bot")
st.write("Ask me anything about my life, skills, and goals!")

# 2. Hardcode your personal background and facts here
MY_CONTEXT = """
You are an AI clone of Anjana Paluru. You must respond to all questions in the first person ("I", "me", "my") as if you are the user themselves.

Here is the truth about you to answer the testing questions:
1. Life Story:  I am an AI Architect with 7 years of background in HR Tech. I hold an IT B.Tech from JNTU University. I build autonomous multi-agent systems and deep learning pipelines.
2. #1 Superpower: Bridging the gap between deep AI engineering and HR business strategy.
3. Top 3 Growth Areas: Orchestrating multi-agent networks, securing enterprise MCP environments, and scaling self-healing infrastructure.
4. Coworker Misconception:  People assume I only handle administrative HR tasks. In reality, I write neural networks and manage LLMOps pipelines.
5. Pushing Boundaries: I build zero-intervention autonomous agent swarms. I also train high-precision predictive compensation deep learning models.

Keep your answers conversational, concise, and professional.
"""

# 3. Securely input your Google API Key via the UI sidebar
with st.sidebar:
    api_key = st.text_input("Enter Google API Key", type="password")
    st.info("Get an API key from Google AI Studio.")

# 4. Chat logic
if api_key:
    # Initialize the Gemini Client
    client = genai.Client(api_key=api_key)
    
    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Handle new user input
    if user_prompt := st.chat_input("Ask a question..."):
        # Display user message
        st.chat_message("user").markdown(user_prompt)
        st.session_state.messages.append({"role": "user", "content": user_prompt})

        try:
            # Generate response using system instructions to enforce your persona
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=MY_CONTEXT,
                    temperature=0.7
                )
            )
            
            # Display bot response
            bot_response = response.text
            with st.chat_message("assistant"):
                st.markdown(bot_response)
                
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            
        except Exception as e:
            st.error(f"Error generating response: {e}")
else:
    st.warning("Please enter your Google API Key in the sidebar to start the bot.")
