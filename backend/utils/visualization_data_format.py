# import pandas as pd
# from agents.pandas_query_executor import pandas_query_executor

import numbers

def format_data_for_visualization(result: dict, chart_type: str):
    try:
        if not result:
            return None

        # -------------------------
        # SERIES
        # -------------------------
        if result["type"] == "series":
            x = result.get("index", list(range(len(result["data"]))))
            y = result["data"]

            x = x[:20]
            y = y[:20]

            if chart_type == "pie":
                return {
                    "labels": x,
                    "values": y
                }

            return {
                "x": x,
                "y": y
            }

        # -------------------------
        # DATAFRAME (FIXED PROPERLY)
        # -------------------------
        if result["type"] == "dataframe":
            rows = result["data"]

            if not rows:
                return None

            keys = list(rows[0].keys())

            if len(keys) < 2:
                return None

            rows = rows[:20]

            # 🔥 Detect numeric vs categorical
            x_key = None
            y_key = None

            for key in keys:
                if isinstance(rows[0][key], numbers.Number):
                    y_key = key
                else:
                    x_key = key

            if not x_key or not y_key:
                return None

            x = [row[x_key] for row in rows]
            y = [row[y_key] for row in rows]

            # 🔥 PIE FIX
            if chart_type == "pie":
                return {
                    "labels": x,   # categorical
                    "values": y    # numeric
                }

            return {
                "x": x,
                "y": y
            }

        return None

    except Exception as e:
        print("Error in format_data_for_visualization:", e)
        return None
    
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