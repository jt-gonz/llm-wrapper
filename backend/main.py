import os

from dotenv import load_dotenv
from google import genai


def get_key():
    _ = load_dotenv()
    openai_key = os.getenv("GEMINI_KEY")
    return openai_key


def make_request(msg_request: str) -> str:
    key = get_key()

    client = genai.Client(api_key=key)
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=msg_request
    )

    if response.text is not None:
        return response.text

    return "Error sending request"


if __name__ == "__main__":
    pass
