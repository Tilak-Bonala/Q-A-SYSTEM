import langchain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.document_loaders import CSVLoader, DirectoryLoader

from langchain_huggingface import HuggingFaceEmbeddings


from typing import List

def load_csv_files(data: str):
    loader = DirectoryLoader(
        data,
        glob="*train*.csv",
        loader_cls=CSVLoader,
        loader_kwargs={"encoding": "utf-8"}  
    )
    extracted_data = loader.load()
    return extracted_data

def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    minimal_docs: List[Document] = []
    for doc in docs:
        src = doc.metadata.get("source")
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source": src}
            )
        )
    return minimal_docs

def text_split(docs: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20
    )
    return splitter.split_documents(docs)



def download_embeddings():
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name
    )
    return embeddings





