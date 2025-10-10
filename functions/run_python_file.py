import os
import subprocess
import sys
from google import genai
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_full_path = os.path.abspath(full_path)
        abs_working_dir = os.path.abspath(working_directory)

        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        if not os.path.isfile(abs_full_path):
            return f'Error: File "{file_path}" not found.'
        
        # Construct command to run
        command = [sys.executable, file_path] + args

        completed_process = subprocess.run(
            command,
            cwd=working_directory,  # Execute from specified directory
            capture_output=True,    # Capture stdout and stderr
            text=True,              # Decodes output as text
            timeout=30              # Set a 30 sec timout
        )

        # Formatting output
        output_parts = []
        stdout = completed_process.stdout.strip()
        stderr = completed_process.stderr.strip()

        if stdout:
            output_parts.append(f"STDOUT:\n{stdout}")

        if stderr:
            output_parts.append(f"STDERR:\n{stderr}")
        
        if completed_process.returncode != 0:
            output_parts.append(f"Process exited with code {completed_process.returncode}")

        if not output_parts:
            return "No output produced."
        
        return "\n".join(output_parts)
    
    except subprocess.TimeoutExpired:
        return f"Error: Execution of '{file_path}' timed out after 30 seconds."
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and captures its output. Only '.py' files are allowed.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the Python script to be executed.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="An optional list of string arguments to pass to the script upon execution.",
            ),
        },
        required=["file_path"],
    ),
)