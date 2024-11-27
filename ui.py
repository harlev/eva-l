import re
import streamlit as st
import pandas as pd
import time
import os

from eval_types import RegexEvalScore
from evals import generate
from dotenv import load_dotenv
from logger import logger
from openai_models import list_openai_models
load_dotenv()

st.set_page_config(
        page_title="Eva-L LLM Evals",
        page_icon="⚖️",
        # layout="wide",
    )


def message(container, message, icon=None):
    container.success(message, icon=icon)
    time.sleep(3)
    container.empty()


if "openai_api_key" not in st.session_state and os.getenv('OPENAI_API_KEY'):
    st.session_state.openai_api_key = os.getenv('OPENAI_API_KEY')

@st.dialog("API Keys")
def get_api_key():
    api_key = st.text_input('Enter your OpenAI API key:', 
                           type='password', 
                           value=st.session_state.get("openai_api_key", ""),
                           key="api_key",
                           help="Keys are never stored, only used for this session")
    if st.button("Save"):
        st.session_state.openai_api_key = api_key
        st.rerun()



col1, col2 = st.columns([5,1])
with col1:
    selected_models = st.multiselect("Select models", list_openai_models(st.session_state.openai_api_key), placeholder="Select models", label_visibility="collapsed")
    if selected_models:
        logger.info(f"Selected models: {selected_models}")
with col2:
    if st.button("Set API 🔑"):
        get_api_key()

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
    uploaded_file = st.file_uploader("Upload variable CSV file", type="csv")
    if uploaded_file is not None:
        df = process_csv(uploaded_file)
        st.session_state.edited_df = st.data_editor(df, num_rows="dynamic")
        
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
    if 'openai_api_key' not in st.session_state:
        st.error('Please enter your OpenAI API key first')
    else:
        with st.spinner("Running models..."):
            df = st.session_state.edited_df

            eval = RegexEvalScore(rule=regex_rule, flags=regex_flags)
            results_data = generate(selected_models, prompt, df, eval, 
                                expected_column=st.session_state.expected_column,
                                api_key=st.session_state.openai_api_key)
            
            results_df = pd.DataFrame(results_data)
            st.dataframe(results_df)

