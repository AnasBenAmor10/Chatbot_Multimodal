import streamlit as st
from llm_chain import load_normal_chain
from langchain.memory import StreamlitChatMessageHistory


def load_chain(chat_history):
    return load_normal_chain(chat_history)


# clear the user’s input field after sending a message
def clear_input_field():
    st.session_state.user_question = st.session_state.user_input
    st.session_state.user_input = ""


# This function is called when the user types a message and changes the send_input status to True (user wants to send the message.)
def set_send_input():
    st.session_state.send_input = True
    clear_input_field()


def main():

    st.title("Multimodal Local Chat App")
    # display messages exchanged between the user and the AI
    chat_container = st.container()
    st.sidebar.title("Chat Sessions")
    
    if "send_input" not in st.session_state:
        st.session_state.send_input = False
        st.session_state.user_question = ""

    chat_history = StreamlitChatMessageHistory(key="history")
    llm_chain = load_chain(chat_history)
    user_input = st.text_input(
        "Type your Message Here", key="user_input", on_change=set_send_input
    )
    send_button = st.button("send", key="send_button")
    if send_button or st.session_state.send_input:
        if st.session_state.user_question != "":

            with chat_container:
                llm_response = llm_chain.run(st.session_state.user_question)
                st.session_state.user_question = ""
    if chat_history.messages != []:
        with chat_container:
            st.write("Chat History")
            for message in chat_history.messages:
                st.chat_message(message.type).write(message.content)


if __name__ == "__main__":
    main()
