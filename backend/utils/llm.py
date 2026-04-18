from google import genai
from dotenv import load_dotenv
from utils.rate_limiter import rate_limiter
load_dotenv()
# import asyncio

client = genai.Client()


async def call_llm(prompt: str) -> str :
    try:
        await rate_limiter.wait_for_slot()
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview", contents=prompt
        )
        return response.text
    except Exception as e:
        print("Exception occured in call_llm() in llm.py as: ",e)
        raise e

# if __name__=="__main__":
#     prompt="hey whats up?"
#     async def _main():
#         resp = await call_llm(prompt)
#         print(resp)
#     asyncio.run(_main())