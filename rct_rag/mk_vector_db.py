from config import *
import json
from dotenv import load_dotenv
import chromadb
import os
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

if __name__ == "__main__":
    load_dotenv()
    chroma_client = chromadb.CloudClient(
        api_key=os.getenv("chromadb_api_key"),
        tenant=os.getenv("chroma_tenant"),
        database="rct_rag",
    )
    # loading src data
    with open(process_text_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # run only once for creating collection
    # collection = chroma_client.create_collection(
    #     name="rct_summaries",
    #     embedding_function=OpenAIEmbeddingFunction(
    #         api_key=os.getenv("OPENAI_API_KEY"),
    #         model_name="text-embedding-3-small"
    #     )
    # )
    collection = chroma_client.get_collection(name="rct_summaries")
    #1 line per study and per section
    for study, summary in data.items():
        for section, text in summary.items() :
            collection.add(ids = f"{study}, {section}",
                           metadatas= [{"study" : study,
                                       "section" : section}],
                           documents=[text],
            )
    #previous version with only 1 line per study           
    # collection.add(
    #     ids=list(data.keys()),
    #     documents=[
    #         ", ".join(f"{k}:{v}" for k, v in d.items()) for d in list(data.values())
    #     ],
    # )
