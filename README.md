# RepoViz

# Task
- High Level architecture
  - This is not the final task but the reason behind doing this is to judge if the model is able to figure out the architecture. It's very likely that if the model is not able to do this,  it will not be able to create a graph containing relationships which programmatically can be drawn.
- Generate a graph of the components of the codebase and how they interact with each other.

# Initial Thoughts
- Since usually repositories are huge, we need a LLM which has quite a large context window size.
  - There are few models specific to code related task with 1MM context window size but they are paid/closed.
    - Gemini Pro 1.5 - 1 MM
    - other models as well which don't have 1MM context size but they can be good enough with context window size of 200K+
  - Planning to use below OPEN SOURCE
    - `codellama/CodeLlama-7b-Instruct-hf` : using typical huggingface pipeline module
    - `llama3.2` - 3B: since it was new, JUST thought to try it once.. not seeing anywhere the mention of code analysing abilities though. using ollama on local
    - `codegemma:7b` : using ollama on local
- Extracting all file contents of repository in 1 text file so that it can be passed in the prompt will be needed.

# Test Repo
  - The repo mentioned in the [thread](https://x.com/deedydas/status/1802529105860252129) is not available publicly anymore.
  - Choosing [AdalFlow](https://github.com/SylphAI-Inc/AdalFlow) . Have never used this but heard positive things about it. Hence, thought to take this. Although, open to take any other repo as well.
    - When putting all files' contents in a text file, it has ~39k lines or ~128k words or ~1.4MM characters
  - If context window of an LLM becomes a problem, for the sake of this task, we can choose another repo to show POC.
    - For now, using AdalFlow, as it will also give an idea how much the models are limited.


# Models' performance on summary / high level architecture
- llama3.2 - 3B performed worst and is not usable at least for code related stuffs.
- codellama 7b
    - codellama was showing signs that it can understand the code and could utter basic things . 
      - e.g on asking the high level architecture, it replied with (after few prompt engg tweaks):
      ```
        The AdalFlow project is a text-to-text generation model based on transformer architecture. It consists of several files and directories, each with its own purpose and function. Here is a high-level overview of the architecture:

        1. `adalflow` directory: This is the main directory for the repository. Inside this directory are subdirectories for different components of the system, such as `src`, `data`, `notebooks`, etc.
        2. `src` directory: This directory contains the source code for the text-to-text generation model. The main file in this directory is `adalflow/__init__.py`, which imports all the necessary libraries and defines the main class `AdalFlow`.
        3. `data` directory: This directory stores the data used to train and evaluate the model. The main file in this directory is `data/adalflow_data.json`, which contains a dictionary of training and evaluation data for the model.
        4. `notebooks` directory: This directory contains Jupyter notebooks that are used to document the model's performance, results, and other relevant information. The main file in this directory is `notebooks/README.md`, which provides an overview of the notebooks and their contents.
        5. `use_cases` directory: This directory contains example use cases for the text-to-text generation model. The main file in this directory is `use_cases/rag/build/README.md`, which describes a specific use case for building a RAG (Risk Adjusted Generative) task pipeline.
        6. `tutorials` directory: This directory contains tutorials and guides for using the text-to-text generation model. The main file in this directory is `tutorials/README.md`, which provides an overview of the tutorials and their contents.
        7. `issues` directory: This directory contains issues related to the repository, such as bugs, feature requests, and other relevant information. The main file in this directory is `issues/ISSUE_TEMPLATE/custom.md`, which defines a custom issue template for reporting problems with the model.
        8. `LICENSE` file: This file contains the license under which the repository is released, such as MIT or Apache 2.0.
        9. `README.md` file: This file provides an overview of the repository and its contents, including a brief description of the project, installation instructions, and usage examples.

      In summary, the architecture of the AdalFlow project is designed to be modular, with separate directories for different components of the system. The main files in each directory serve as entry points for their respective functions, and they work together to provide a comprehensive text-to-text generation model.```
      ```
      - with  initial few prompt engg, it was not able to get the architecture in a very detailed manner. This summary looks too superficial.
- codegemma
  - Asked the same high level architecture and it replied with 
    ```**High-Level Architecture Overview**
  
    **File and Directory Structure:**
            
    The repository is organized into various files and directories, each with a specific purpose:
            
    - **.github/ISSUE_TEMPLATE:** Contains two issue templates: bug report and custom issue template.
      - **use_cases:** Includes various use cases for AdalFlow, such as RAG and retrieval tasks.
      - **notebooks:** Houses Jupyter notebooks for showcasing code and results.
      - **docs:** Documents the AdalFlow functionalities and architecture.
            
    **Key Components:**
            
    - **AdalFlow Library:** The primary module containing the core functionalities and logic.
      - **RAG Task Pipeline:** Responsible for retrieving context based on user queries.
      - **Data Process Pipeline:** Preprocesses data and converts it into embeddings.
      - **LLM Judge:** Evaluates the retrieved context based on user feedback.
            
    **File and Directory Interaction:**
            
    - The RAG task pipeline interacts with the data process pipeline to obtain embeddings.
      - The LLM judge relies on the RAG task pipeline and user feedback for evaluation.
      - Notebooks showcase the utilization of AdalFlow functionalities in different scenarios.
            
    **Key Files and Directories:**
            
    - **use_cases/rag/build/README.md:** Provides instructions on different ways to build a RAG.
      - **use_cases/README.md:** Lists outstanding tasks and potential features.
      - **notebooks/README.md:** Outlines the structure and usage of Jupyter notebooks.
            
    **Additional Notes:**
            
    - The repository includes instructions for setting up the development environment.
      - There is a template Jupyter notebook for creating new colab notebooks.
      - The link to the colab notebook is provided.```
  - In my opinion, this is better than whatever results we have seen so far. But we can improve probably with prompt engg.

# Models on Graph creation
- LLama3.2 - 3B
   - Since, it was not able to give good high level architecture. Not trying this for graph visualisation.
- CodeGemma
  - wrote prompt asking to read the code and write the relationships of codebase in dot file so that graphviz can be utilised.
  - it returned with response:
  
  ```**Codebase Component Diagram**
      
      **File:** components.dot
      
      ```dot
      digraph components {
          node [shape=box]
      
          // Core Components
          model { label="Model" }
          tokenizer { label="Tokenizer" }
          generator { label="Generator" }
          retriever { label="Retriever" }
          judge { label="Judge" }
      
          // Data Processing
          data_loader { label="Data Loader" }
          embedding_generator { label="Embedding Generator" }
      
          // Data Storage
          database { label="Database" }
      
          // Connections
          model -> tokenizer
          tokenizer -> generator
          generator -> retriever
          retriever -> judge
          judge -> model
          model -> database
          embedding_generator -> database
      }
      ```
      
      **Explanation:**
      
      * The graph shows the key components of the codebase.
        * Each node represents a component.
        * The lines represent the flow of data between components.
        * The `model` component is the central element, responsible for generating text and making decisions.
        * Other components like `tokenizer`, `generator`, `retriever`, `judge`, and `database` are involved in the process.
        * `Data Loader` and `Embedding Generator` are responsible for preparing the data.
      
      **Usage:**
      
      * Save the `components.dot` file in a location accessible to graphviz.
        * Run the following command to generate the graph:
      
      ```
      dot -Tpng components.dot -o components.png
      ```
      
      * Open the generated `components.png` file to view the graph.
      
      **Note:**
      
      * This diagram provides a high-level overview of the codebase components.
        * The actual implementation details of each component may be more complex.
        * The graph can be further modified to include additional components or specific functionality.```
      
  ```  
   - I manually pasted the dot file contents in a file to create the graphviz.
     - Diagram looked like [this](https://dreampuf.github.io/GraphvizOnline/?compressed=CYSw5gTghgDgFgAgMYHsC2MUDsCmWAuAzggN4BQClCWKwOCA2oXLDgLwBGKAHgLpkUqAeiEIAwigj0JGbHiKDKaWjgA2pBKqgc1bAEQBZFar0IAvooT4UAazwgAXjggatO1foAqt%2B04imLKgQwPGcoaxcSTW1dPQBxUOgIgMspfAgQHAA3Z1cYjz0AJRx0zJz-c0sAKwBXYBC8930AKTqQlMsRBAARcKgEAAUIFCQcQkIQLDBLYD6AfVUUKDpI6Ka9Xvx%2BgBkllZSgnDQdYFApuZDcJMlG2IBRY5xTybAEBKvwyQ6grs3%2BgGUIlAQjM%2BhwoIR6FE3LE-uDId9hKIJFhcEh8CBsIRLMo6OoALQAPisPiwjmclmsdjJfgQROCiU%2BEEslzCETpxLSGWyFKCXLKuXptXqOGqbXo9Nxahxxg5CFmW3hosOj2e51Z1xc9IV2ghorMQA)
  - This needs more prompt engg.
- CodeLlama: #TODO

# Thoughts after above steps:
- Prompt engg is needed in many of the steps involved in above.
- Closed/Paid models to try
- Right now, I am manually copying the dot file contents and creating a new file for graph visualisation.
  - Agentic kind of workflow needed for THIS task !!? which directly taked dot file and in the end creates the graph visualisation without manually doing anything.
