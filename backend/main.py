from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
import shutil
import os

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

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "File processed successfully"
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

class ChatReq:
    query: str
    session_id: str

@app.post("/chat")
async def chat(req: ChatReq):
    try:
        user_query = req.query
        session_id = req.session_id

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "File processed successfully"
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
    




