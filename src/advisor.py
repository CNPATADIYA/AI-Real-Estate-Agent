import streamlit as st
from dotenv import load_dotenv
import os

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langchain_community.llms.ollama import Ollama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder

load_dotenv()
os.environ["STREAMLIT_WATCHDOG"] = "false"

# app config
st.set_page_config(page_title="RealEstate Advisor", page_icon="🤖")
st.title("RealEstate AI Advisor")


# Ensure answers are available
if "answers" not in st.session_state or not st.session_state.answers_ready:
    st.error("Please complete the questionnaire first!")
    st.stop()


embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
# Initialize vector_store & LLM
vector_store = FAISS.load_local("property_vector_db",  embeddings)
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})
#llm = init_chat_model("llama3-8b-8192", model_provider="groq")
llm = init_chat_model("llama3-70b-8192", model_provider="groq")
#llm = Ollama(model="deepseek-r1:1.5b")

#####################
##########################

def get_response(rag_chain, user_query, chat_history, user_preference, question_and_answer):
    response = rag_chain.invoke({"input": user_query, "chat_history": chat_history, "user_preference": user_preference, "questions_and_answers": question_and_answer})
    return response["answer"]


if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello, I am a RealEstate Advisor. I will help you to find property based on you preference and also solve your queries."),
    ]


if "retrieved_docs" not in st.session_state:
    st.session_state.retrieved_docs = ""



# Initial suggestion message
Initial_suggestion = f"""Hello, I am finding property in {st.session_state.answers['q1']['Answer']}. 
The possession should be {st.session_state.answers['q6']['Answer']}. 
I am looking for {st.session_state.answers['q7']['Answer']}. 
Property type is {st.session_state.answers['q8']['Answer']} and configuration can be {st.session_state.answers['q9']['Answer']}. 
I am finding properties in the following areas: {st.session_state.answers['q10']['Answer']}. 
{st.session_state.answers['q11']['Answer']} regarding workplace/school. 
My budget is {st.session_state.answers['q12']['Answer']}. 
I want to have {st.session_state.answers['q17']['Answer']} neighborhood."""


system_prompt = (
    "You are an realestate advisor for advising user to buy properties based on their preference. "
    "There is user preference. Understand that properly"
    "There is set of question which are answered by user. Understand that thoroughly"
    "Use the following pieces of retrieved context to answer "
    "show retrived context to user and explain everything about properties and give analysis why should they buy it"
    "the question. If you don't know the answer, say that you "
    "don't know. "
    "\n\n"
    "{context}"
    "{user_preference}"
    "{questions_and_answers}"
)

contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

qanda = list(st.session_state.answers.values())
questions_and_answers = "\n".join([f"Question: {item['Question']}, Answer: {item['Answer']}" for item in qanda])

# st.session_state.chat_history.append(HumanMessage(content=Initial_suggestion))
# response = get_response(rag_chain, str(Initial_suggestion), st.session_state.chat_history, questions_and_answers)
# st.session_state.chat_history.append(AIMessage(content=response))
#st.session_state.chat_history.append(AIMessage(content=response["answer"]))

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
        response = get_response(rag_chain, user_query, st.session_state.chat_history, Initial_suggestion, questions_and_answers)
        st.markdown(response)
    st.session_state.chat_history.append(AIMessage(content=response))

if st.button("Clear Chat"):
    st.session_state.chat_history = [
        AIMessage(content="Hello, I am a RealEstate Advisor. How can I help you?"),
    ]
    st.rerun()