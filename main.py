import sys
import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

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

    try:
        # Set up gemini client
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)

        # Save previous messages
        messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]

        # Creates response
        response = client.models.generate_content(
            model='gemini-2.0-flash-001', contents=messages,
        )

        # Checks for flag to print extra information
        if is_verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        # Prints gemini response
        print(response.text)

    # Catch errors
    except KeyError:
        print("Error: GEMINI_API_KEY not found. Please set it in your .env file.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
