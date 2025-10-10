import os

# Returns every file in directory
def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
        abs_full_path = os.path.abspath(full_path)
        abs_workign_dir = os.path.abspath(working_directory)

        # Checks if directory is in working_directoyr
        if not abs_full_path.startswith(abs_workign_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Checks if in current directory
        if not os.path.isdir(abs_full_path) :
            return f'Error: "{directory}" is not a directory'

        # Gets a list of every item in path
        contents = os.listdir(abs_full_path)
        output = []

        # Gets the size and checks if it is in current directory
        for item in sorted(contents):
            item_path = os.path.join(abs_full_path, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            # Appends information to output
            output.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")

        # Output is combined with '\n'
        return "\n".join(output)
    # Catches errors
    except Exception as e:
        return f"Error: {e}"
