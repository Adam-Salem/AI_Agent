import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

model_name = "gemini-2.0-flash-001"

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

if len(sys.argv) == 1:
    exit(1)
prompt = sys.argv[1]

verbose = False
if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
    verbose = True

available_functions = types.Tool(
    function_declarations=[schema_get_files_info]
)

messages = [types.Content(role="user", parts=[types.Part(text=prompt)]),]
response = client.models.generate_content(
    model=model_name,
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt))

# print(response.text)
if len(response.function_calls) != None:
    for function_calls_part in response.function_calls:
        print(f'Calling function: {function_calls_part.name}({function_calls_part.args})')
if verbose:
    print("User prompt:", prompt)
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
