from utils.llm import call_llm
# from agents.pandas_query_generator import pandas_query_generator
# from agents.pandas_query_executor import pandas_query_executor
# import pandas as pd
# import asyncio

async def nl_response(user_query: str, enhaced_user_query:str, pandas_result: dict) -> str:
    try:
        prompt = f"""
            You are a data assistant.

            Your job is to convert structured query results into a clear, slightly descriptive, and user-friendly natural language response.

            ---

            ### INPUTS:

            User Query:
            {user_query}

            Enhanced User Query:
            {enhaced_user_query}

            Query Result:
            {pandas_result}

            ---

            ### YOUR TASK:

            Generate a helpful and natural response based ONLY on the query result.

            The response should not be just a raw value — it should provide context and readability.

            ---

            ### RULES (STRICT):

            - DO NOT hallucinate or assume anything not present in the result
            - DO NOT add external knowledge
            - DO NOT explain how the result was computed
            - Keep the response concise BUT informative
            - Add clarity where useful (e.g., what the value represents)

            ---

            ### RESPONSE GUIDELINES:

            #### Case 1: Scalar Result
            - Mention what the value represents
            - Make it sound complete

            Example:
            "Total sales amount to 450 units."

            ---

            #### Case 2: Series Result
            - Present key values clearly
            - Mention top or most relevant entries
            - If many values → summarize (top 3–5)

            Example:
            "Sales vary across regions, with North leading at 250 units, followed by South at 200 units."

            ---

            #### Case 3: DataFrame Result
            - Describe what the table represents
            - Highlight key insights (top rows, max/min, patterns)
            - Avoid dumping raw data

            Example:
            "The top products by sales show that Product A leads with 500 units, followed by Product B and Product C."

            ---

            #### Case 4: Empty Result
            - Say:
            "No data found for this query."

            ---

            ### STYLE GUIDELINES:

            - Use natural, conversational tone
            - Avoid robotic phrasing
            - Prefer complete sentences over fragments
            - Add slight interpretation ONLY if directly supported by data

            ---

            ### OUTPUT:

            Return ONLY the final answer as plain text.
        """
        return await call_llm(prompt)
    except Exception as e:
        print("Exception occured in nl_response() in nl_response.py as: ",e)
        raise e
    

# if __name__=="__main__":
#     async def _main():
#         df = pd.read_excel("uploads/Route_Input_file (1).xlsx")
#         enhaced_user_query = "Find the maximum value in the 'Total Qty' column."
#         user_query = "Can you tell me about the maximum quantity of order in the list?"
#         with open("dataset_context.txt", "r", encoding="utf-8") as f:
#             dataset_context = f.read()
#         pandas_expr = await pandas_query_generator(enhaced_user_query, dataset_context)
#         print(pandas_expr)
#         pandas_result = pandas_query_executor(df, pandas_expr)
#         print(pandas_result)
#         nl_resp = await nl_response(user_query, enhaced_user_query, pandas_result)
#         print(nl_resp)

#     asyncio.run(_main())