from utils.llm import call_llm
import json
# import asyncio

async def input_guardrail(user_query: str, data_context: str, conversation_history: str) -> str:
    try:
        prompt = f"""
            You are a strict query processor for a data assistant system.

            You are given:
            1. Dataset context (what data is available)
            2. Conversation history (previous user and assistant messages)
            3. Current user query

            ---

            ### YOUR RESPONSIBILITIES:

            You must ALWAYS do the following:

            1. Rewrite the user query into a fully clear, standalone query using:
            - Conversation history
            - Dataset context

            This rewritten query will be used by downstream systems.

            2. Decide whether:
            - The query can be answered directly (without data processing), OR
            - It needs to go to the data pipeline

            ---

            ### OUTPUT FORMAT (STRICT JSON ONLY):

            {{
            "isContinue": <true or false>,
            "contextualized_user_query": "<fully rewritten standalone query>",
            "query": "<final answer OR empty string>"
            }}

            ---

            ### DECISION RULES (VERY IMPORTANT):

            #### CASE 1: Answer from conversation history
            If the user is asking about something already discussed in the conversation:
            - Answer using ONLY the conversation history
            - DO NOT perform any new calculations
            - DO NOT use dataset knowledge
            - isContinue = false
            - query = answer from conversation

            Examples:
            - "what did you say earlier?"
            - "what was the max quantity?"
            - "which location were we discussing?"

            ---

            #### CASE 2: Greeting
            If the query is a greeting:
            - Respond politely
            - isContinue = false
            - query = greeting response

            Examples:
            - "hi", "hello", "hey"

            ---

            #### CASE 3: Out of scope
            If the query is unrelated to the dataset:
            - isContinue = false
            - query = "I can't answer this question as it is out of data scope."

            Examples:
            - "who is the prime minister?"
            - "write a poem"

            ---

            #### CASE 4: Data-related query (needs processing)
            If the query requires accessing or computing from the dataset:
            - isContinue = true
            - query = "" (empty string)

            IMPORTANT:
            - DO NOT answer these queries yourself
            - Always pass them forward

            Examples:
            - aggregations
            - filtering
            - comparisons
            - trends
            - calculations

            ---

            ### CONTEXTUALIZATION RULES:

            - Resolve references using conversation:
            - "that", "it", "those", "next day", "previous", etc.
            - Fill missing details ONLY if clearly available in conversation
            - DO NOT hallucinate missing values
            - DO NOT change the intent of the query
            - Keep it precise and useful for generating a pandas query

            ---

            ### IMPORTANT CONSTRAINTS:

            - DO NOT generate pandas code
            - DO NOT explain anything
            - DO NOT include extra text outside JSON
            - DO NOT hallucinate answers
            - ALWAYS return valid JSON

            ---

            ### INPUT:

            Conversation:
            {conversation_history}

            Dataset Context:
            {data_context}

            User Query:
            {user_query}
        """
        raw_content = await call_llm(prompt)
        if raw_content.startswith("```"):
            raw_content = raw_content[3:]
        if raw_content.startswith("json"):
            raw_content = raw_content[4:]
        if raw_content.endswith("```"):
            raw_content = raw_content[:-3]
        return json.loads(raw_content)
    except Exception as e:
        print("Exception occured in input_guardrail() in input_guardrail.py as: ",e)
        raise e
    

# if __name__=="__main__":
#     async def _main():
#         with open("dataset_context.txt", "r", encoding="utf-8") as f:
#             data_context = f.read()
#         resp = await input_guardrail("Can you tell me about the maximum quantity of order in the list?", data_context)
#         print(resp)
    
#     asyncio.run(_main())