import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


documents = []

for file in os.listdir("data"):
    if file.endswith(".txt"):
        loader = TextLoader(
            os.path.join("data", file),
            encoding="utf-8"
        )
        documents.extend(loader.load())


print(f"Loaded {len(documents)} documents")

for doc in documents[:2]:
    print(doc.page_content[:200])
    print("-" * 50)



splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks")


load_dotenv()

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

test_embedding = embeddings.embed_query(
    "What is a black hole?"
)

print("Embedding size:", len(test_embedding))

vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="chroma_db"
)

print("Vector Database Created!")

query = "What is a black hole?"

retriever = vectordb.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 3}
)

results = retriever.invoke(query)

print("\nRetrieved Chunks:\n")

for i, doc in enumerate(results):
    print(f"\nResult {i+1}")

    
    if "source" in doc.metadata:
        print("Source:", doc.metadata["source"])

    print(doc.page_content[:500])
    print("=" * 80)


def retrieve_context(query):

    retriever = vectordb.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 3,
        "fetch_k": 10
    }
)

results = retriever.invoke(query)