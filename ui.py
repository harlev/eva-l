import streamlit as st
import pandas as pd
import time

def message(container, message, icon=None):
    # Display the success message in the container
    container.success(message, icon=icon)

    # Wait for a few seconds
    time.sleep(3)

    # Clear the container, effectively hiding the success message
    container.empty()

model = st.multiselect("Select models", ["gpt-4o-mini", "gpt-4o"])

prompt = st.text_area("Enter a prompt")
# Initialize session state for columns and data if not exists
if 'columns' not in st.session_state:
    st.session_state.columns = []
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=st.session_state.columns)



with st.expander("Variable Settings"):
    # CSV upload section
    uploaded_file = st.file_uploader("Upload CSV file", type="csv")
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.edited_df = st.data_editor(df, num_rows="dynamic")
            # st.success("CSV file uploaded successfully!", icon="✅")
            msg_conaytiner = st.empty()
            message(msg_conaytiner,"CSV file uploaded successfully!", icon="✅")
        except Exception as e:
            st.error(f"Error reading CSV file: {str(e)}")


