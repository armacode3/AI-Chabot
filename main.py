import sys
import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Import functions and schema
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file

# Every available funciton
AVAILABLE_FUNCTIONS = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")
    
    if function_name not in AVAILABLE_FUNCTIONS:
        function_result = {"error": f"Unknown function: {function_name}"}
    else:
        function_to_call = AVAILABLE_FUNCTIONS[function_name]
        args_dict = dict(function_args)
        args_dict["working_directory"] = "./calculator"
        try:
            result_string = function_to_call(**args_dict)
            function_result = {"result": result_string}
        except Exception as e:
            function_result = {"error": str(e)}

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response=function_result,
            )
        ],
    )

def main():
    # Argument parsr for prompt and flag
    parser = argparse.ArgumentParser(
        description="An example AI agent that requires a prompt and accepts an optional flag."
    )

    parser.add_argument(
        "prompt",
        type=str,
        help="The text prompt for the AI Agent"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose mode to print extra details"
    )

    args = parser.parse_args()
    user_prompt = args.prompt
    is_verbose = args.verbose

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    try:
        # Set up gemini client
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)

        # Save previous messages
        messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]

        tools = types.Tool(
            function_declarations=[
                schema_get_files_info,
                schema_get_file_content,
                schema_run_python_file,
                schema_write_file,
            ]
        )

        system = types.Content(role="user", parts=[types.Part(text=system_prompt)])
        cfg = types.GenerateContentConfig(tools=[tools], system_instruction=system)

        # Creates response
        response = client.models.generate_content(
            model='gemini-2.0-flash-001', 
            contents=messages,
            config=cfg,
        )
        
        while response.function_calls:
            messages.append(response.candidates[0].content)

            function_call_results = []
            for function_call in response.function_calls:
                result_content = call_function(function_call, verbose=is_verbose)
                function_call_results.append(result_content)

                if is_verbose:
                    if not result_content.parts or not result_content.parts[0].function_response:
                        raise RuntimeError("Invalid function response from call_function.")

                    response_dict = result_content.parts[0].function_response.response
                    print(f"-> {response_dict}")

            messages.extend(function_call_results)

            response = client.models.generate_content(
                model='gemini-2.0-flash-001', 
                contents=messages,
                config=cfg,
            )

        print(f"\n{response.text}")

    # Catch errors
    except KeyError:
        print("Error: GEMINI_API_KEY not found. Please set it in your .env file.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
