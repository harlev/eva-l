from langchain_core.prompts import PromptTemplate
from llms import MockLLM
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage


def generate(selected_models, prompt, variables_df):
    results_data = []
    prompt_template = PromptTemplate.from_template(prompt)

    for current_model in selected_models:
        for index, row in variables_df.iterrows():
            row_dict = {k: v for k, v in row.to_dict().items()}
            formatted_prompt = prompt_template.format(**row_dict)
            messages = [HumanMessage(content=formatted_prompt)]
            result = MockLLM().generate(messages=messages, model=current_model)
                
            results_data.append({
                    "Model": current_model,
                    "Input": formatted_prompt,
                    "Output": result
                })
            
    return results_data