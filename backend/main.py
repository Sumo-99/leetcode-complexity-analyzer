from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from api.analysis import router as analysis_router


app = FastAPI()

# Allow localhost origins for frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://leetcode.com",
        "https://www.leetcode.com",
        "https://*.leetcode.com",
        "http://leetcode.com",
        "http://www.leetcode.com",
        "http://*.leetcode.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
def ping():
    return {
        "status": "ok",
        "message": "PONG! Complexity Analyzer API is running"
    }

# Include analysis API router
app.include_router(analysis_router)
