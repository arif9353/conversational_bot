from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
import shutil
import os
from utils.process_ingestion_file import process_file
from pydantic import BaseModel
from langgraph_workflow import build_langgraph_workflow
import pandas as pd

app = FastAPI()

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = (".csv", ".xlsx", ".xls")

@app.post("/ingest")
async def ingest_file(file: UploadFile = File(...)):
    try:
        # ✅ Validate file type
        if not file.filename.endswith(ALLOWED_EXTENSIONS):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only CSV and Excel files are allowed"
            )

        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # ✅ Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ✅ Process file
        result = await process_file(file_path)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "File processed successfully",
                "columns": result["columns"],
                "preview": result["preview"],
                "context_saved": True
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal server error",
                "details": str(e)
            }
        )

class ChatReq(BaseModel):
    query: str
    session_id: str
    file_name: str

@app.post("/chat")
async def chat(req: ChatReq):
    try:
        user_query = req.query
        session_id = req.session_id
        df = pd.read_excel(f"uploads/{req.file_name}")
        with open("dataset_context.txt", "r", encoding="utf-8") as f:
            dataset_context = f.read()
        chain = await build_langgraph_workflow()
        state = await chain.ainvoke({
            "user_query": user_query,
            "data_context": dataset_context,
            "pandas_dataframe": df
        })
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "text": state["answer"],
                "base64": state["visualization_base64"]
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal server error",
                "details": str(e)
            }
        )
    