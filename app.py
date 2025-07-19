import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/v1/api")
async def root():
    return {"message": "hello form hands on session lab 1"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 