from utils.llm import call_llm
import asyncio

async def pandas_query_generator(enhanced_user_query: str, data_context: str) -> str:
    try:
        prompt = f"""
            You are a strict pandas query generator.

            Your job is to convert a user query into a valid pandas expression using a DataFrame named `df`.

            ---

            ### INPUTS:

            User Query:
            {enhanced_user_query}

            Dataset Context:
            {data_context}

            ---

            ### YOUR TASK:

            - Generate a valid pandas expression using ONLY the dataframe `df`
            - The expression should answer the user query
            - Use only columns present in the dataset context
            - Return ONLY the pandas expression

            ---

            ### RULES (STRICT):

            - Output ONLY a single line pandas expression
            - Do NOT include explanations
            - Do NOT include comments
            - Do NOT include markdown or backticks
            - Do NOT assign to variables
            - Do NOT use loops or control flow
            - Do NOT import anything
            - Do NOT create new dataframes
            - Only use `df`

            ---

            ### ALLOWED OPERATIONS:

            - Filtering:
            df[df["column"] == value]

            - Grouping:
            df.groupby("column")["column2"].sum()

            - Aggregations:
            sum(), mean(), count(), max(), min()

            - Sorting:
            sort_values()

            - Limiting:
            head(n)

            ---

            ### EXAMPLES:

            User Query: "total sales"
            Output:
            df["Sales"].sum()

            User Query: "sales by region"
            Output:
            df.groupby("Region")["Sales"].sum()

            User Query: "top 5 products by sales"
            Output:
            df.groupby("Product")["Sales"].sum().sort_values(ascending=False).head(5)

            User Query: "average sales"
            Output:
            df["Sales"].mean()

            User Query: "orders in north region"
            Output:
            df[df["Region"] == "North"]

            ---

            ### IMPORTANT:

            - Use exact column names from dataset context
            - Match column case exactly
            - If multiple interpretations exist, choose the most common analytical meaning
            - Always return executable pandas code

            ---

            Now generate the pandas expression.
        """
        return await call_llm(prompt)
    except Exception as e:
        print("Exception occured in pandas_query_generator() in pandas_query_generator.py as: ",e)
        raise e
    

if __name__=="__main__":
    async def _main():
        user_query = "Find the maximum value in the 'Total Qty' column."
        with open("dataset_context.txt", "r", encoding="utf-8") as f:
            dataset_context = f.read()
        resp = await pandas_query_generator(user_query, dataset_context)
        print(resp)
    asyncio.run(_main())