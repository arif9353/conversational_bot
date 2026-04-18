import matplotlib.pyplot as plt
import base64
from io import BytesIO
# from agents.pandas_query_executor import pandas_query_executor
# from utils.visualization_data_format import format_data_for_visualization
# import pandas as pd

def generate_chart(formatted_data: dict, chart_type: str):
    try:
        plt.figure()

        if chart_type == "bar":
            plt.bar(formatted_data["x"], formatted_data["y"])

        elif chart_type == "horizontal_bar":
            plt.barh(formatted_data["x"], formatted_data["y"])

        elif chart_type == "line":
            plt.plot(formatted_data["x"], formatted_data["y"])

        elif chart_type == "scatter":
            plt.scatter(formatted_data["x"], formatted_data["y"])

        elif chart_type == "pie":
            plt.pie(
                formatted_data["values"],
                labels=formatted_data["labels"],
                autopct="%1.1f%%"
            )

        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)

        img_str = base64.b64encode(buffer.read()).decode("utf-8")
        plt.close()

        return img_str

    except Exception as e:
        print("Exception occured in generate_chart() in generate_visualization_chart.py as: ",e)
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
#         formatted_data = format_data_for_visualization(query_result, "line")
#         base64 = generate_chart(formatted_data, "line")
#         with open("base64format_image.txt", "w", encoding="utf-8") as f:
#             f.write(base64) 

#     _main()   