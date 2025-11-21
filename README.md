# AI Coding Agent

A command-line AI agent powered by Google's **Gemini 2.0 Flash** model. This agent is designed to act as an autonomous coding assistant capable of planning tasks, manipulating files, and executing Python code within a sandboxed environment.

## Features

* **Autonomous Planning**: The agent receives a prompt, devises a step-by-step plan, and executes it to achieve the user's goal.
* **Tool Integration**: Equipped with specific function calls to interact with the file system:
    * `get_files_info`: List files and directories with size details.
    * `get_file_content`: Read the contents of specific files.
    * `write_file`: Create or overwrite files with generated code.
    * `run_python_file`: Execute Python scripts and capture `stdout`/`stderr`.
* **Sandboxed Environment**: All file operations and code executions are constrained to a specific working directory (default: `./calculator`) to ensure safety.
* **Verbose Mode**: Optional flag to view the agent's internal thought process and tool execution details.

## Project Structure

* `main.py`: Application entry point and agent loop.
* `functions/`: Contains the implementation of tools available to the AI.
    * `run_python_file.py`: Securely executes Python code.
    * `get_files_info.py`: Securely lists directory contents.
* `calculator/`: The default sandbox directory where the agent operates.
* `pyproject.toml`: Dependency and project configuration.

## Setup & Installation

### 1. Prerequisites
* Python **3.12** or higher.
* A Google GenAI API key.

### 2. Install Dependencies
```bash
pip install google-genai python-dotenv
```

### 3. Environment Configuration
Create a `.env` file in the root directory of the project and add your API key:
```bash
GEMINI_API_KEY=your_actual_api_key_here
```

## Usage
Run the agent from the command line by providing a prompt string.

### Basic Command
```bash
python main.py "Check the files in the directory and run the main calculator script"
```

### Verbose Mode
Use the `-v` flag to see the tool calls, the agent's reasoning, and step-by-step execution details.
```bash
python main.py "Write a new python script that prints Hello World and run it" -v
```

## Testing
You can run the included test script to verify that the function calling logic and tools work as expected:
```bash
python tests.py
```
