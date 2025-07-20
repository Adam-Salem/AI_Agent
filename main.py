import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ClientError
import inspect
import time
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

func_dict = {"get_files_info": get_files_info, 
             "get_file_content": get_file_content, 
             "run_python_file": run_python_file, 
             "write_file": write_file}

def call_function(function_call, verbose=False):
    func = func_dict[function_call.name]
    sig = inspect.signature(func)
    allowed_args = sig.parameters.keys()
    function_call.args["working_directory"] = "./calculator"
    
    # Filter arguments to only allow those accepted by function
    filtered_args = {k: v for k, v in function_call.args.items() if k in allowed_args}
    
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
    
    # Call function
    if function_call.name not in func_dict:
        return types.Content(
            role="tool",
            parts=[types.Part.from_function_response(
                    name=function_call.name,
                    response={"error": f"Unknown function: {function_call.name}"})])
    else:
        function_result = func(**filtered_args)
        return types.Content(
            role="tool",
            parts=[types.Part.from_function_response(
                    name=function_call.name,
                    response={"result": function_result})])

# def call_function(*args, **kwargs):
#     class FakePart:
#         function_response = type('FR', (), {'response': {'result': "Fake tool function result"}})()
#     return type('FResult', (), {'parts': [FakePart()]})()

# def fake_generate_content(*args, **kwargs):
#     class FakeCandidate:
#         def __init__(self, text):
#             self.content = types.Content(role="model", parts=[types.Part(text=text)])
#             self.finish_reason = "stop"
#     # Simulate what Gemini would return
#     class Response:
#         candidates = [FakeCandidate("Fake model reply!")]
#         function_calls = []
#         usage_metadata = type('um', (), {'prompt_token_count': 0, 'candidates_token_count': 0})()
#     return Response()

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

Always call get_files_info before trying to do any other functions to understand the directory structure. Any file you try to read, write, or execute must have the proper relative path.
All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

If a function call fails, analyze the error and adjust your approach rather than repeating the same failed operation.
"""

load_dotenv()

model_name = "gemini-2.0-flash-001"
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

if len(sys.argv) == 1:
    exit(1)
prompt = sys.argv[1]

verbose = False
if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
    verbose = True

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, 
                           schema_get_file_content, 
                           schema_run_python_file, 
                           schema_write_file])

messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
loop_counter = 0
done = False

while(loop_counter < 20):
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt))
    except ClientError as e:
        # If token limit is reached, wait and try again
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            print(f"Rate limit hit. Waiting 60 seconds before retry...")
            time.sleep(60)
            continue
        else:
            print(f"API error: {e}")
            raise e
    except Exception as e:
        print(f"Unexpected error: {e}")
        break

    for candidate in response.candidates:
        messages.append(candidate.content)
        if getattr(candidate, "finish_reason", None) == "stop":
            print(candidate.content.parts[0].text)
            done = True
            break
    if done:
        break

    if response.function_calls:
        for function_calls_part in response.function_calls:
            func_result = call_function(function_calls_part, verbose)
            tool_message = types.Content(role="model",
                                        parts=[types.Part(text=func_result.parts[0].function_response.response['result'])])
            messages.append(tool_message)
            try:
                print(f"-> {func_result.parts[0].function_response.response}")
            except Exception as e:
                print(f"Error occurred: {e}")
    if verbose:
        print("User prompt:", prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    loop_counter+=1
for msg in messages:
    print(msg)
