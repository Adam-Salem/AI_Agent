import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    full_path = os.path.join(working_directory,directory)
    
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_dir = os.path.abspath(full_path)
    
    # Ensure directory exists within the working directory
    if not abs_target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    # Ensure directory is an actual directory
    if os.path.isdir(abs_target_dir) == False:
        return f'Error: "{directory}" is not a directory'
    
    # Iterate through each file and display info
    file_info = []
    for file in sorted(os.listdir(abs_target_dir)):
        fsize = os.path.getsize(os.path.join(abs_target_dir,file))
        f_dir = os.path.isdir(os.path.join(abs_target_dir,file))
        file_info.append(f'- {file}: file_size={fsize} bytes, is_dir={f_dir}')
    return '\n'.join(file_info)


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)