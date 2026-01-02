import streamlit as st
import requests
import json
import os
import uuid
import time
import logging


def send_message(message, agent_url, agent_name):
    """
    Sends a message to the agent and renders the response in a structured, streaming way.
    Tool calls are displayed using st.status in chronological order.
    """

    # if not st.session_state.session_id:
    #     st.error("No active session")

    st.session_state.messages.append({"role": "user", "content": message})

    with st.chat_message("user"):
        st.markdown(message)

    payload = {
        "appName": agent_name,
        "userId": st.session_state.user_id,
        "sessionId": st.session_state.session_id,
        "newMessage": {"role": "user", "parts": [{"text": message}]},
    }
    headers = {"Content-Type": "application/json"}
    full_url = f"{agent_url}/run"

    final_response_text = ""

    with st.chat_message("assistant"):

        with requests.post(
            full_url, headers=headers, json=payload, stream=False
        ) as response:

            event_data = json.loads(response.content)

            for data in event_data:
                if "content" in data and data["content"].get("parts"):
                    for part in data["content"]["parts"]:
                        if "text" in part:

                            final_response_text = part["text"]

            st.write(final_response_text)

    st.session_state.messages.append(
        {"role": "assistant", "content": final_response_text}
    )


def create_session(agent_url, agent_name, user_id):
    """
    Create a new session with the specified agent.
    """
    session_id = f"session-{int(time.time())}"
    session_init_url = (
        f"{agent_url}/apps/{agent_name}/users/{user_id}/sessions/{session_id}"
    )
    try:
        response = requests.post(
            session_init_url,
            headers={"Content-Type": "application/json"},
            json={"state": {}},
        )
        response.raise_for_status()
        st.session_state.session_id = session_id
        st.session_state.messages = []
        # st.success(f"New session created: {session_id}")
        st.rerun()  # Rerun to update the UI immediately
        return True
    except requests.exceptions.RequestException as e:
        st.sidebar.error(f"Failed to initiate session: {e}")
        return False


st.title("Game Deals Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_id" not in st.session_state:
    st.session_state.user_id = f"user-{uuid.uuid4()}"

agent_url = "http://localhost:8000"
agent_name = "game_agent"

if "session_id" not in st.session_state:
    # st.session_state.session_id = None
    create_session(agent_url, agent_name, st.session_state.user_id)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if st.session_state.session_id:
    if user_input := st.chat_input(
        "Ask about deals on certain games or a list of game deals from Steam."
    ):
        send_message(user_input, agent_url, agent_name)
