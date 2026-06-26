from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS


def create_vector_store():

    loader = TextLoader("data/medical_knowledge.txt")

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )

    docs = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_db = FAISS.from_documents(
        docs,
        embeddings
    )

    vector_db.save_local("data/embeddings")

    print("Vector Database Created Successfully!")