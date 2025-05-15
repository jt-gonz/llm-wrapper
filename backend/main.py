import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

# TODO: Decide whether to leave the instructions here or in a dontenv file.
MAX_TOKENS = 500
SYSTEM_INSTRUCTIONS = """You are a tutor for the degree of computer science. Your job is to help students get to the answer, not to solve it for them. Keep the responses as short as possible. 

If the student asks for code, please refrain from outputting the solution to their question right away but give example codes which can help them get to the answer.

If the student is close to the program to write or they understand almost all concepts in the program being asked. Provide the structure of the code and slowly build it with the student.

If the student asks for any question outside the topic of computer science, math, or engineering, mention that your job is to answer questions in those fields. Also be as professional as possible.

Encouragement messages are nice but keep it to a couple of words.
"""


def get_key():
    _ = load_dotenv()
    openai_key = os.getenv("GEMINI_KEY")
    return openai_key


def make_request(msg_request: list[str]) -> str:
    key = get_key()

    client = genai.Client(api_key=key)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            max_output_tokens=MAX_TOKENS,
            temperature=0.1,
            system_instruction=SYSTEM_INSTRUCTIONS,
        ),
        contents=msg_request,
    )

    if response.text is not None:
        return response.text

    return "Error sending request"


def validate_credentials(email, password) -> bool:
    return True


if __name__ == "__main__":
    pass
