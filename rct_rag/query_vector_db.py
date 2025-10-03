from config import *
from dotenv import load_dotenv
import chromadb
import os
from pydantic import BaseModel
from openai import OpenAI
from logging import Logger
from logger import logger
import pandas as pd

class RephrasedQuery(BaseModel):
    queries: list[str]

def rephrase_query(query: str, client) -> list[str]:
    """
    Given a text query, use an LLM to rephrase the query in 3 different ways,
    Typing is ensured by Pdyantic
    """
    completion = client.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system",
                "content": "Rephrase this user query for a clincial trial search engine in 3 different ways",
            },
            {"role": "user", "content": query},
        ],
        response_format=RephrasedQuery,
    )
    event = completion.choices[0].message.parsed
    return event.queries

def query(user_query: str, collection, llm_client, logger: Logger, section_filtering:str ="", top_k: int = 2) -> dict:
    """
    given a user query :
    rephrases it
    generates top k results for each query
    returns : top-k results ids and distance for each query
    """
    rephrasing = rephrase_query(user_query, llm_client)
    logger.info({"search query" : [user_query] + rephrasing})

    if section_filtering == "":
          result = collection.query(
          query_texts=[user_query] + rephrasing,
          n_results=top_k,
          include=["documents", "distances"],
      )

    else :
        assert section_filtering in list(section_categories.keys()), "section_filetring should be a valid section"
        result = collection.query(
        query_texts=[user_query] + rephrasing,
        n_results=top_k,
        include=["documents", "distances"],
        where={"section": section_filtering} #eventually query several sections?
      )
    return result

def rank_query_result(result: dict, top_k :int=3) -> str:
    """
    Input : result of the vector database query 
    Output : JSON with results ids, distances and document content ranked by average distance to queries and keeping only top k results
    """
    results = []
    for ids, dists, doc_texts in zip(result["ids"], result["distances"], result["documents"]):
        for id_, dist, doc_text in zip(ids, dists, doc_texts):
            results.append((id_, dist, doc_text))
    df = pd.DataFrame(results, columns=["id", "distance", "doc_text"])

    ranked_df = df.groupby(["id", "doc_text"])["distance"].mean().reset_index().sort_values(by="distance")

    output = ranked_df[:top_k].to_json(orient="records")
    logger.info({"result" : output})

    return output

if __name__ == "__main__":

    load_dotenv()
    llm_client = OpenAI()
    chroma_client = chromadb.CloudClient(
        api_key=os.getenv("chromadb_api_key"),
        tenant=os.getenv("chroma_tenant"),
        database="rct_rag",
    )
    collection = chroma_client.get_collection(name="rct_sections")

    user_query = "dose finding clinical trial"
    result = query(user_query, collection, llm_client, logger, "INCLUSION CRITERIA")
    print(rank_query_result(result))
