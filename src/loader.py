import pandas as pd
from langchain.schema import Document

def load_data(file_path):
    df = pd.read_excel(file_path)
    df.fillna("", inplace=True)

    documents = []
    metadata = []

    for _, row in df.iterrows():
        text = f"""
Product Name: {row.get('name', '')}
Category: {row.get('category', '')}
Price: ₹{row.get('price', '')}
Features: {row.get('features', '')}
Description: {row.get('description', '')}

This is a {row.get('category', '')} product priced at ₹{row.get('price', '')}.
"""

        doc = Document(
            page_content=text.strip(),
            metadata=row.to_dict()
        )

        documents.append(doc)
        metadata.append(row.to_dict())

    return documents, metadata