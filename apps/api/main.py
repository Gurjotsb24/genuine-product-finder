from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.verifier import verify_url, load_verified_platforms
from services.search import search_product

app = FastAPI(
    title="Genuine Product Finder API",
    description="Locates verified platforms and delivery times by pincode",
    version="1.0.0"
)

# Enable CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request Models
class VerifyRequest(BaseModel):
    url: str


class SearchRequest(BaseModel):
    product_name: str
    pincode: str


# API Routes
@app.get("/")
def read_root():
    return {"status": "online", "message": "Genuine Product Finder API operational"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/platforms")
def get_platforms():
    return {"verified_platforms": load_verified_platforms()}


@app.post("/verify")
def verify_domain(request: VerifyRequest):
    if not request.url or not request.url.strip():
        raise HTTPException(status_code=400, detail="URL is required")
    return verify_url(request.url)


@app.post("/search")
def search_product_availability(request: SearchRequest):
    if not request.product_name or not request.product_name.strip():
        raise HTTPException(status_code=400, detail="product_name is required")
    if not request.pincode or not request.pincode.strip():
        raise HTTPException(status_code=400, detail="pincode is required")
    
    return search_product(request.product_name, request.pincode)