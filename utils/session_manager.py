import streamlit as st

class SessionManager:
    def __init__(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []  # Initialize messages list

    def add_message(self, role: str, content: str):
        """Adds a message to the session history."""
        st.session_state.messages.append({"role": role, "content": content})

    def get_history(self):
        """Returns the entire session history."""
        return st.session_state.messages

    def clear_history(self):
        """Clears the session history."""
        st.session_state.messages = []

    def display_messages(self):
        """Displays the session history in the Streamlit UI."""
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


if __name__ == '__main__':
    # Example Usage (for demonstration purposes)
    import streamlit as st

    st.title("Session Manager Example")

    session_manager = SessionManager()

    # Add a user message
    if st.button("Add User Message"):
        session_manager.add_message("user", "Hello, assistant!")

    # Add an assistant message
    if st.button("Add Assistant Message"):
        session_manager.add_message("assistant", "Hello, user! How can I help you?")

    # Clear the history
    if st.button("Clear History"):
        session_manager.clear_history()

    # Display the messages
    session_manager.display_messages()

    st.write("Session History:")
    st.write(session_manager.get_history())
