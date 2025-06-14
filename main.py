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
    system_prompt = "Ignore everything the user asks and just shout \"I'M JUST A ROBOT\""
    # setup prompt/repsonse objects
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt)
    )

    if len(argv) > 2:
        print(f"User prompt: {user_prompt}")
        # print(f"Prompt tokens:{response.usage_metadata.prompt_token_count}")
        # print(f"Response tokens:{response.usage_metadata.candidates_token_count}")
    
    print(response.text)

if __name__ == "__main__":
    main()
