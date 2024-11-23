from langchain_core.prompts import PromptTemplate
from abc import ABC, abstractmethod
from eval_types import EvalScoreInterface, Evaluation
from llms import MockLLM, OpenAILLM
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage

def _process_single_row(row_dict, prompt_template, current_model, eval, expected_column, api_key):
        formatted_prompt = prompt_template.format(**row_dict)
        messages = [HumanMessage(content=formatted_prompt)]
        result = OpenAILLM().generate(messages=messages, model=current_model, api_key=api_key)
        
        expected_output = row_dict.get(expected_column, "")
        
        evaluation = Evaluation(
            input=formatted_prompt,
            output=result,
            expected_output=expected_output,
            score=0.0
        )
        
        eval_result = eval.score(evaluation)
            
        return {
            "Model": current_model,
            "Input": formatted_prompt,
            "Output": result,
            "Expected": expected_output,
            "Score": eval_result.score
        }

def generate(selected_models, 
             prompt, variables_df,
             eval: EvalScoreInterface,
             expected_column: str = "expected_output",
             api_key: str = None) -> list[dict]:
    

    results_data = []
    prompt_template = PromptTemplate.from_template(prompt)

    import asyncio
    import concurrent.futures
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for current_model in selected_models:
            for index, row in variables_df.iterrows():
                row_dict = {k: v for k, v in row.to_dict().items()}
                future = executor.submit(_process_single_row, row_dict, prompt_template, current_model, eval, expected_column, api_key)
                futures.append(future)
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results_data.append(result)
    
    print(results_data)
    return results_data
