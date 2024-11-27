from openai import OpenAI
import streamlit as st

@st.cache_data(ttl=60*60)
def list_openai_models(api_key: str = None):
    client = OpenAI(api_key=api_key)
    models = client.models.list()
    return [model.id for model in models if model.id.startswith("gpt")]


if __name__ == "__main__":
    print(list_openai_models())