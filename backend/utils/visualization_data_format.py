# import pandas as pd
# from agents.pandas_query_executor import pandas_query_executor

def format_data_for_visualization(result: dict, chart_type: str):
    try:
        if result["type"] == "scalar":
            return None

        # ✅ SERIES (FIXED)
        if result["type"] == "series":
            x = result.get("index", list(range(len(result["data"]))))
            y = result["data"]

            # limit size
            x = x[:20]
            y = y[:20]

            # PIE special case
            if chart_type == "pie":
                return {
                    "labels": x,
                    "values": y
                }

            return {
                "x": x,
                "y": y
            }

        # DATAFRAME (same as before)
        if result["type"] == "dataframe":
            rows = result["data"]
            cols = result["summary"]["columns"]

            if len(cols) < 2:
                return None

            rows = rows[:20]

            x = [row[cols[0]] for row in rows]
            y = [row[cols[1]] for row in rows]

            if chart_type == "pie":
                return {
                    "labels": x,
                    "values": y
                }

            return {
                "x": x,
                "y": y
            }

        return None

    except Exception as e:
        print("Exception occured in format_data_for_visualization() in visualization_data_format.py as: ", e)
        raise e
    
# if __name__=="__main__":
#     def _main():
#         df = pd.read_excel("uploads/Route_Input_file (1).xlsx")
#         user_query = "Provide me the total quantity of order for each day going from 'SBPPC - Guwahati'"
#         with open("dataset_context.txt", "r", encoding="utf-8") as f:
#             dataset_context = f.read()
#         # pandas_expr = await pandas_query_generator(user_query, dataset_context)
#         pandas_expr = """df[df["From Location"] == "SBPPC - Guwahati"].groupby("Date of truck release")["Total Qty"].sum()"""
#         # print(pandas_expr)
#         query_result = pandas_query_executor(df, pandas_expr)
#         resp = format_data_for_visualization(query_result, "line")
#         print(resp)
    
#     _main()