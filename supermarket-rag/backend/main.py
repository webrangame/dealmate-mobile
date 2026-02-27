from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Request, BackgroundTasks, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
import shutil
import os
from rag_engine import rag_engine
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import StreamingResponse
from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

description = """
## 🚀 What is this API?
This is an advanced AI-powered backend service designed to ingest, process, and query supermarket product catalogues (PDFs) and price data. It leverages **RAG (Retrieval-Augmented Generation)** technology, combining vector search with Large Language Models (LLMs like Gemini/OpenAI) to provide accurate, context-aware answers about product prices and availability.

## 💡 What is it used for?
- **Automated Price Extraction**: Ingests weekly PDF catalogues from major supermarkets (e.g., Coles, Woolworths).
- **Intelligent Search**: Allows users to ask natural language questions like *"Where is the cheapest milk?"* or *"Compare Coca-Cola prices"*.
- **Visual Analysis**: Uses Vision AI to read prices from complex catalogue images where text extraction fails.

## 🎯 What Business Problem does it solve?
- **Price Transparency**: Solves the difficulty of manually comparing prices across different supermarket flyers.
- **Data Digitization**: Converts unstructured PDF data into structured, searchable product databases.
- **Smart Shopping**: Empowers consumers (or downstream apps) to make data-driven purchasing decisions, instantly identifying the best deals and savings.
"""

# Rate Limiter Configuration
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Supermarket RAG API",
    description=description,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    servers=[
        {"url": "https://xfukqtd5pc.us-east-1.awsapprunner.com", "description": "AWS Production Environment"},
        {"url": "http://localhost:8000", "description": "Local Development"}
    ]
)

# Attach rate limit error handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Permissive CORS Configuration (Supporting Mobile & Web)
# Note: allow_credentials MUST be False when using "*" in allow_origins
allowed_origins_env = os.getenv("CORS_ALLOWED_ORIGINS", "")
if allowed_origins_env:
    allow_origins = [origin.strip() for origin in allowed_origins_env.split(",")]
    allow_credentials = "*" not in allow_origins
else:
    # Default to permissive for mobile apps and multi-subdomain web access
    allow_origins = ["*"]
    allow_credentials = False

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Admin Security
security = HTTPBearer()
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "super-secret-key-change-me")

def verify_admin_key(auth: HTTPAuthorizationCredentials = Security(security)):
    if auth.credentials != ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid admin API key")
    return auth.credentials

UPLOAD_DIR = "uploaded_docs"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

class QueryRequest(BaseModel):
    text: str = Field(..., description="The user query text (e.g., 'price of milk in coles')")
    user_id: str = Field(..., description="The ID of the user for LiteLLM attribution and key generation")
    stream: bool = Field(default=False, description="Whether to stream the response chunks")
    session_id: str = Field(default=None, description="The session ID for chat history grouping")

    @validator("text")
    def validate_text_length(cls, v):
        if len(v) > 1000:
            raise ValueError("Query text too long (max 1000 characters)")
        return v

class ChatResponse(BaseModel):
    response: str = Field(..., description="The RAG-generated response containing product info and price comparison.")
    metadata: list = Field(default=[], description="List of source images and metadata used for the response.")
    backend_version: str = Field(default="v1", description="Backend version identifier.")

class UploadResponse(BaseModel):
    message: str = Field(..., description="Success message")
    filename: str = Field(..., description="Name of the uploaded file")

@app.post("/upload", summary="Upload PDF Document", tags=["Ingestion"], response_model=UploadResponse)
@limiter.limit("5/minute")
async def upload_document(
    request: Request,
    file: UploadFile = File(...), 
    user_id: str = Form("admin_ingest", description="User ID for attribution")
):
    """
    Upload a supermarket catalogue PDF to be ingested into the RAG system.
    The document will be parsed, chunked, and stored in the vector database.
    If the text is sparse, Vision OCR will be attempted.
    """
    # File Validation
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    # Check file size (approximate via content-length header if available, or read chunk)
    # Note: proper size check requires reading file, here we rely on server constraints or explicit read limit
    # Implementing a read constraint:
    MAX_FILE_SIZE = 10 * 1024 * 1024 # 10MB
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
         raise HTTPException(status_code=400, detail="File too large (max 10MB).")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Pass user_id if ingestion logic supports it (currently uses 'admin_ingest' inside RAGEngine)
        count = await rag_engine.ingest_documents(UPLOAD_DIR, user_id=user_id)
        return {"message": f"Successfully ingested {count} documents.", "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", summary="Query Product Prices", tags=["Query"], response_model=ChatResponse)
