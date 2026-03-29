from fastapi import FastAPI
from pydantic import BaseModel
from src.loader import load_data
from src.embedding import get_embeddings
from src.vectorstore import create_vectorstore
from src.filter import apply_filters
from src.ranker import rank_results
from src.generator import generate_response

app = FastAPI()

documents = None
metadata = None
vectorstore = None


@app.on_event("startup")
# @app.lifespan("startup")
def startup_event():
    global documents, metadata, vectorstore

    print("Loading data...")

    try:
        documents, metadata = load_data("data/data.xlsx")
        print(f"📄 Documents loaded: {len(documents)}")

        embeddings = get_embeddings()
        vectorstore = create_vectorstore(documents, embeddings, metadata)

        print("✅ Startup complete")

    except Exception as e:
        print("❌ STARTUP ERROR:", str(e))


# ROOT ROUTE
@app.get("/")
def root():
    return {"message": "AI Shopping Assistant Backend Running"}


# REQUEST MODEL
class QueryRequest(BaseModel):
    query: str


# MAIN API
@app.post("/ask")
def ask_question(request: QueryRequest):
    global vectorstore

    try:
        if vectorstore is None:
            return {
                "answer": "System not ready yet. Please wait.",
                "results": []
            }

        query = request.query
        print("📩 Query:", query)

        # Retrieval
        results = vectorstore.similarity_search(query, k=5)
        print("🔍 Retrieved docs:", len(results))

        # Filtering + Ranking
        results = apply_filters(results, query)
        results = rank_results(results)

        print("After ranking:", len(results))

        # LLM Response
        answer = generate_response(query, results)

        # Return response
        return {
            "answer": answer,
            "results": [doc.metadata for doc in results]
        }

    except Exception as e:
        print("ERROR IN /ask:", str(e))

        import traceback
        traceback.print_exc()

        return {
            "answer": "Something went wrong",
            "results": [],
            "error": str(e)
        }