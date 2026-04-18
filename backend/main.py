from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil, json, os
from utils.process_ingestion_file import process_file
from pydantic import BaseModel
from langgraph_workflow import build_langgraph_workflow
import pandas as pd
from utils.llm import call_llm
from utils.print_langgraph_state import print_state

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

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
                "context": result["context"],
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


async def summarize_text(text: str) -> str:
    prompt = f"""
You are a conversation memory compressor.

Your job is to extract ONLY important structured information from the conversation.

STRICT RULES:
- Do NOT include instructions or meta text
- Do NOT include greetings or filler
- Do NOT explain anything
- Only extract facts useful for future queries

Return STRICT JSON ONLY:

{{
  "goals": ["What the user is trying to achieve"],
  "entities": ["Locations, names, columns, etc"],
  "constraints": ["Filters, conditions, time ranges"],
  "insights": ["Important results already computed"]
}}

Conversation:
{text}
"""

    response = await call_llm(prompt)

    # ✅ Clean markdown if model adds it
    if response.startswith("```"):
        response = response.strip("```")
    if response.startswith("json"):
        response = response[4:]

    try:
        parsed = json.loads(response)
    except Exception:
        # fallback: store raw text safely
        parsed = {
            "goals": [],
            "entities": [],
            "constraints": [],
            "insights": [text[:200]]
        }

    return json.dumps(parsed, ensure_ascii=False)


class SmartChatHistory:
    def __init__(self):
        self.summary = {
            "goals": [],
            "entities": [],
            "constraints": [],
            "insights": []
        }
        self.recent_messages = []
        self.max_messages = 4

    async def add_user_message(self, message: str):
        self.recent_messages.append({"role": "user", "text": message})

    async def add_ai_message(self, message: str):
        self.recent_messages.append({"role": "assistant", "text": message})
        await self._compact_history()

    async def _compact_history(self):
        """
        When messages reach 6:
        - Take first 2
        - Summarize them
        - Merge into structured summary
        - Keep last 4
        """
        if len(self.recent_messages) == 6:

            first_two = self.recent_messages[:2]

            two_msgs_text = "\n".join(
                f"{m['role']}: {m['text']}" for m in first_two
            )

            try:
                new_summary_raw = await summarize_text(two_msgs_text)
                new_summary = json.loads(new_summary_raw)
            except Exception:
                return  # fail silently, don't break flow

            # ✅ Merge summaries (deduplicated)
            for key in self.summary:
                existing = set(self.summary.get(key, []))
                incoming = set(new_summary.get(key, []))
                merged = list(existing.union(incoming))

                # limit size per section
                self.summary[key] = merged[:10]

            # keep only last 4 messages
            self.recent_messages = self.recent_messages[2:]

    def dump_for_llm(self):
        """
        Returns structured + recent context
        """
        context = ""

        # ✅ Structured memory
        if any(self.summary.values()):
            context += "### Conversation Memory (Facts)\n"
            context += json.dumps(self.summary, indent=2)
            context += "\n\n"

        # ✅ Recent conversation
        context += "### Recent Conversation\n"
        for msg in self.recent_messages:
            context += f"{msg['role']}: {msg['text']}\n"

        return context


store = {}

def get_session_history(session_id: str) -> SmartChatHistory:
    if session_id not in store:
        store[session_id] = SmartChatHistory()
    return store[session_id]


class ChatReq(BaseModel):
    query: str
    session_id: str
    file_name: str
    dataset_context: str


@app.post("/chat")
async def chat(req: ChatReq):
    try:
        user_query = req.query
        session_id = req.session_id
        df = pd.read_excel(f"uploads/{req.file_name}")
        dataset_context = req.dataset_context
        chain = await build_langgraph_workflow()
        history = get_session_history(session_id)
        full_context = history.dump_for_llm()
        state = await chain.ainvoke({
            "user_query": user_query,
            "data_context": dataset_context,
            "conversation_history": full_context,
            "pandas_dataframe": df,
            "visualization_base64": ""
        })
        await history.add_user_message(user_query)
        await history.add_ai_message(state["answer"])
        print_state(state)
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
    