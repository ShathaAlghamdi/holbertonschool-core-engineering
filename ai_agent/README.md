# AI Agents in Python
 
## Description
 
**AI Study Guide Generator.** You give it a programming topic, for example
`Python decorators`. Three AI agents then work one after another to write a
Markdown study guide, and two deterministic Python tools check the guide and
save it to `output/study_guide.md`.
 
Stack: **Python**, **Google ADK** (agents), **LiteLLM** (model connector) and
**Ollama** (local model runtime).
 
````
Google ADK  ->  LiteLLM  ->  Ollama  ->  local model
````
 
## Requirements
 
- Python 3.10 or newer
- [Ollama](https://ollama.com) installed and running
- A small local model, for example `llama3.2` (about 2 GB)
- About 4 GB of free RAM for a 3B model
## Setup
 
````bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
 
# 2. Install the Python dependencies
pip install -r requirements.txt
 
# 3. Install Ollama (macOS: download the app from ollama.com,
#    Linux: see the official install instructions), then pull a model
ollama pull llama3.2
 
# 4. Check that the model answers outside Python first
ollama run llama3.2 "Say hello in one sentence."
````
 
## Configuration
 
Copy the example file and edit it:
 
````bash
cp .env.example .env
````
 
| Variable          | Example                     | Meaning                                    |
|-------------------|-----------------------------|--------------------------------------------|
| `OLLAMA_API_BASE` | `http://localhost:11434`    | Address of the local Ollama server         |
| `MODEL_NAME`      | `ollama_chat/llama3.2`      | LiteLLM model name (`ollama_chat/<model>`) |
| `DEBUG`           | `0`                         | Set to `1` to see full error tracebacks    |
 
**Model provider used:** Ollama, running `llama3.2` locally.
 
To use another LiteLLM provider, change `MODEL_NAME` (for example
`gemini/gemini-2.0-flash`) and add that provider's key to `.env`, for example
`GEMINI_API_KEY`. Never commit `.env`: it is listed in `.gitignore`.
 
## How to Run
 
````bash
# Topic on the command line
python3 main.py "Python decorators"
 
# Or let the program ask for the topic
python3 main.py
````
 
Example topics are listed in `data/topic_examples.json`.
 
The workflow runs in this order:
 
````
Topic input
  -> Explainer Agent
  -> Practice Designer Agent
  -> Draft Study Guide
  -> Reviewer Agent
  -> Final Markdown Assembly
  -> Validation Tool
  -> Save Markdown Tool  (output/study_guide.md)
````
 
## Example Input
 
````bash
python3 main.py "Python decorators"
````
 
````
[1/6] Explainer Agent: explaining 'Python decorators'...
[2/6] Practice Designer Agent: creating an exercise...
[3/6] Assembling the draft study guide...
[4/6] Reviewer Agent: reviewing the draft...
[5/6] Assembling the final study guide...
[6/6] Validating and saving...
Validation passed: all required sections are present.
Study guide saved to .../output/study_guide.md
````
 
## Example Output
 
Input: `python3 main.py "HTTP status codes"` (shortened output):
 
````markdown
# HTTP status codes
 
## Simple Explanation
 
HTTP status codes are used to communicate the result of an HTTP request.
They are three-digit numbers that indicate whether an action was successful
or not...
 
## Key Concepts
 
* HTTP status codes are three-digit numbers.
* They indicate the result of an HTTP request.
* Codes can be categorized into five main groups: Informational, Successful,
  Redirection, Client Error, and Server Error.
 
## Example
 
```http
HTTP/1.1 200 OK
```
The HTTP/1.1 200 OK status code indicates that the request was successful...
 
## Practice Exercise
 
**Exercise:** Build a simple HTTP status code table that categorizes the
codes into their respective groups...
 
## Common Mistakes
 
* Not checking for redirect codes (like 301 or 302)...
* Not checking for server error codes (like 500 or 502)...
 
## Review Comments
 
**Missing information:**
- A more detailed explanation of the five main groups...
 
**Recommendation:** Approved
 
## Final Summary
 
HTTP status codes are an essential part of the HTTP protocol, providing
crucial information about the outcome of requests...
````
 
## Project Structure
 
````
ai-agents-intro/
├── agents/
│   ├── common.py                   # model config + run_agent() helper
│   ├── explainer_agent.py
│   ├── practice_designer_agent.py
│   └── reviewer_agent.py
├── tools/
│   ├── file_writer.py              # save_markdown_file()
│   └── validation.py               # validate_required_sections()
├── output/
│   └── study_guide.md              # generated study guide
├── data/
│   └── topic_examples.json         # example topics
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── main.py                         # sequential workflow
````
 
## Agents
 
| Agent | File | Input | Output |
|-------|------|-------|--------|
| **Explainer Agent** | `agents/explainer_agent.py` | The topic | Simple Explanation, Key Concepts, Example, Common Mistakes and Final Summary, as `##` sections |
| **Practice Designer Agent** | `agents/practice_designer_agent.py` | The topic and the explanation | One small exercise, with expected input and output and one or two hints. It does not repeat the explanation |
| **Reviewer Agent** | `agents/reviewer_agent.py` | The draft guide | Missing information, unclear parts, suggestions, and an Approved or Needs revision recommendation. It does not rewrite the guide |
 
All three agents use the same model, built in `agents/common.py`. Each agent
has one narrow job, and its instructions fix the exact output format.
 
## Tools
 
| Tool | File | What it does |
|------|------|--------------|
| `save_markdown_file(file_path, content)` | `tools/file_writer.py` | Creates the parent folder if needed, writes the file in UTF-8 and returns the absolute path. It raises a readable `OSError` if the write fails |
| `validate_required_sections(markdown)` | `tools/validation.py` | Checks that the 8 required headings exist and returns `{"valid": bool, "missing": [...]}` |
 
The tools are plain Python with no AI inside, so the same input always gives
the same result.
 
Test the tools without any model:
 
````bash
python3 -c "from tools.validation import validate_required_sections as v; print(v('# T\n## Example\n'))"
python3 -c "from tools.file_writer import save_markdown_file as s; print(s('output/test.md', '# Test\n'))"
````
 
## Troubleshooting
 
| Problem | Message | Fix |
|---------|---------|-----|
| Empty topic | `Topic cannot be empty.` | Pass a topic, for example `python3 main.py "HTTP status codes"` |
| `.env` missing | `MODEL_NAME is not set...` | Run `cp .env.example .env` |
| Ollama not running | `Cannot reach Ollama at http://localhost:11434...` | Open the Ollama app, or run `ollama serve` |
| Model not pulled | `The model '...' is not available...` | Run `ollama pull llama3.2` and check `MODEL_NAME` |
| Cannot write the file | `Could not write Markdown file ...` | Check folder permissions and free disk space |
| Validation failed | `Validation failed. Missing sections: ...` | The model ignored the format. Run again or try a bigger model. The file is still saved so you can inspect it |
| Need more detail | (any error) | Set `DEBUG=1` in `.env` to see the full traceback |
 
## Self-Validation Checklist
 
- [ ] Project directories and base files exist
- [ ] Virtual environment created, dependencies installed
- [ ] Ollama installed, model pulled, model answers with `ollama run`
- [ ] Explainer Agent tested with at least two topics
- [ ] `save_markdown_file()` tested without the agent
- [ ] `validate_required_sections()` tested with valid and incomplete Markdown
- [ ] Practice Designer Agent uses the explanation as context
- [ ] Reviewer Agent comments without rewriting the guide
- [ ] `main.py` runs the full workflow and saves `output/study_guide.md`
- [ ] Errors are readable (empty topic, missing config, Ollama down)
- [ ] `.env` is not committed, and no secrets are in the repository
## Reflection
 
**What is the difference between a direct LLM call and an AI agent?**
A direct LLM call sends one prompt and gets text back. An agent wraps the model
with a role, fixed instructions, optional tools and execution logic, so it can
do a specific job the same way every time and be combined with other agents.
 
**What role does each agent have in your system?**
The Explainer teaches the topic. The Practice Designer turns that explanation
into one small exercise. The Reviewer checks the draft and gives feedback.
Each agent does one job only, so the outputs do not overlap.
 
**What role does each tool have in your system?**
`validate_required_sections()` checks the structure of the guide, and
`save_markdown_file()` writes it to disk. These steps must be predictable, so
they are done in normal Python code and not by the model.
 
**What was the most difficult part of the project?**
Setting up the environment, more than writing the agents. Ollama was not
installed at first (`command not found: ollama`), so I installed it with
Homebrew and started it as a service. The `.env.example` file did not get
copied because files starting with a dot are hidden on macOS, so the program
stopped with `MODEL_NAME is not set` until I created `.env`. My system Python
was 3.9, which made Google ADK print many warnings (it expects 3.10+), even
though the workflow still ran.
 
**What limitation did you observe when using your selected model?**
With `llama3.2` (3B, running locally) the structure was correct and validation
passed, but the content quality was uneven. For "HTTP status codes":
 
- The practice exercise asked for at least 10 status codes per group in about
  10 minutes, which is unrealistic (the Informational group does not even have
  10 common codes).
- The Reviewer Agent listed missing and unclear parts, but still answered
  **Approved**, so its recommendation does not always match its own comments.
- Some explanations were vague, for example comparing status codes to
  "letters in a letter box".
The validator can check the headings, but it cannot check if the content is
correct or useful. A human still needs to read the result.
 
## Known Limitations
 
- Small local models do not always follow the format exactly. The validator
  reports missing sections but does not fix them.
- The quality of the content depends on the model. The Reviewer Agent is also
  an LLM, so it can miss mistakes too.
- Each run creates new sessions, so there is no memory between runs.
- `output/study_guide.md` is overwritten on every run.
- Answers can differ from one run to another for the same topic.
 