import os
from .config import MAX_CHARS

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory,file_path)
    
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_file = os.path.abspath(full_path)
    
    # Ensure file exists in working directory
    if not abs_target_file.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    # Ensure file is a file and not a directory
    if os.path.isfile(abs_target_file) == False:
        return f'Error: File not found or is not a regular file: "{directory}"'
    
    # Read file up to MAX_CHARS
    try:
        with open(abs_target_file, "r") as f:
            file_content = f.read(MAX_CHARS)
            if len(f.read()) > MAX_CHARS:
                file_content += (f'[...File "{file_path}" truncated at {MAX_CHARS} characters]')
            return file_content
    except Exception as e:
        return f'Error: {str(e)}'