from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from processor import extract_receipt_data

app = FastAPI()

# IMPORTANT: This block allows your Frontend to talk to your Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permits all connections
    allow_credentials=True,
    allow_methods=["*"],  # Permits GET, POST, etc.
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Groq Receipt API is live!"}

@app.post("/process")
async def process_receipt(file: UploadFile = File(...)):
    try:
        content = await file.read()
        data = extract_receipt_data(content)
        return data
    except Exception as e:
        return {"error": str(e)}