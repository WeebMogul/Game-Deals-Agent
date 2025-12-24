import streamlit as st
import requests
import json
import os
import uuid
import time
import logging

st.title("Game Deals Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_id" not in st.session_state:
    st.session_state.user_id = f"user-{uuid.uuid4()}"

if "session_id" not in st.session_state:
    st.session_state.session_id = None

agent_url = "http://localhost:8000"
agent_name = "game_agent"


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
        st.success(f"New session created: {session_id}")
        st.rerun()  # Rerun to update the UI immediately
        return True
    except requests.exceptions.RequestException as e:
        st.sidebar.error(f"Failed to initiate session: {e}")
        return False


# Sidebar for session management
with st.sidebar:
    st.header("⏳ Session Management")
    if st.session_state.session_id:
        st.success(f"Active session: {st.session_state.session_id}")
    else:
        st.warning("No active session.")

    if st.button("➕ Create Session"):
        create_session(agent_url, agent_name, st.session_state.user_id)


def send_message(message, agent_url, agent_name):
    """
    Sends a message to the agent and renders the response in a structured, streaming way.
    Tool calls are displayed using st.status in chronological order.
    """

    if not st.session_state.session_id:
        st.error("No active session")

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

        # final_text_placeholder = st.empty()

        with requests.post(
            full_url, headers=headers, json=payload, stream=False
        ) as response:

            event_data = json.loads(response.content)

            for data in event_data:
                if "content" in data and data["content"].get("parts"):
                    for part in data["content"]["parts"]:
                        # print(part)
                        if "text" in part:

                            final_response_text = part["text"]
                            # print(part["text"])

            # print(final_response_text)
            st.write(final_response_text)

            # text_data = event_data[0]["content"]["parts"][0]["text"]

            # st.write(text_data)

        #         for chunk in response.iter_content(chunk_size=None):
        #             if not chunk:
        #                 continue
        #             try:
        #                 lines = chunk.decode("utf-8").splitlines()
        #                 for line in lines:
        #                     # print(line)
        #                     if not line.startswith("data:"):
        #                         continue

        #                     json_data = line[len("data:") :].strip()
        #                     if not json_data:
        #                         continue

        #                     event = json.loads(json_data)
        #                     logging.log(msg=event, level=1)

        #                     if "content" in event and event["content"].get("parts"):
        #                         for part in event["content"]["parts"]:
        #                             if "text" in part and part["text"] != "":
        #                                 text_content = part["text"]

        #                                 is_partial = event.get("partial", True)

        #                                 if is_partial:
        #                                     final_response_text += text_content
        #                                 else:
        #                                     final_response_text = text_content

        #                                 # final_text_placeholder.markdown(
        #                                 #     final_response_text + "Hello"
        #                                 # )

        #             except json.JSONDecodeError as e:
        #                 print(f"Could not decode JSON: {line} - Error: {e}")
        #             except Exception as e:
        #                 print(f"Error processing chunk: {e}")

        #     if final_response_text:
        #         final_text_placeholder.markdown(final_response_text)
        #     else:
        #         final_text_placeholder.markdown("*Response completed*")

        # except requests.exceptions.RequestException as e:
        #     error_message = f"Error connecting to agent: {e}"
        #     final_text_placeholder.error(error_message)
        #     final_response_text = error_message
        # except Exception as e:
        #     error_message = f"An unexpected error occurred: {e}"
        #     final_text_placeholder.error(error_message)
        #     final_response_text = error_message

    st.session_state.messages.append(
        {"role": "assistant", "content": final_response_text}
    )


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if st.session_state.session_id:
    if user_input := st.chat_input(
        "Ask about stocks, companies, market trends, or financial analysis..."
    ):
        send_message(user_input, agent_url, agent_name)
else:
    st.info("👈 Create a session to start chatting 💬")
