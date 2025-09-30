from config import *
from dotenv import load_dotenv
import chromadb
import os
from pydantic import BaseModel
from openai import OpenAI


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

def query(user_query: str, collection, llm_client, section_filtering:str ="", top_k: int = 2) -> dict:
    """
    given a user query :
    rephrases it
    generates top k results for each query
    returns : top-k results ids and distance for each query
    """
    rephrasing = rephrase_query(user_query, llm_client)

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

if __name__ == "__main__":

    load_dotenv()
    llm_client = OpenAI()
    chroma_client = chromadb.CloudClient(
        api_key=os.getenv("chromadb_api_key"),
        tenant=os.getenv("chroma_tenant"),
        database="rct_rag",
    )
    collection = chroma_client.get_collection(name="rct_summaries")

    user_query = "dose finding clinical trial"
    result = query(user_query, collection, llm_client, "INCLUSION CRITERIA")
    print(result["ids"])
    print(result["distances"])
