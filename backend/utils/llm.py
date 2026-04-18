from google import genai
import asyncio
from dotenv import load_dotenv
from utils.rate_limiter import rate_limiter
load_dotenv()

client = genai.Client()


async def call_llm(prompt: str) -> str :
    await rate_limiter.wait_for_slot()
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview", contents=prompt
    )
    return response.text


if __name__=="__main__":
    prompt="hey whats up?"
    async def _main():
        resp = await call_llm(prompt)
        print(resp)
    asyncio.run(_main())