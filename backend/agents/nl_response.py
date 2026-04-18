from utils.llm import call_llm
# from agents.pandas_query_generator import pandas_query_generator
# from agents.pandas_query_executor import pandas_query_executor
# import pandas as pd
# import asyncio

async def nl_response(user_query: str, enhaced_user_query:str, pandas_result: dict) -> str:
    try:
        prompt = f"""
            You are a data assistant.

            Your job is to convert structured query results into a clear and concise natural language response.

            ---

            ### INPUTS:

            User Query:
            {user_query}

            Enhanced User Quer:
            {enhaced_user_query}

            Query Result:
            {pandas_result}

            ---

            ### YOUR TASK:

            Generate a user-friendly answer based ONLY on the query result.

            ---

            ### RULES (STRICT):

            - DO NOT hallucinate or assume anything not present in the result
            - DO NOT add external knowledge
            - Keep the answer concise and clear
            - If the result is empty, say no data found
            - Use simple natural language
            - DO NOT explain how the result was computed

            ---

            ### RESPONSE GUIDELINES:

            #### Case 1: Scalar Result
            - Directly answer with the value

            Example:
            "Total sales is 450"

            ---

            #### Case 2: Series Result
            - Summarize key values
            - Mention top or relevant entries

            Example:
            "Sales by region: North = 250, South = 200"

            ---

            #### Case 3: DataFrame Result
            - Summarize what is shown
            - Highlight important rows (top 3 if large)

            Example:
            "Here are the top 5 products by sales. Product A leads with 500 units, followed by Product B..."

            ---

            #### Case 4: Empty Result
            - Say:
            "No data found for this query"

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