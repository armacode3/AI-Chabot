import sys
import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file

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
    parser = argparse.ArgumentParser(
        description="An example AI agent that requires a prompt and accepts an optional flag."
    )
    parser.add_argument("prompt", type=str, help="The text prompt for the AI Agent")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode to print extra details")
    args = parser.parse_args()
    user_prompt = args.prompt
    is_verbose = args.verbose

    system_prompt = """
    You are a helpful AI coding agent. Your goal is to assist the user with their request by executing a plan.
    First, think step-by-step and devise a plan to address the user's request.
    Next, execute the plan by calling the necessary functions in sequence.
    Finally, once all the necessary information has been gathered, provide a comprehensive, final answer to the user.
    All file paths are relative to the working directory.
    """

    try:
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)

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
        
        for i in range(20): 
            if is_verbose:
                print(f"\n--- Turn {i+1} ---")
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-001', 
                contents=messages,
                config=cfg,
            )

           
            if not response.function_calls:
                print(f"\nFinal response:\n{response.text}")
                break

            messages.append(response.candidates[0].content)

            tool_responses = []
            for function_call in response.function_calls:
                result_content = call_function(function_call, verbose=is_verbose)
                tool_responses.append(result_content)
            
            messages.extend(tool_responses)

        else: 
            print("\nAgent could not complete the request in 20 iterations.")

    except KeyError:
        print("Error: GEMINI_API_KEY not found. Please set it in your .env file.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()