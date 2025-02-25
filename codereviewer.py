import streamlit as st
import google.generativeai as genai

genai.configure(api_key = "")

st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(to right, #1E3A8A, #3B82F6);
            animation: gradientAnimation 5s ease infinite;
        }

        @keyframes gradientAnimation {
            0% {background: linear-gradient(to right, #1E3A8A, #3B82F6);}
            50% {background: linear-gradient(to right, #2563EB, #4F46E5);}
            100% {background: linear-gradient(to right, #1E3A8A, #3B82F6);}
        }

        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border-radius: 12px;
            padding: 10px 24px;
            box-shadow: 0 9px #999;
        }

        .stButton>button:hover {
            background-color: #45a049;
            box-shadow: 0 12px #999;
            transform: translateY(-4px);
        }

        .stTextArea textarea {
            background-color: #F3F4F6;
            color: #333;
            border-radius: 8px;
            padding: 15px;
        }

        .success-message {
            background-color: #FFD700;
            color: black;
            padding: 20px;
            font-size: 18px;
            border-radius: 10px;
        }

        .history-message {
            background-color: #98C9E1;
            color: black;
            padding: 20px;
            font-size: 18px;
            border-radius: 10px;
        }

        .animated-effect {
            font-size: 22px;
            color: #FF6347;
            animation: pulseEffect 1.5s ease-in-out infinite;
        }

        @keyframes pulseEffect {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
    </style>
    """, unsafe_allow_html=True)

st.title("Suman AI Code Reviewer and Generater🤖")

llm = genai.GenerativeModel("models/gemini-1.5-flash")
chatbot = llm.start_chat(history=[])

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

def update_chat(role, message):
    st.session_state["chat_history"].append({"role": role, "content": message})

st.markdown("""
    <h3 style="color: #FF6347;">Welcome to the AI Code Reviewer App! 🎉</h3>
    <p style="font-size: 18px; color: #fff; background-color: #4CAF50; padding: 10px; border-radius: 10px;">
    Let the AI Review or Generate it for you!
    </p>
    """, unsafe_allow_html=True)

input_code = st.text_area("**Enter your Python code here or  Which code you want:**", height=200)

if st.button("Result:"):
    st.markdown("""
        <div class="animated-effect">
            🚀 Please Wait ...  as your Result is Generating!
        </div>
    """, unsafe_allow_html=True)

    if input_code.strip():
        update_chat("human", input_code)
        review_prompt = f"Review the following Python code to identify any critical issues, focusing on potential bugs, inefficiencies, or areas for improvement. Then, provide concise suggestions for enhancing the code's functionality, performance, or readability:\n{input_code}"
        response = chatbot.send_message(review_prompt)

        update_chat("ai", response.text)
        st.success("Successfully Excuted! See suggestions below.")
        st.subheader("AI Suggestions Results:")
        st.write(response.text)

        st.markdown("""
            <div class="animated-effect">
                🎉 Review complete! Check Suggestion above.
            </div>
        """, unsafe_allow_html=True)

    else:
        st.warning("Please Enter python code to review.")

if st.button("Show Previous History"):
    st.markdown("""
        <div class="history-message">
            Here's the past Search history.
        </div>
    """, unsafe_allow_html=True)

    if st.session_state["chat_history"]:
        st.subheader("Past Review History")
        for entry in st.session_state["chat_history"]:
            role = "User" if entry["role"] == "human" else "AI"
            st.markdown(f"*{role}:* {entry['content']}")
    else:
        st.info("No history available yet.")

