from utils.llm import call_llm
import json, asyncio
import pandas as pd
from agents.pandas_query_executor import pandas_query_executor

async def visualization(user_query: str, pandas_query: str, query_result: dict, data_context: str) -> str:
    try:
        prompt = f"""
            You are an AI assistant that recommends appropriate data visualizations. Based on the user's question, Pandas query, query results, and the dataset context(info about columns etc) suggest the most suitable type of graph or chart to visualize the data. If no visualization is appropriate, indicate that.

            ### INPUT:
            User Question:
            {user_query}

            Pandas Query:
            {pandas_query}

            Query Results:
            {query_result}

            Dataset Context:
            {data_context}

            Available chart types and their use cases:

            - Bar Graphs: Best for comparing categorical data or showing changes over time when categories are discrete and the number of categories is more than 2. Use for questions like "What are the sales figures for each product?" or "How does the population of cities compare? or "What percentage of each city is male?"
            - Horizontal Bar Graphs: Best for comparing categorical data or showing changes over time when the number of categories is small or the disparity between categories is large. Use for questions like "Show the revenue of A and B?" or "How does the population of 2 cities compare?" or "How many men and women got promoted?" or "What percentage of men and what percentage of women got promoted?" when the disparity between categories is large.
            - Scatter Plots: Useful for identifying relationships or correlations between two numerical variables or plotting distributions of data. Best used when both x axis and y axis are continuous. Use for questions like "Plot a distribution of the fares (where the x axis is the fare and the y axis is the count of people who paid that fare)" or "Is there a relationship between advertising spend and sales?" or "How do height and weight correlate in the dataset? Do not use it for questions that do not have a continuous x axis."
            - Pie Charts: Ideal for showing proportions or percentages within a whole. Use for questions like "What is the market share distribution among different companies?" or "What percentage of the total revenue comes from each product?"
            - Line Graphs: Best for showing trends and distributionsover time. Best used when both x axis and y axis are continuous. Used for questions like "How have website visits changed over the year?" or "What is the trend in temperature over the past decade?". Do not use it for questions that do not have a continuous x axis or a time based x axis.

            Consider these types of questions when recommending a visualization:

            1. Aggregations and Summarizations (e.g., "What is the average revenue by month?" - Line Graph)

            2. Comparisons (e.g., "Compare the sales figures of Product A and Product B over the last year." - Line or Column Graph)

            3. Plotting Distributions (e.g., "Plot a distribution of the age of users" - Scatter Plot)

            4. Trends Over Time (e.g., "What is the trend in the number of active users over the past year?" - Line Graph)

            5. Proportions (e.g., "What is the market share of the products?" - Pie Chart)

            6. Correlations (e.g., "Is there a correlation between marketing spend and revenue?" - Scatter Plot)

            Provide your response in the following JSON format:
            {{
                "recommended_visualization": "<Chart type or "None". ONLY use the following names: bar, horizontal_bar, line, pie, scatter, none>",
                "reason" : "<Brief explanation for your recommendation>"
            }}
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
        print("Exception occured in visualization() in visualization.py as: ",e)
        raise e
    

if __name__=="__main__":
    async def _main():
        df = pd.read_excel("uploads/Route_Input_file (1).xlsx")
        user_query = "Provide me the total quantity of order for each day going from 'SBPPC - Guwahati'"
        with open("dataset_context.txt", "r", encoding="utf-8") as f:
            dataset_context = f.read()
        # pandas_expr = await pandas_query_generator(user_query, dataset_context)
        pandas_expr = """df[df["From Location"] == "SBPPC - Guwahati"].groupby("Date of truck release")["Total Qty"].sum()"""
        # print(pandas_expr)
        query_result = pandas_query_executor(df, pandas_expr)
        print(query_result)
        resp = await visualization(user_query, pandas_expr, query_result, dataset_context)
        print(resp)

    asyncio.run(_main())