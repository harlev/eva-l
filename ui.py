import re
import streamlit as st
import pandas as pd
import time

from eval_types import RegexEvalScore
from evals import generate


def message(container, message, icon=None):
    # Display the success message in the container
    container.success(message, icon=icon)

    # Wait for a few seconds
    time.sleep(3)

    # Clear the container, effectively hiding the success message
    container.empty()

selected_models = st.multiselect("Select models", ["gpt-4o-mini", "gpt-4o"])

prompt = st.text_area("Enter a prompt", placeholder="Prompt with {variables} here")

@st.cache_data
def process_csv(file):
    try:
        df = pd.read_csv(file)
        msg_conaytiner = st.empty()
        message(msg_conaytiner,"CSV file uploaded successfully!", icon="✅")
        return df
    except Exception as e:
        st.error(f"Error reading CSV file: {str(e)}")

with st.expander("Variable Settings"):
    # CSV upload section
    uploaded_file = st.file_uploader("Upload variable CSV file", type="csv")
    if uploaded_file is not None:
        df = process_csv(uploaded_file)
        st.session_state.edited_df = st.data_editor(df, num_rows="dynamic")
        
        # Add column selector for expected results
        columns = df.columns.tolist()
        st.selectbox(
            "Select column containing expected results",
            columns,
            key="expected_column"
        )

with st.expander("Evaluation Settings"):
    regex_rule = st.text_input("Regex rule", value=r"^.*{expected}.*$")
    regex_flags = sum((getattr(re, flag) for flag in st.multiselect("Regex flags", ["IGNORECASE"], default=["IGNORECASE"])), 0)


if st.button("Run"):
    with st.spinner("Running models..."):
        df = st.session_state.edited_df

        eval = RegexEvalScore(rule=regex_rule, flags=regex_flags)
        results_data = generate(selected_models, prompt, df, eval, expected_column=st.session_state.expected_column)
        
        results_df = pd.DataFrame(results_data)
        st.dataframe(results_df)


