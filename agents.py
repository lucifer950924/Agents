from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).parent / ".env")
from groq import Groq
def create_agent(prompt: str, input):
    client = Groq()
    completion = client.chat.completions.create(
        model = "openai/gpt-oss-120b",
        messages= [
            {
                "role" : "system",
                "content" : prompt
            },
            {
                "role" : "user",
                "content" : f"You are an agent for the specific purpose: {input}"
            }
        ],
        temperature = 0.1,
        reasoning_effort= "medium"

    )

    return completion.choices[0].message.content
