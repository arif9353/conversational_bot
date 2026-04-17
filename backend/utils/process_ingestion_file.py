import pandas as pd
from agents.ingestion_agent import ingestion

async def process_file(file_path: str):
    # Load file
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    # Extract metadata
    columns = df.columns.tolist()
    sample_rows = df.head(10).to_dict(orient="records")
    dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}

    # Generate context using the Ingestion agent
    context = await ingestion(columns, sample_rows, dtypes)
    
    # Save context
    with open("dataset_context.txt", "w", encoding="utf-8") as f:
        f.write(context)

    return {
        "columns": columns,
        "preview": sample_rows,
        "context": context
    }