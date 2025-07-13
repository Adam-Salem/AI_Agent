import os

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