# @limiter.limit("120/hour")
async def chat(request: Request, body: QueryRequest, background_tasks: BackgroundTasks):
    """
    Query the RAG system for product prices.
    Returns a Markdown formatted table comparing prices between stores (e.g., Coles vs Woolworths)
    and a verdict on which is cheaper.
    """
    # Extract IP address (handle X-Forwarded-For if behind proxy/App Runner)
    ip_address = request.headers.get("X-Forwarded-For")
    if not ip_address:
        ip_address = request.client.host
    else:
        # X-Forwarded-For can be a list, take the first one
        ip_address = ip_address.split(",")[0].strip()

    # Privacy: Hash user_id if it's an email to ensure LiteLLM and logs don't store PII
    effective_user_id = body.user_id
    if "@" in str(effective_user_id):
        if hasattr(rag_engine, 'encryptor') and rag_engine.encryptor:
            effective_user_id = rag_engine.encryptor.hash_pii(effective_user_id)
        else:
            import hmac, hashlib
            salt = os.getenv("PII_HASH_SALT", "default-salt-change-me")
            effective_user_id = hmac.new(
                salt.encode('utf-8'),
                str(effective_user_id).lower().strip().encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
    try:
        # Check if streaming is requested
        if body.stream:
            # rag_engine.query returns an async generator for streaming
            gen = await rag_engine.query(body.text, effective_user_id, stream=True)
            return StreamingResponse(gen, media_type="text/event-stream")

        query_result = await rag_engine.query(body.text, effective_user_id, stream=False)
        response_text = query_result.get("response")
        extracted_metadata = query_result.get("metadata", [])
        
        # Log the interaction in the background
        background_tasks.add_task(
            rag_engine.log_chat, 
            user_id=effective_user_id, 
            query=body.text, 
            response=response_text, 
            ip_address=ip_address,
            session_id=body.session_id
        )
        
        return {"response": response_text, "metadata": extracted_metadata, "backend_version": query_result.get("backend_version", "v1.1")}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", summary="Health Check", tags=["System"])
async def health():
    """
    Simple health check endpoint to verify API reachability.
    """
    return {"status": "ok"}

@app.get("/chat/history", summary="Get Chat History", tags=["Query"])
async def get_chat_history(user_id: str):
    """
    Retrieve the list of recent chat conversations for a specific user.
    """
    try:
        # We need to handle email hashing if user_id is an email
        effective_user_id = user_id
        if "@" in str(effective_user_id):
            if hasattr(rag_engine, 'encryptor') and rag_engine.encryptor:
                effective_user_id = rag_engine.encryptor.hash_pii(effective_user_id)
            else:
                import hmac, hashlib
                salt = os.getenv("PII_HASH_SALT", "default-salt-change-me")
                effective_user_id = hmac.new(
                    salt.encode('utf-8'),
                    str(effective_user_id).lower().strip().encode('utf-8'),
                    hashlib.sha256
                ).hexdigest()

        history = await rag_engine.get_user_conversations(effective_user_id)
        return {"user_id": user_id, "conversations": history}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat/history/{session_id}", summary="Get Conversation Messages", tags=["Query"])
async def get_conversation_messages(session_id: str, user_id: str = None):
    """
    Retrieve all messages for a specific chat session.
    """
    try:
        effective_user_id = None
        if user_id:
             effective_user_id = user_id
             if "@" in str(effective_user_id):
                if hasattr(rag_engine, 'encryptor') and rag_engine.encryptor:
                    effective_user_id = rag_engine.encryptor.hash_pii(effective_user_id)
                else:
                    import hmac, hashlib
                    salt = os.getenv("PII_HASH_SALT", "default-salt-change-me")
                    effective_user_id = hmac.new(
                        salt.encode('utf-8'),
                        str(effective_user_id).lower().strip().encode('utf-8'),
                        hashlib.sha256
                    ).hexdigest()

        messages = await rag_engine.get_conversation_messages(session_id, user_id=effective_user_id)
        return {"session_id": session_id, "messages": messages}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/items", summary="Get Shop Items", tags=["Query"])
@limiter.limit("60/minute")
async def get_items(request: Request, shop_name: str, search: str = None, limit: int = 20, offset: int = 0):
    """
    Retrieve product items for a specific shop (e.g., 'Coles' or 'Woolworths') with pagination.
    """
    try:
        items = await rag_engine.get_shop_items(shop_name, search=search, limit=limit, offset=offset)
        return {"shop_name": shop_name, "search": search, "count": len(items), "items": items, "limit": limit, "offset": offset}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/update-catalogs", summary="Trigger Weekly Catalog Update", tags=["Admin"])
async def trigger_catalog_update(background_tasks: BackgroundTasks, auth_key: str = Security(verify_admin_key)):
    """
    Administrative endpoint to manually or automatically trigger the 
    weekly supermarket catalogue download and ingestion process in the background.
    """
    try:
        from auto_update_catalogs import run_update
        background_tasks.add_task(run_update)
        return {"message": "Catalog update triggered in background."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to trigger update: {e}")

# We need a proper background task implementation for trigger_catalog_update
@app.post("/api/admin/update-catalogs/sync", summary="Trigger Weekly Catalog Update (Sync)", tags=["Admin"])
async def trigger_catalog_update_sync(auth_key: str = Security(verify_admin_key)):
    try:
        from auto_update_catalogs import run_update
        await run_update()
        return {"message": "Catalog update completed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Update failed: {e}")

@app.post("/api/admin/ingest", summary="Re-index Existing Documents", tags=["Admin"])
async def trigger_manual_ingest(auth_key: str = Security(verify_admin_key)):
    """
    Manually trigger re-indexing of all documents in the uploaded_docs directory.
    Useful after switching embedding models or clearing the database.
    """
    try:
        count = await rag_engine.ingest_documents(UPLOAD_DIR, user_id="admin_reingest")
        return {"message": f"Re-indexing completed. {count} documents processed.", "count": count}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Re-indexing failed: {e}")

