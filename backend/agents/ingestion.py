
from utils.llm import call_llm

async def ingestion(columns, sample_rows, dtypes) -> str:
    try:

        prompt = f"""
            You are a strict data schema analyzer.

            Your task is to analyze a dataset and return ONLY a concise structured summary.

            ### Rules (MUST FOLLOW):
            - DO NOT add sections like use cases, insights, or analysis
            - DO NOT write long paragraphs
            - DO NOT explain beyond what is asked
            - Keep everything concise and structured
            - Output must strictly follow the format below

            ### Output Format:

            DATASET_DESCRIPTION:
            <Describing what the dataset represents>

            COLUMNS:
            - <column_name>(<dataType>): <short explanation of the column with an example value>
            - <column_name>(<dataType>): <short explanation of the column with an example value>
            ...

            ### Input:

            Columns:
            {columns}

            Data Types:
            {dtypes}

            Sample Data:
            {sample_rows}
            """
        return await call_llm(prompt)
    
    except Exception as e:
        print("Exception occured in ingestion() in ingestion.py as: ",e)
        raise e