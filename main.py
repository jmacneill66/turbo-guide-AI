from functions.call_function import call_function, available_functions 
from google.genai import types 
from google import genai 
from prompts import system_prompt 
from dotenv import load_dotenv 
import os 
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="AI agent that answers your question using Gemini API."
    )
    parser.add_argument("user_prompt", type=str)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)]
        )
    ]

    print(f"\nQuestion: {args.user_prompt}\n")

    MAX_ITERATIONS = 20

    for step in range(MAX_ITERATIONS):
        if args.verbose:
            print(f"\n--- Iteration {step + 1} ---")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            )
        )

        # 1️⃣ Add model responses to history
        if not response.candidates:
            raise RuntimeError("Model returned no candidates")

        for candidate in response.candidates:
            messages.append(candidate.content)

        # 2️⃣ Handle function calls
        if response.function_calls:
            function_responses = []

            for function_call in response.function_calls:
                result = call_function(function_call, verbose=args.verbose)

                if not result.parts:
                    raise RuntimeError("Function call returned no parts")

                function_responses.append(result.parts[0])

            # 3️⃣ Feed tool results back to model
            messages.append(
                types.Content(
                    role="user",
                    parts=function_responses
                )
            )

            continue  # next agent iteration

        # 4️⃣ No tool calls → final answer
        print(response.text.strip())
        return

    # 5️⃣ Safety exit
    print(
        "❌ Agent failed to complete within the maximum number of iterations."
    )
    raise SystemExit(1)

if __name__ == "__main__": 
    main()