import streamlit as st
from google import genai
from io import StringIO



st.title("Simple ai chatbot")

if "client" not in st.session_state:
    st.session_state.client = genai.Client()

if "chat" not in st.session_state:
    st.session_state["chat"] = st.session_state.client.chats.create(
        model="gemini-3-flash-preview"
    )


if "file_sent" not in st.session_state:
    st.session_state["file_sent"] = False

if "messages" not in st.session_state:
    st.session_state["messages"] = []

upload_file = st.file_uploader("Upload any text file")

if upload_file is not None and not st.session_state["file_sent"]:
    string_io = StringIO(upload_file.getvalue().decode("utf-8"))
    text = string_io.read()

    st.session_state["chat"].send_message(f"Here is a document {text}")
    st.session_state["file_sent"] = True

if st.session_state["file_sent"]:

    for message in st.session_state.messages:
        if message["role"] == "user":
            st.chat_message("user").write(message["parts"][0]["text"])
        else:
            st.chat_message("assistant").write(message["parts"][0]["text"])


    user_question = st.text_input("Enter a question about the document ")

    if st.button("Submit"):
        st.session_state.messages.append({"role" : "user" , "parts" : [{"text" : user_question}]})
        response = st.session_state.chat.send_message(f"{user_question}")
        st.session_state.messages.append({"role" : "model" , "parts" : [{"text" : response.text}]})
        
        st.rerun()

    
    

