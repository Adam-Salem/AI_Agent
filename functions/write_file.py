import os
from google.genai import types

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory,file_path)
    
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_file = os.path.abspath(full_path)
    
    # Ensure file path exists in working directory
    if not abs_target_file.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    # If file path does not exist, create it
    if os.path.exists(os.path.dirname(abs_target_file)) == False:
        try:
            os.makedirs(os.path.dirname(abs_target_file))
        except Exception as e:
            return f'Error: {str(e)}'
    
    # Write content to file
    try:    
        with open(abs_target_file, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {str(e)}'
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a file in a specified directory, constrained to the working directory. If either the directory or the file do not exist, it will create them.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file that is generated or written to with the specified content.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that is written to the file."
            )
        },
        required=["file_path", "content"],
    ),
)