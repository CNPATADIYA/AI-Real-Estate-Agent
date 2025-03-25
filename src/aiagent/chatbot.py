from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import MessagesPlaceholder

import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["STREAMLIT_WATCHDOG"] = "false"



# app config
st.set_page_config(page_title="RealEstate Advisor", page_icon="🤖")
st.title("RealEstate AI Advisor")

if "user_preference" not in st.session_state:
    st.error("Please provide preference first!")
    st.stop()


llm = init_chat_model("llama3-70b-8192", model_provider="groq")


with st.container(border=True):
    st.write(llm.invoke(st.session_state.user_preference).content)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello, I am a RealEstate Advisor. I will help you to find property based on you preference and also solve your queries."),
    ]

contextualize_q_system_prompt = (
    f"""
    You are an expert real estate advisor. 
    {st.session_state.user_preference}
    """)
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

with st.container(border=True):
    st.write(contextualize_q_system_prompt)


# conversation
for i, message in enumerate(st.session_state.chat_history):
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)


user_query = st.chat_input("Ask here...")

if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        formatted_prompt = contextualize_q_prompt.format(chat_history=st.session_state.chat_history, input=user_query)
        response = llm.invoke(formatted_prompt).content
        st.markdown(response)
    st.session_state.chat_history.append(AIMessage(content=response))

if st.button("Clear Chat"):
    st.session_state.chat_history = [
        AIMessage(content="Hello, I am a RealEstate Advisor. How can I help you?"),
    ]
    st.rerun()