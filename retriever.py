from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

vectordb = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

def retrieve_context(query):

    retriever = vectordb.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 3,
            "fetch_k": 10
        }
    )

    results = retriever.invoke(query)

    return "\n\n".join(
        [doc.page_content for doc in results]
    )