# RepoViz

# Task
- High Level architecture
  - This is not the final task but the reason behind doing this is to judge if the model is able to figure out the architecture. 
  - It's very likely that if the model is not able to do this,  it will not be able to create a graph containing relationships which programmatically can be drawn.
- Generate a graph of the components of the codebase and how they interact with each other.

# Test Repo
  - The repo mentioned in the [thread](https://x.com/deedydas/status/1802529105860252129) is not available publicly anymore.
  - have found [this repo](https://github.com/kukico/DeepFaceLab) with same content. Using this repo.

# Initial Thoughts
- Since usually repositories are huge, we need a LLM which has quite a large context window size.
  - There are few models specific to code related task with 1MM context window size but they are paid/closed.
    - Gemini Pro 1.5 - 1 MM
    - other models as well which don't have 1MM context size but they can be good enough with context window size of 200K+
  - Planning to use below OPEN SOURCE
    - `codellama` : using ollama
      - 7B params
      - 3.8 GB
    - `llama3.2` - 3B: since it was new, JUST thought to try it once. not seeing anywhere the mention of code analysing abilities though. using ollama on local
      - 3B params
      - 2GB
    - `codegemma:7b` : using ollama on local
      - 7B params
      - 5 GB
- Extracting all file contents of repository in 1 text file so that it can be passed in the prompt will be needed.
- If context window of an LLM becomes a problem, for the sake of this task, we can choose another repo to show POC.


# Models' performance on summary / high level architecture
- Model wise performance comments
  - llama3.2 - 3B performed worst and is not usable at least for code related stuffs.
  - codellama 7b
      - codellama was showing signs that it can understand the code and could utter basic things .
      - but it was not able to get to more detailed
  - codegemma
    - Among all the alternatives tried, this performed the best.
    - the output looked convincing enough.
    - probably, bigger params model of this will be very good for this task.
- Codegemma is the winner here.
- few outputs of models can be checked out at `outputs/hl_arch/<run_id>/<model_id>.md`

# Models on Graph creation
- Model wise performance comments 
  - LLama3.2 - 3B
     - Since, it was not able to give good high level architecture. Hunch was that it will not be able to produce good dot file.
     - Although, dot file given did not have very good detailed relationships.
     - It was able to figure out how to output in dot file content.
  - Codellama - 7B
    - more often than not, it was  not able to get the dot file. It was generating some text description.
    - Not usable.
  - CodeGemma
    - Its outputs on trying multiple times gives results which makes the conclusion hard to draw.
    - It is able to figure out some relationships and convert it into dot file format.
    - Often it is also able to find out reasonable amount of relationships.
    - In my opinion, 
      - either it needs more prompt engineering or
      - we need to break down the task into 2: 
        - creating high level arch description and
        - using above description to create a dot file for graph visualisation
- Codegemma is the most suitable model for the task of analysing the repo it seems.
  - Having said that this still does seem to be at a stage where people can use this.
- few outputs can be checked out at `outputs/graphviz/<run_id>/<model_id>.md` [if some error happens, png may not get generated.. just heads up]

# Thoughts after above steps:
- Step of graph creation can be broken down into 2. 
  - using 2 models, where one model generates the high level architecture description and other converts into dot file.
- Closed/Paid models to try
