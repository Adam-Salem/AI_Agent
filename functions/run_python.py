import os 
import subprocess

def run_python_file(working_directory, file_path):
    full_path = os.path.join(working_directory,file_path)
    
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_file = os.path.abspath(full_path)
    
    # Ensure file exists in working directory
    if not abs_target_file.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # Ensure file exists
    if os.path.exists(abs_target_file) == False:
        return f'Error: File "{file_path}" not found'
    
    # Ensure file is a .py file
    if full_path.endswith(".py") == False:
        return f'Error: "{file_path}" is not a Python file.'
    
    # Execute file
    try:
        output = []
        execution = subprocess.run(["python", file_path], timeout=30, capture_output=True, text=True, cwd=abs_working_dir)
        if execution.stdout != "":
            output.append("STDOUT:" + execution.stdout)
        if execution.stderr != "":
            output.append("STDERR:" + execution.stderr)
        if execution.returncode != 0:
            output.append("Process exited with code " + str(execution.returncode))
        
        
        if len(output) == 0:
            return "No output produced."
        else:
            return '\n'.join(output)
    except Exception as e:
        return f'Error: executing Python file: {e}'