import pandas as pd
import numpy as np
from typing_extensions import Any
# import asyncio
# from agents.pandas_query_generator import pandas_query_generator

# 🚫 Forbidden patterns
FORBIDDEN_KEYWORDS = [
    "__", "import", "exec", "eval", "open", "os", "sys",
    "subprocess", "lambda", "while", "for", "class", "def"
]


def is_safe_expression(expr: str) -> bool:
    expr_lower = expr.lower()
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in expr_lower:
            return False
    return True


def pandas_query_executor(df: pd.DataFrame, pandas_expr: str):
    try:
        # ✅ Safety check
        if not is_safe_expression(pandas_expr):
            raise ValueError("Unsafe expression detected")

        # ✅ Restricted globals
        allowed_globals = {
            "df": df,
            "pd": pd
        }

        # ❗ No builtins
        result = eval(pandas_expr, {"__builtins__": {}}, allowed_globals)

        # ✅ Normalize output
        normalized_result = normalize_result(result)
        return normalized_result

    except Exception as e:
        print("Exception occured in pandas_query_executor() in pandas_query_executor.py as: ", e)
        raise e


def dataframe_to_json(df, max_rows=50) -> dict:
    summary = {
        "row_count": len(df),
        "columns": list(df.columns)
    }

    sample = df.head(max_rows).reset_index()

    return {
        "type": "dataframe",
        "summary": summary,
        "data": sample.to_dict(orient="records")
    }


def normalize_result(result: Any) -> dict:
    try:
        if isinstance(result, pd.DataFrame):
            return dataframe_to_json(result)

        elif isinstance(result, pd.Series):
            return {
                "type": "series",
                "index": result.index.tolist(),
                "data": result.tolist(),
                "name": result.name
            }

        elif isinstance(result, np.generic):
            return {
                "type": "scalar",
                "data": result.item()
            }

        elif isinstance(result, (int, float, str, bool)):
            return {
                "type": "scalar",
                "data": result
            }

        return {
            "type": "unknown",
            "data": str(result)
        }

    except Exception as e:
        print("Exception occured in normalize_result() in pandas_query_executor.py as: ", e)
        raise e
    

# if __name__=="__main__":
#     async def _main():
#         df = pd.read_excel("uploads/Route_Input_file (1).xlsx")
#         user_query = "Find the maximum value in the 'Total Qty' column."
#         with open("dataset_context.txt", "r", encoding="utf-8") as f:
#             dataset_context = f.read()
#         # pandas_expr = await pandas_query_generator(user_query, dataset_context)
#         pandas_expr = """df[df["From Location"] == "SBPPC - Guwahati"].groupby("Date of truck release")["Total Qty"].sum()"""
#         # print(pandas_expr)
#         resp = pandas_query_executor(df, pandas_expr)
#         print(resp)

#     asyncio.run(_main())
