# eva-l
LLM Evaluation Framework

### Currently implemented
- [x] Open AI model selection
- [x] Prompt definition with template variables
- [x] Uploading a set of variables (csv)
- [x] Eval regex rule
- [x] Running evals concurrently and showing rule results in a table

### Future plan
- [ ] Support more LLM models (Anthropic Claude etc.)
- [ ] Extend prompt to support System + User sections
- [ ] Define model settings (Temperature etc)
- [ ] More Eval types (Semantic similarity etc)
- [ ] Better results visualization. Color for success/fail
- [ ] Support expandability for models and eval rules


### Basic usage example
[streamlit-ui-2024-11-22-22-11-36.webm](https://github.com/user-attachments/assets/53cf7406-2852-4d8e-be70-3cddab4680a3)


## Local Setup
1. Clone the repository to your local machine
```
git clone https://github.com/harlev/eva-l.git
cd eva-l
```
2. Create a virtual environment (optional but recommended)
```
python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```
3. Install the required dependencies  
`pip install -r requirements.txt`
4. Optionally, set your `.env` file with  
`OPENAI_API_KEY=<your API key>`
5. Run the Streamlit app  
`streamlit run ui.py`
