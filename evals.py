from langchain_core.prompts import PromptTemplate
from abc import ABC, abstractmethod
from eval_types import EvalScoreInterface, Evaluation
from llms import MockLLM, OpenAILLM
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage


def generate(selected_models, 
             prompt, variables_df,
             eval: EvalScoreInterface,
             expected_column: str = "expected_output") -> list[dict]:
    results_data = []
    prompt_template = PromptTemplate.from_template(prompt)

    for current_model in selected_models:
        for index, row in variables_df.iterrows():
            row_dict = {k: v for k, v in row.to_dict().items()}
            formatted_prompt = prompt_template.format(**row_dict)
            messages = [HumanMessage(content=formatted_prompt)]
            result = OpenAILLM().generate(messages=messages, model=current_model)
            
            # Get expected output from variables dataframe using the provided column name
            expected_output = row_dict.get(expected_column, "")
            
            # Create evaluation and score it
            evaluation = Evaluation(
                input=formatted_prompt,
                output=result,
                expected_output=expected_output,
                score=0.0
            )
            
            eval_result = eval.score(evaluation)
                
            results_data.append({
                "Model": current_model,
                "Input": formatted_prompt,
                "Output": result,
                "Expected": expected_output,
                "Score": eval_result.score
            })
            
    return results_data
