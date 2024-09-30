import os
import json
import datetime
from models.ollama_model import OllamaModel

with open("repo_code_text.txt") as f:
    codebase_contents = f.read()

system_prompt = """
You are an expert in analysing code repository. You can explain the code repository in high level  provide a high-level overview of the architecture.
Describe the following:

    - The main components or modules and their roles.
    - The relationships or interactions between different components.
    - The core technologies or frameworks used.
    - The overall design pattern (e.g., MVC, microservices, monolithic, etc.).
    - Any key functionalities or features implemented in the codebase.
    - Any notable third-party libraries or dependencies.
    - The general flow of data or control through the system.

Focus on summarizing the high-level architecture rather than line-by-line details of the code.
Use your analysis to help me understand how the system is organized and functions.

"""

# high level arch
# system_prompt = f"""
# You are a highly skilled software architect and code analysis expert.
# Your task is to analyze code repositories and describe their high-level architecture.
# You should provide an overview of the components, the relationships between files and directories,
# the purpose of key files, and how different parts of the repository interact with each other.
#
# """

code_prompt = f"""Here is the codebase:\n{codebase_contents}"""

user_prompt = """
Can you provide a high-level overview of the architecture? 
Describe the relationships between files and directories, identify the main components, 
and explain how different parts of the repository interact. 
Also, highlight any key files or directories that play an important role in the system's design.
"""

# prompt = system_prompt + user_prompt
prompt = [
    {"role": "system", "content": system_prompt},
    {"role": "system", "content": code_prompt},
    {"role": "user", "content": user_prompt},
]


def generate_run_id():
    # Get the current date and time
    now = datetime.datetime.now()

    # Format the date as YYYYMMDD and time as HHMMSS
    date_str = now.strftime("%Y%m%d")
    time_str = now.strftime("%H%M%S")

    return f"{date_str}_{time_str}"


RUN_ID = generate_run_id()

for ollama_model_id in [
    "codegemma:7b",
    "llama3.2:latest",
    "codellama:latest"
]:
    import gc

    gc.collect()

    ollama_model = OllamaModel(ollama_model_id)

    responses = ollama_model.generate(json.dumps(prompt))

    run_id_dir_path = f"./repo_viz/outputs/hl_arch/{RUN_ID}"
    os.makedirs(run_id_dir_path, exist_ok=True)

    ollama_model_id_formatted = ollama_model_id.replace('.', '_').replace(':', '_')
    # file name storing in outputs/hl_arch/<DATE>_<TIME>/_<Model>.md
    output_file_path = f"{run_id_dir_path}/{ollama_model_id_formatted}.md"

    with open(output_file_path, "w") as f:
        if type(responses) is dict:
            print("responses is dict")
            responses = json.dumps(responses)
        f.write(responses)
