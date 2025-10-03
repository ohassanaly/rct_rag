#fast api serving of my search engine

from query_vector_db import *
from typing import Annotated
from fastapi import FastAPI, Query
from logger import logger
from middleware import log_middleware
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()
app.add_middleware(BaseHTTPMiddleware, dispatch = log_middleware)

load_dotenv()
llm_client = OpenAI()
chroma_client = chromadb.CloudClient(
    api_key=os.getenv("chromadb_api_key"),
    tenant=os.getenv("chroma_tenant"),
    database="rct_rag",
)
collection = chroma_client.get_collection(name="rct_sections")

@app.get("/")
def welcome_page():
    return("Welcome to the searchCT API")

@app.post("/search/")
async def search_engine(user_input: str):
    result = query(user_input, collection, llm_client, logger,"INCLUSION CRITERIA")
    return rank_query_result(result)