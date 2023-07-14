# NotebookGPT

Use OpenAI GPTs models to create and execute a python notebook. Similar to what you could do with Code Interpreter.

## Set up

### Env
Create a .env file at the root of the folder and add your openai api key in it:
```
OPENAI_API_KEY = "your-key"
```

### Python environment
Create a conda environment named notebook-gpt and install dependencies:
```
conda create -n notebook-gpt
conda activate notebook-gpt
pip install -r requirements.txt
```

## Running

```
python src/notebook_gpt.py file_name number_of_steps
```