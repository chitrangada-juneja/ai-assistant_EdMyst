from fastapi import FastAPI, UploadFile, File,Form
from fastapi.middleware.cors import CORSMiddleware
import shutil, os
from config import UPLOAD_DIR
from models.request_models import QueryRequest
from pathlib import Path
from agents.edy_agent import query_agent
from models.request_models import QueryRequest


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

index, chunks = None, []



@app.post("/upload")
async def upload_message_and_file(
    message: str = Form(...),
    file: UploadFile = File(None)
):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_location = None
    if file:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)

    # Call query_agent immediately with optional PDF
    pdf_filename = Path(file_location).name if file_location else None
    answer = query_agent(message, pdf_filename=pdf_filename)

    return {
        "message": message,
        "filename": file.filename if file else None,
        "file_path": file_location,
        "answer": answer
    }


@app.post("/query")
def query(req: QueryRequest):
    """
    Accepts a user query, retrieves relevant chunks, and returns a short answer.
    """
    answer = query_agent(req.query)
    return {"answer": answer}
