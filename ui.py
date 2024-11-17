import streamlit as st
import pandas as pd
import time

from evals import generate


if "variables_expanded" not in st.session_state:
    st.session_state["variables_expanded"] = False

def message(container, message, icon=None):
    # Display the success message in the container
    container.success(message, icon=icon)

    # Wait for a few seconds
    time.sleep(3)

    # Clear the container, effectively hiding the success message
    container.empty()

selected_models = st.multiselect("Select models", ["gpt-4o-mini", "gpt-4o"])

prompt = st.text_area("Enter a prompt", placeholder="What is the capital of {country}")

@st.cache_data
def process_csv(file):
    try:
        df = pd.read_csv(file)
        msg_conaytiner = st.empty()
        message(msg_conaytiner,"CSV file uploaded successfully!", icon="✅")
        return df
    except Exception as e:
        st.error(f"Error reading CSV file: {str(e)}")

with st.expander("Variable Settings", expanded=st.session_state.variables_expanded):
    # CSV upload section
    uploaded_file = st.file_uploader("Upload variable CSV file", type="csv")
    if uploaded_file is not None:
        df = process_csv(uploaded_file)
        st.session_state.edited_df = st.data_editor(df, num_rows="dynamic")


if st.button("Run"):
    with st.spinner("Running models..."):
        st.session_state.variables_expanded = False
        df = st.session_state.edited_df

        results_data = generate(selected_models, prompt, df)
        
        results_df = pd.DataFrame(results_data)
        st.dataframe(results_df)


