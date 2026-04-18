from google import genai
import asyncio
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()


async def call_llm(prompt: str) -> str :
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite", contents=prompt
    )
    return response.text


if __name__=="__main__":
    prompt="hey whats up?"
    async def _main():
        resp = await call_llm(prompt)
        print(resp)
    asyncio.run(_main())