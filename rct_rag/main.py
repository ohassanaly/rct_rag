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
collection = chroma_client.get_collection(name="rct_summaries")

@app.get("/query") #TODO : use a post request instead ; the user_input must be a request body instead of a query parameter
async def query_endpoint(user_input: Annotated[str, Query(max_length=50)]):
    result = query(user_input, collection, llm_client, "INCLUSION CRITERIA")
    return {"ids" : result["ids"], "distances" : result["distances"]}

#example : run http://127.0.0.1:8000/query?user_input=dose&finding

#we should rather use this POST request
@app.post("/search/")
async def search_engine(user_input: str):
    result = query(user_input, collection, llm_client, "INCLUSION CRITERIA")
    return result