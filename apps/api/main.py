from fastapi import FastAPI

app = FastAPI(
    title="Genuine Product Finder API",
    description="Locates verified platforms and delivery times by pincode",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"status": "online", "message": "Genuine Product Finder API operational"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}