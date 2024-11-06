from fastapi import FastAPI, UploadFile, File, HTTPException
from utils.embeddings import get_embedding
from utils.storage import add_document, query_documents
import uuid

app = FastAPI()

@app.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()
    if file.content_type not in ["application/pdf", "text/plain", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    
    if file.filename.endswith(".txt"):
        text = content.decode('utf-8')
    else:
        
        text = "Extracted content from non-TXT file"  

    document_id = str(uuid.uuid4())
    embedding = get_embedding(text)
    
    add_document(document_id, text, embedding)

    return {"message": "Document added successfully", "document_id": document_id}

@app.get("/search/")
async def search_documents(query: str):
    query_embedding = get_embedding(query)
    results = query_documents(query_embedding)

    return {"results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
