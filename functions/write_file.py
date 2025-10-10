import os

# Writes into the file given
def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_full_path = os.path.abspath(full_path)
        abs_working_dir = os.path.abspath(working_directory)

        # Checks if file is in directory
        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # Opens and overwrites file
        with open(abs_full_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        # Returns success string
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    # Catches any errors
    except Exception as e:
        return f'Error: {e}'