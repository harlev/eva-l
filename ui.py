import streamlit as st
import pandas as pd
import time

from llms import MockLLM
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langchain_core.prompts import PromptTemplate

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

with st.expander("Variable Settings"):
    # CSV upload section
    uploaded_file = st.file_uploader("Upload variable CSV file", type="csv")
    if uploaded_file is not None:
        df = process_csv(uploaded_file)
        st.session_state.edited_df = st.data_editor(df, num_rows="dynamic")


if st.button("Run"):
    # st.dataframe(st.session_state.edited_df)

    for current_model in selected_models:
        print(current_model)
        prompt_template = PromptTemplate.from_template(prompt)
        df = st.session_state.edited_df
        
        for index, row in df.iterrows():
            # Format prompt with all column values from the row
            # Extract only the variables mentioned in the prompt template
            template_variables = prompt_template.input_variables
            row_dict = {k: v for k, v in row.to_dict().items()}
            formatted_prompt = prompt_template.format(**row_dict)
            messages = [HumanMessage(content=formatted_prompt)]
            result = MockLLM().generate(messages=messages, model=current_model)
            print(f"Row {index}: {result}")


