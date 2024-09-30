import os
import json
import datetime
import traceback
import subprocess
from models.ollama_model import OllamaModel

with open("repo_code_text.txt") as f:
    codebase_contents = f.read()


codebase_prompt = f"Here is the codebase to analyze:\n{codebase_contents}"


# for relationship in terms of code files
system_prompt = f"""
You are an expert software architect proficient in code analysis, dependency mapping, and graph representation using the DOT language.
Your task is to analyze the provided codebase to understand the structural relationships and interactions between its components. 
This includes identifying dependencies between files, classes, functions, and folders, as well as any architectural patterns or modular structures.

You will represent these relationships using the DOT language in a way that can be used with Graphviz. Ensure the correct usage of DOT syntax, including:

1. Quoting filenames or class names that contain special characters like dots (e.g., 'main.py' or 'FaceDetector').
2. Using subgraphs to represent folder structures, ensuring that folder groupings are clear and correctly linked.
3. Displaying relationships between files (e.g., imports, dependencies), class hierarchies, and function calls with correct DOT formatting.

The output should be a valid DOT file with no syntax errors, formatted for Graphviz visualization.
"""


user_prompt = """
Please generate a `.dot` file that accurately represents the structure and interactions of the components within the codebase. 
The file should capture:

1. Relationships between files (e.g., imports, dependencies), ensuring **all filenames and class names that contain special characters** (such as periods `.` or hyphens `-`) are enclosed in **double quotes**.
2. Class hierarchies (inheritance, composition) with appropriate edges, and ensure inheritance is shown using arrows with labels like `label="inherits"`.
3. Function calls and dependencies with clear connections between functions and classes, also ensuring that any function names with special characters are enclosed in double quotes.
4. Folder structure using subgraphs to represent folders, with files and subfolders grouped inside their respective folders. Do not use `graph [rank=same; ...]`, instead, use `subgraph` with a `cluster_<folder_name>` to group nodes.

Make sure all file and folder names are enclosed in **double quotes** to avoid Graphviz syntax errors. 
The output should be valid DOT syntax and can be rendered without errors.
The output should only include the valid `.dot` file content, without any additional explanation or commentary.
"""

# for relationships in terms of functional components
system_prompt = f"""
You are an expert software architect proficient in code analysis and dependency mapping. Your task is to analyze the provided codebase in detail and understand the structural relationships and interactions between its components. 
Instead of merely copying filenames, your goal is to identify key components based on their functionality and purpose.

You should:
1. **Interpret the purpose of each file, class, function, and module**, and assign a human-readable name that reflects its role in the codebase (e.g., "Face Detection Module" instead of "face_detector.py").
2. **Identify and name the key components**, including modules, classes, or functions, based on what they represent in the overall architecture (e.g., "Image Preprocessing" for a module that handles image transformations).
3. **Map relationships between these components**, such as class inheritance, function dependencies, and file imports. Represent these relationships clearly in a way that shows how the components interact.

The output should describe the structure of the codebase in terms of meaningful components and how they are connected, rather than simply listing file names.
"""

user_prompt = """
Please generate a `.dot` file that accurately represents the structure and interactions of the key components within the codebase. Use the following guidelines:

1. **Human-readable component names**: Instead of copying filenames, assign meaningful names to each component based on its role or functionality (e.g., "Image Preprocessing" instead of "image_utils.py").
2. **Map relationships**: Clearly show relationships between components, such as class inheritance, function calls, and module dependencies.
3. **Use subgraphs** to represent logical groupings or layers, such as different modules or folders in the project.
4. Ensure that the `.dot` file is valid Graphviz syntax and can be rendered without any errors.

The output should include:
- High-level relationships between components.
- Connections between classes, functions, and modules.
- Groupings of components in subgraphs where appropriate.

Remember to name components based on their functionality, not the filename.
The output should only include the valid `.dot` file content, without any additional explanation or commentary.
"""

# prompt = system_prompt + user_prompt
prompt = [
    {"role": "system", "content": system_prompt},
    {"role": "system", "content": codebase_prompt},
    {"role": "user", "content": user_prompt},
]


def generate_run_id():
    # Get the current date and time
    now = datetime.datetime.now()

    # Format the date as YYYYMMDD and time as HHMMSS
    date_str = now.strftime("%Y%m%d")
    time_str = now.strftime("%H%M%S")

    return f"{date_str}_{time_str}"


# Helper function to clean Markdown formatting from .dot content
def clean_dot_content(dot_content):
    # Strip out markdown code block backticks and language identifier (`dot`)
    if dot_content.startswith("```dot"):
        dot_content = dot_content.lstrip("```dot").rstrip("```")
    return dot_content.strip()


RUN_ID = generate_run_id()

# TODO: if not correct dot file generated, retry logic to add
for ollama_model_id in [
    "codegemma:7b",
    "llama3.2:latest",
    "codellama:latest"
]:
    import gc

    gc.collect()

    ollama_model = OllamaModel(ollama_model_id)

    responses = ollama_model.generate(json.dumps(prompt))

    run_id_dir_path = f"./repo_viz/outputs/graphviz/{RUN_ID}"
    os.makedirs(run_id_dir_path, exist_ok=True)

    ollama_model_id_formatted = ollama_model_id.replace('.', '_').replace(':', '_')
    # file name storing in outputs/hl_arch/<DATE>_<TIME>/_<Model>.md
    output_file_path = f"{run_id_dir_path}/{ollama_model_id_formatted}.md"

    with open(output_file_path, "w") as f:
        if type(responses) is dict:
            print("responses is dict")
            responses = json.dumps(responses)
        f.write(responses)

    # Write the .dot file to the output directory
    dot_file_path = f"{run_id_dir_path}/{ollama_model_id_formatted}.dot"

    with open(dot_file_path, "w") as f:
        if type(responses) is dict:
            responses = json.dumps(responses)
        cleaned_dot_content = clean_dot_content(responses)
        print(f"\n\n{cleaned_dot_content}\n\n")
        f.write(cleaned_dot_content)


    try:
        output_png_path = f"{run_id_dir_path}/{ollama_model_id_formatted}.png"
        command = f"dot -Tpng {dot_file_path} -o {output_png_path}"
        # Run the command
        subprocess.run(command, shell=True, check=True)
        print(f"Graph successfully generated at: {output_png_path}")
    except subprocess.CalledProcessError as e:
        print(traceback.format_exc())
        print(f"Error generating graph: {e}")
