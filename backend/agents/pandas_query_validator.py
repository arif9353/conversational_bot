from utils.llm import call_llm
# import asyncio

async def pandas_query_validator(enhanced_user_query: str, data_context: str, pandas_expr: str) -> str:
    try:
        prompt = f"""
            You are a strict pandas query validator and enhancer.

            Your job is to:
            1. Validate the correctness of a pandas query
            2. Improve the output to make it more informative (if needed)
            3. Preserve the original intent of the query

            ---

            ### INPUTS:

            User Query:
            {enhanced_user_query}

            Generated Pandas Query:
            {pandas_expr}

            Dataset Context:
            {data_context}

            ---

            ### YOUR TASK:

            You must analyze the given pandas query and:

            ### STEP 1: VALIDATE
            - Ensure the query is valid pandas syntax
            - Ensure it uses only the dataframe `df`
            - Ensure it uses valid column names from dataset context

            ---

            ### STEP 2: ENHANCE (VERY IMPORTANT)

            Improve the query ONLY IF it lacks useful output.

            #### Apply these rules:

            1. If query returns ONLY a single identifier (e.g., City, Product):
            → Include the associated metric column as well

            Example:
            ❌ df.loc[df["Demand"].idxmax(), "City"]  
            ✔ df.loc[[df["Demand"].idxmax()], ["City", "Demand"]]

            ---

            2. If query returns scalar but can be more informative:
            → Prefer tabular output if it adds clarity

            ---

            3. If query uses idxmax / idxmin:
            → Always return a row (DataFrame), not a single value

            ---

            4. If query already returns a DataFrame with meaningful columns:
            → KEEP IT UNCHANGED

            ---

            5. If query is already optimal:
            → RETURN AS IS

            ---

            ### STRICT RULES:

            - DO NOT change the intent of the query
            - DO NOT introduce new logic
            - DO NOT guess missing columns
            - DO NOT add unnecessary columns
            - DO NOT add explanations

            ---

            ### OUTPUT FORMAT:

            Return ONLY the final pandas expression.

            No explanation. No markdown. No comments.

            ---

            ### EXAMPLES:

            Input:
            df.loc[df["Demand"].idxmax(), "City"]

            Output:
            df.loc[[df["Demand"].idxmax()], ["City", "Demand"]]

            ---

            Input:
            df["Sales"].sum()

            Output:
            df["Sales"].sum()

            ---

            Input:
            df.groupby("City")["Demand"].sum()

            Output:
            df.groupby("City")["Demand"].sum()

            ---

            Now validate and improve the query.
        """
        return await call_llm(prompt)
    except Exception as e:
        print("Exception occured in pandas_query_validator() in pandas_query_validator.py as: ",e)
        raise e
    
