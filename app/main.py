
from contextlib import asynccontextmanager
import os
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI

from app.routes import routes



class MyFastAPI(FastAPI):
    # GITHUB_CLIENT_ID: Optional[str] = None
    # GITHUB_CLIENT_SECRET: Optional[str] = None
    # GITHUB_REDIRECT_URI: Optional[str] = None
    pass

 
@asynccontextmanager
async def lifespan(app: MyFastAPI):
    try:
         print("Starting")              


         print("Visit: http://127.0.0.1:8000 for API")
         print("Visit: http://127.0.0.1:8000/docs for API documentation.")
         print()  
         yield 
         
    finally:
         print("\n🛑 Shutting down  server...")



app = MyFastAPI(
    title="Auth",
    description="Auth",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(routes.router)
