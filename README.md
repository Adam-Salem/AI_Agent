This is a fun little project that I worked on to familiarize myself with prompt engineering.

To use this AI Agent, you will need:

Python 3.10+ 

uv project and package manager

Unix-like shell

This AI Agent can read files, write to files, and execute code in the working directory you provide to it. For testing purposes, the calculator directory was included in this repository.
To change the agent's working directory, edit line 23 in main.py 'function_call.args["working_directory"] = "./calculator"' and rename it to the desired directory.
