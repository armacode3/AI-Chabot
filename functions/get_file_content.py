import os
from config import MAX_CHARS

# Returns the files contents
def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_full_path = os.path.abspath(full_path)
        abs_working_dir = os.path.abspath(working_directory)

        # Checks if file_path is in working_directory
        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Checks if file is a file
        if not os.path.isfile(abs_full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Opens file to read
        with open(abs_full_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Checks if content is larger than the max characters
        if len(content) > MAX_CHARS:
            # If it is then it is chopped of at max characters
            truncated = content[:MAX_CHARS]
            # String is added at end of content
            return truncated + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        # If content is not longer than max characters then it is just returned
        return content
    # Checks if not in utf-8 format
    except UnicodeDecodeError:
        return f'Error: Cannot read "{file_path}" as it is not a text file.'
    # Any other errors
    except Exception as e:
        return f"Error: {e}"