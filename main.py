from sys import argv


def main():
    import os
    import sys

    from dotenv import load_dotenv
    from google import genai
    from google.genai import types

    load_dotenv()

    # initial setup
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    user_prompt = sys.argv[1]
    # system prompt
    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. 

        You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory. You 
        do not need to specify the working directory in your function calls as 
        it is automatically injected for security reasons.
        """
    # setup prompt/repsonse objects
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description=(
            "Lists files in the specified directory along with their sizes, "
            "constrained to the working directory."
        ),
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

    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description=(
            "Get text from files in the specified directory along with their sizes, "
            "constrained to the working directory"
        ),
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="the path to the file"
                )
            },
        ),
    )

    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description=(
            """
            Run python files in the specified directory, constrained to the work directory.
        """
        ),
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description=(
                        """
                        The path to the file to run it.
                        """
                    ),
                ),
            },
        ),
    )

    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description=(
            """
            Write to python files given a directory and a filename, constrained to their
            working directory
        """
        ),
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="file_path to write to"
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="content to write to file"
                )
            },
        ),
    )

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if len(argv) > 2:
        print(f"User prompt: {user_prompt}")
        # print(f"Prompt tokens:{response.usage_metadata.prompt_token_count}")
        # print(f"Response tokens:{response.usage_metadata.candidates_token_count}")
    # print(response.text)
    if response.function_calls:
        for call in response.function_calls:
            print(f"Calling function: {call.name} ({call.args})")


if __name__ == "__main__":
    main()
