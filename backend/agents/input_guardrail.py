from utils.llm import call_llm
import json, asyncio

async def input_guardrail(user_query: str, data_context: str) -> str:
    try:
        prompt = f"""
            You are a strict input guardrail agent for a data analysis system.

            Your job is to decide whether a user query:
            1. Should proceed for data processing
            2. Should be rejected
            3. Can be directly answered using dataset context

            ---

            ### INPUTS:

            User Query:
            {user_query}

            Dataset Context:
            {data_context}

            ---

            ### YOUR TASK:

            You must choose ONE of the following:

            ---

            ### CASE 1: CONTINUE (isContinue = true)
            If the query:
            - Requires data computation (sum, avg, count, groupby, filter, etc.)
            - Needs processing on dataset

            Then:
            - Rewrite the query into a clearer, structured form

            ---

            ### CASE 2: DIRECT ANSWER (isContinue = false)
            If the query:
            - Can be answered directly from dataset context
            - Requires NO computation

            Examples:
            - column names
            - dataset description
            - meaning of a column

            Then:
            - Answer directly using the dataset context

            ---

            ### CASE 3: REJECT (isContinue = false)
            If the query:
            - Is a greeting → respond politely
            - Is unrelated to dataset → respond:
            "I can't answer this question based on the provided data"

            ---

            ### RULES (STRICT):

            - Do NOT hallucinate information not present in dataset context
            - Do NOT perform calculations yourself
            - Do NOT answer questions requiring aggregation or filtering
            - Only answer directly if information is explicitly available
            - Keep responses concise
            - Do NOT explain reasoning

            ---

            ### OUTPUT FORMAT (STRICT JSON ONLY):

            {{ 
            "isContinue": <true or false>,
            "query": "<rewritten query OR final response>"
            }}

            ---

            ### EXAMPLES:

            User Query: "hi"
            Output:
            {{"isContinue": false, "query": "Hello! How can I help you with your data?"}}

            User Query: "What columns are present?"
            Output:
            {{"isContinue": false, "query": "The dataset contains columns: ..."}}

            User Query: "What is the weather today?"
            Output:
            {{"isContinue": false, "query": "I can't answer this question based on the provided data"}}

            User Query: "sales by region"
            Output:
            {{"isContinue": true, "query": "Calculate total sales grouped by region"}}

            User Query: "average sales last month"
            Output:
            {{"isContinue": true, "query": "Calculate average sales for the last month"}}

            ---

            Now produce the output.
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
    

if __name__=="__main__":
    async def _main():
        with open("dataset_context.txt", "r", encoding="utf-8") as f:
            data_context = f.read()
        resp = await input_guardrail("What is the temperature?", data_context)
        print(resp)
    
    asyncio.run(_main())