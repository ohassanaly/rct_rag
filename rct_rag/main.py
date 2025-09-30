#fast api serving of my search engine

from query_vector_db import *
from fastapi import FastAPI, Query

app = FastAPI()

load_dotenv()
llm_client = OpenAI()
chroma_client = chromadb.CloudClient(
    api_key=os.getenv("chromadb_api_key"),
    tenant=os.getenv("chroma_tenant"),
    database="rct_rag",
)
collection = chroma_client.get_collection(name="rct_summaries")

@app.get("/query")
async def query_endpoint(user_input: str=Query()):
    result = query(user_input, collection, llm_client, "INCLUSION CRITERIA")
    return {"ids" : result["ids"], "distances" : result["distances"]}