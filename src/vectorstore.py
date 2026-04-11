from langchain_community.vectorstores import FAISS

def create_vectorstore(documents, embeddings, metadata):
    return FAISS.from_documents(documents, embeddings)